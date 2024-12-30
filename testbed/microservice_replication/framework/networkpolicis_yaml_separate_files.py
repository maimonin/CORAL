import yaml
from yaml.loader import SafeLoader
import framework_general_funcs as general_functions


def create_networkpolicy_seperate_files(child_address, parents_ms_list):
    """
    Creates new YAML files of NetworkPolicies for new child microservices to be added to the cluster.
    Creates number of NetworkPolicy YAMLs as number of parents microservices (all the traffic in the application is incoming - ingress).

    :param child_address: current child microservice to create NetworkPolicy YAMLs for.
    :param parents_ms_list: list: parent microservices of the child microservice.
    """

    child_label, child_port = child_address.split(":")[0], child_address.split(":")[1]

    child_label_ms, child_ms_idx = child_label.split("-")[0], child_label.split("-")[1]
    # Fix microservice label and index for redis-cart microservice.
    if child_label_ms == "redis":
        child_label_ms = "redis-cart"
        child_ms_idx = 1

    # Read network policy YAML file template, and rewrite needed fields in order to create a new network policy YAML
    # file for the new microservice to be added.
    # Choose the correct network policy template according to the number of parent microservices -
    # it is needed to create a separate YAML file for each network policy
    # (each file/network policy is for ingress to child microservice from each of its parent microservices).
    with open(
            general_functions.get_path(r'utils\netpol-template-selector.yaml'),
            'r') as f_in:
        child_netpol = yaml.load(f_in, Loader=SafeLoader)

        child_netpol['spec']['podSelector']['matchLabels']['app'] = child_label

        # Iterate over all parent microservices and update ingress from them.
        for parent_idx in range(0, len(parents_ms_list)):
            parent_ms_label = parents_ms_list[parent_idx]
            with open(
                    f'yamls-to-apply/{child_label_ms}-apply/{child_label_ms}-netpol-{child_ms_idx}-{parent_ms_label}.yaml',
                    'w') as f_out:
                child_netpol['metadata']['name'] = f'{child_label_ms}-{child_ms_idx}-allow-{parent_ms_label}'
                child_netpol['spec']['ingress'][0]['from'] = []
                # Update ingress to be from current parent microservice from the list of parents.
                child_netpol['spec']['ingress'][0]['from'].append(
                    {'podSelector': {'matchLabels': {'app': parent_ms_label}}})

                # Update port according to service resource port.
                child_netpol['spec']['ingress'][0]['ports'][0]['port'] = int(child_port)

                yaml.dump(child_netpol, f_out)
