import yaml
from yaml.loader import SafeLoader
import framework_general_funcs as general_functions
import random


def create_recommendationservice_yamls(idx, used_ports, child_to_parents_relations, child_addresses_product):
    """
    Create new YAML files for new recommendationservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    This function also uses child producatcatalogservice microservices addresses for relevant fields in parent recommendationservice microservice's YAMLs
        and updates the child microservices addresses dictionary accordingly.

    :param idx: int: new recommendationservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).
    :param child_addresses_product: dictionary: used and unused addresses of newly created (YAMLs) productcatalog microservices,
            which are recommendationservice's child microservices.

    :return new recommendationservice microservice's address in the format of label:port.
    """

    new_recommendationservice_port = general_functions.generate_new_port(used_ports)
    new_recommendationservice_label = f"recommendationservice-{idx}"
    new_recommendationservice_address = f"{new_recommendationservice_label}:{new_recommendationservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(
            general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                       r'recommendationservice-yamls\recommendationservice-deploy.yaml'),
            'r') as f_in:
        with open(
                f'yamls-to-apply/recommendationservice-apply/recommendationservice-deploy-{idx}.yaml',
                'w') as f_out:
            recommendationservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            recommendationservice_deploy['metadata']['name'] = new_recommendationservice_label
            recommendationservice_deploy['spec']['selector']['matchLabels']['app'] = new_recommendationservice_label
            recommendationservice_deploy['spec']['template']['metadata']['labels'][
                'app'] = new_recommendationservice_label

            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(
                new_recommendationservice_port)
            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_recommendationservice_port
            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec'][
                'command'][1] = f"-addr=:{new_recommendationservice_port}"
            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec'][
                'command'][1] = f"-addr=:{new_recommendationservice_port}"
            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['env'][0][
                'value'] = f'{new_recommendationservice_port}'

            # Choose a child microservice for the new microservice created and update environment variables.
            # First, look for an 'unused' child microservice.
            # If all are used, choose a 'used' child microservice randomly.
            curr_child_address_product = child_addresses_product['unused'].pop(0) if child_addresses_product[
                'unused'] else random.choice(child_addresses_product['used'])
            if curr_child_address_product not in child_addresses_product['used']:
                child_addresses_product['used'].append(curr_child_address_product)
            recommendationservice_deploy['spec']['template']['spec']['containers'][0]['env'][1][
                'value'] = curr_child_address_product

            yaml.dump(recommendationservice_deploy, f_out)

    # This is a new parent microservice - update the relation to the chosen child microservice in the relations dictionary.
    child_to_parents_relations[curr_child_address_product].append(new_recommendationservice_label)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(
             general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                        r'recommendationservice-yamls\recommendationservice-svc.yaml'),
            'r') as f_in:
        with open(
                f'yamls-to-apply/recommendationservice-apply/recommendationservice-svc-{idx}.yaml',
                'w') as f_out:
            recommendationservice_svc = yaml.load(f_in, Loader=SafeLoader)

            recommendationservice_svc['metadata']['name'] = new_recommendationservice_label
            recommendationservice_svc['spec']['selector']['app'] = new_recommendationservice_label
            recommendationservice_svc['spec']['ports'][0]['port'] = new_recommendationservice_port
            recommendationservice_svc['spec']['ports'][0]['targetPort'] = new_recommendationservice_port

            yaml.dump(recommendationservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_recommendationservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_recommendationservice_address] = []

    return new_recommendationservice_address
