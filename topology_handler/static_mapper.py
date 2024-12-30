from kubernetes import client
import pandas as pd
import subprocess

# Path to the CSV file where the topology mapping will be saved
OUTPUT_CSV_PATH = "/home/ubuntu/attack-graphs-/Demo/assets/topology_mapping_static.csv"

def create_topology(config_api_client):
    """
    Creates a topology mapping for Kubernetes Pods and Network Policies within a cluster.
    This function extracts detailed data about Pods, including their IDs, IP addresses, and inbound networking configurations
    such as protocols and ports. It also analyzes Network Policies in the specified namespace to determine Pod connections and relations.
    The resulting topology includes the following details for each Pod:
    - Pod-ID: Unique identifier for the Pod.
    - IP: Pod's IP address.
    - Pod-Inbound-List: A list of inbound connections represented as tuples of (Pod-ID, Protocol, Port).
    - Protocol: The protocol used (e.g., TCP, UDP).
    - Port: The port number.
    The function constructs a structured DataFrame combining this information, enabling further analysis or export as a CSV file.

    :param config_api_client: API Client configuration for accessing the Kubernetes API using the Python client.
    :return: Saves the constructed topology as a CSV file.
    """
    # Get pods information.
    core_api = client.CoreV1Api(api_client=config_api_client)
    df_pods = pd.DataFrame(columns=['label', 'name', 'port', 'protocol', 'pod_ip'])
    pods_list = core_api.list_namespaced_pod(namespace='default')
    for pod in pods_list.items:
        curr_pod_row = pd.Series({'label': pod.metadata.labels["app"] if "app" in pod.metadata.labels else '',
                                  'name': pod.metadata.name,
                                  'port': pod.spec.containers[0].ports[0].container_port if
                                  pod.spec.containers[0].ports is not None else 0,
                                  'protocol': pod.spec.containers[0].ports[0].protocol if
                                  pod.spec.containers[0].ports is not None else 0,
                                  'pod_ip': pod.status.pod_i_ps[0].ip})
        df_pods = pd.concat([df_pods, curr_pod_row.to_frame().T], ignore_index=True)

    # Get network policies information.
    networking_api = client.NetworkingV1Api(api_client=config_api_client)
    df_netpol = pd.DataFrame(columns=['pod', 'ingress_from', 'ingress_port', 'ingress_protocol'])
    netpol_list = networking_api.list_namespaced_network_policy(namespace='default')
    for netpol in netpol_list.items:
        pol_types_list = netpol.spec.policy_types
        for poltype in pol_types_list:
            if poltype == 'Ingress':
                curr_netpol_ingress_row = pd.Series({'pod': netpol.spec.pod_selector.match_labels['app'],
                                                     "ingress_from":
                                                         netpol.spec.ingress[0]._from[0].pod_selector.match_labels[
                                                             'app']
                                                         if netpol.spec.ingress[0]._from is not None else "None",
                                                     "ingress_port": [p.port for p in netpol.spec.ingress[0].ports],
                                                     # netpol.spec.ingress[0].ports[0].port,
                                                     "ingress_protocol": netpol.spec.ingress[0].ports[0].protocol})
                df_netpol = pd.concat([df_netpol, curr_netpol_ingress_row.to_frame().T], ignore_index=True)
    df_netpol['ingress_from'] = df_netpol.groupby('pod')['ingress_from'].transform(lambda x: ','.join(x))
    df_netpol = df_netpol.drop_duplicates(subset=['pod'])

    # Join pods & network policies information.
    df_topology = df_pods.join(df_netpol.set_index('pod')['ingress_from'], on='label')
    df_topology = df_topology.dropna()
    df_topology['Pod-Inbound-List'] = ""

    for index, row in df_topology.iterrows():
        inbound_list = []
        for p in row['ingress_from'].split(','):
            curr_inbound = df_pods[df_pods['label'] == p]
            if not curr_inbound.empty:
                # if p == "frontend":
                #     inbound_list.append((str(curr_inbound['name'].iloc[0], "8080", "TCP"))
                # else:
                inbound_list.append((str(curr_inbound['label'].iloc[0]), str(curr_inbound['port'].iloc[0]),
                                     str(curr_inbound['protocol'].iloc[0])))
                df_topology.at[index, 'Pod-Inbound-List'] = inbound_list

    # Organize topology dataframe.
    df_topology.drop(['name', 'ingress_from'], axis=1, inplace=True)
    df_topology.rename(columns={'label': "Pod-ID",
                                'pod_ip': "IP",
                                'protocol': "Protocol",
                                'port': "Port"}, inplace=True)
    df_topology = df_topology[['Pod-ID', 'IP', 'Pod-Inbound-List', 'Protocol', 'Port']]

    svc_list = core_api.list_namespaced_service(namespace='default')
    for svc in svc_list.items:
        if svc.spec.type == 'LoadBalancer':
            curr_pod = df_pods[df_pods['label'] == svc.spec.selector['app']]
            topology_pods = df_topology["Pod-ID"].tolist()
            curr_pod_label = curr_pod["label"].tolist()[0]
            if curr_pod_label in topology_pods:
                idx = df_topology.index[df_topology['Pod-ID'] == curr_pod_label]
                if not idx.empty:
                    current_inbound_list = df_topology.at[idx[0], 'Pod-Inbound-List']
                    if isinstance(current_inbound_list, str):
                        current_inbound_list = [current_inbound_list]  # Convert the string to a list

                    # Check if the list contains only empty strings, and add 'Internet' in that case
                    if all(item == '' for item in current_inbound_list):
                        current_inbound_list = ['Internet']
                        df_topology.at[idx[0], 'Pod-Inbound-List'] = current_inbound_list
                else:
                    df_topology = df_topology.append(
                        pd.DataFrame({"Pod-ID": str(curr_pod['label'].iloc[0]), "IP": str(curr_pod['pod_ip'].iloc[0]),
                                      'Pod-Inbound-List': ['Internet'], "Protocol": str(curr_pod['protocol'].iloc[0]),
                                      "Port": str(curr_pod['port'].iloc[0])}))

    df_topology.to_csv(OUTPUT_CSV_PATH, index=False)


def config_api():
    """
    Configure the client and API client in order to access Kubernetes API with Python client.
    return: the desired API client configuration.
    """
    client_config = client.configuration.Configuration()
    client_config.host = "127.0.0.1:8001"
    api_client_config = client.ApiClient(configuration=client_config)
    return api_client_config


def run_terminal_command_background(command):
    """
    Run a terminal command in the background using subprocess.Popen.
    Args:
    - command (str): The command to be executed.
    """
    try:
        # Run the command in the background using subprocess.Popen
        subprocess.Popen(['sudo', 'su', '-c', command], shell=False)
        print(f"Command '{command}' started successfully in the background.")
    except Exception as e:
        print(f"Error starting command '{command}': {str(e)}")


def run_topology_creation():
    """
    Initiates the processes required to create a Kubernetes topology.
    This function performs the following actions:
    1. Starts any required background processes, such as establishing a `kubectl proxy` for communicating with the Kubernetes cluster.
    2. Configures a Kubernetes API client to facilitate interactions with the Kubernetes API.
    3. Creates a topology mapping using the configured API client.
    """
    # Start the required background processes
    run_terminal_command_background("kubectl proxy")

    # Configure the API client for Kubernetes
    config_client_api = config_api()

    # Create the topology mapping
    create_topology(config_client_api)
