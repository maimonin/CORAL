import os.path
import shutil
import pandas as pd
from dash import html
from kubernetes import client
import random
import networkx as nx
import matplotlib.pyplot as plt


def get_path(repo_path, rel_path):
    """
    Join a relative path to a repository path.

    Parameters:
    rel_path (str): The relative path to be appended.
    repo_path (str): The base repository path to which the relative path will
                     be added.

    Returns:
    str: The combined path as a string.
    """
    return os.path.join(repo_path, rel_path)


def copy_files(source_folder, destination_folder):
    """
    Copy all files from a source folder to a destination folder.

    Parameters:
        source_folder: str
            Path to the folder containing files to be copied.
        destination_folder: str
            Path to the target folder where files will be copied.
    """
    # fetch all files
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = source_folder + file_name
        destination = destination_folder + file_name
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f'COPIED {file_name} from {source} into {destination}')


def config_api():
    """
    Configure the client and API client in order to access Kubernetes API with Python client.

    return: the desired API client configuration.
    """
    client_config = client.configuration.Configuration()
    client_config.host = "127.0.0.1:8001"
    api_client_config = client.ApiClient(configuration=client_config)
    return api_client_config


def print_deployments():
    """
    Prints the details of multiple Kubernetes deployments into individual text files.
    """
    deploys_list = ['adservice', 'cartservice', 'checkoutservice', 'currencyservice', 'emailservice', 'frontend',
                    'loadgenerator', 'paymentservice', 'productcatalogservice', 'recommendationservice', 'redis-cart',
                    'shippingservice']
    apps_api = client.AppsV1Api(api_client=config_api())
    for deploy_name in deploys_list:
        curr_deployment = apps_api.read_namespaced_deployment(name=deploy_name, namespace="attack-graphs")
        f = open(f"deployment-texts/{deploy_name}_deployment.txt", mode='w')
        print(curr_deployment, file=f)

    # frontend_deploy = apps_api.read_namespaced_deployment(name='frontend', namespace="attack-graphs")
    # f = open("frontend_deployment.txt", mode='w')
    # print(frontend_deploy, file=f)


def get_used_ports(config_client_api):
    """
    Get all currently used ports in cluster.

    :return: list of ports.
    """

    core_api = client.CoreV1Api(api_client=config_client_api)
    svc_list = core_api.list_namespaced_service(namespace="attack-graphs")
    return list(set([svc.spec.ports[0].target_port for svc in svc_list.items]))


def generate_new_port(used_ports):
    """
    Generate a new port to allocate after checking it is not used in the cluster already.

    :param: used_ports: list of already used ports in cluster.

    :return: new_port: int: new port number available for use.
    """
    # port_range = [1025, 65536]
    new_port = random.randint(1025, 65536)
    while new_port in used_ports:
        new_port = random.randint(1025, 65536)
    return new_port


def parse_inbound_pods(x):
    """
    Parses a string representation of inbound pods and transforms it into a structured format.

    Parameters:
        x (str): A string containing inbound pod data to be processed.

    Returns:
        list: A list of formatted data extracted from the input string.
                Each item is either a tuple of three elements (str, int, str) or a single string based on the structure of the parsed input.
    """
    l = x.strip('][').split(')')
    l2 = []
    for item in l:
        if item == '':
            continue
        item = item.strip('(')
        item = item.strip(',(')
        item = item.replace(" ", "")
        item = item.replace("'", "")
        split_item = item.strip(')(').split(',')
        if len(split_item) == 3:
            l2.append((split_item[0], int(split_item[1]), split_item[2]))
        else:
            l2.append(split_item[0])
    return l2


def draw_topology(df):
    """
    Draw a network topology graph based on input data.

    Parameters:
        df (pandas.DataFrame): A DataFrame containing the details required to build the graph.
                               It must include the columns "Pod-ID" and "Pod-Inbound-List".
    """
    ls = []
    for i in range(len(df)):
        if df["Pod-ID"][i].startswith('frontend'):
            continue
        for in_pod in parse_inbound_pods(df['Pod-Inbound-List'][i]):
            ls.append((in_pod[0], df["Pod-ID"][i]))
    G = nx.from_edgelist(ls, create_using=nx.DiGraph())
    plt.figure(figsize=(15, 10))
    nx.draw(G, with_labels=True, node_size=1000, alpha=0.5, arrows=True, font_size=10)
    plt.show()



if __name__ == '__main__':

    path_dir = r'C:\Users\Administrator\PycharmProjects\attack-graphs\Demo\assets\dynamic_topologies\0'
    path = os.path.join(path_dir, 'sub_graph_topology.csv')
    df = pd.read_csv(path)
    df2 = pd.read_csv(os.path.join(path_dir, 'sub_graph_cve.csv'))
    # df=df[df['Pod-Inbound-List']!= '[]']
    df2=df2[df2['Pod-ID'].isin(df['Pod-ID'].tolist())]
    # print(df)
    # df.to_csv(path, index=False)
    df2.to_csv(os.path.join(path_dir, 'sub_graph_cve.csv'), index=False)
    draw_topology(df)