import yaml
from yaml.loader import SafeLoader
import random


def create_cartservice_yamls(idx, used_ports, child_to_parents_relations, child_addresses_redis):
    """
    Create new YAML files for new cartservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    This function also uses child microservices addresses for relevant fields in parent cartservice microservice YAMLs
        and updates the child microservices addresses dictionary accordingly.

    :param idx: int: new cartservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservice (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).
    :param child_addresses_redis: dictionary: used and unused addresses of newly created (YAMLs) redis-cart microservices,
            which are cartservice's child microservices.

    :return new cartservice microservice's address in the format of label:port.
    """

    # new_cartservice_port = general_functions.generate_new_port(used_ports)
    cartservice_port = 7070
    new_cartservice_label = f"cartservice-{idx}"
    new_cartservice_address = f"{new_cartservice_label}:{cartservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(r'..\deploy_and_svc_yamls\cartservice-yamls\cartservice-deploy.yaml', 'r') as f_in:
        with open(f'yamls-to-apply/cartservice-apply/cartservice-deploy-{idx}.yaml', 'w') as f_out:
            cartservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            cartservice_deploy['metadata']['name'] = new_cartservice_label
            cartservice_deploy['spec']['selector']['matchLabels']['app'] = new_cartservice_label
            cartservice_deploy['spec']['template']['metadata']['labels']['app'] = new_cartservice_label

            cartservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0][
                'containerPort'] = cartservice_port
            # cartservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(
            #     cartservice_port)
            # cartservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec']['command'][
            #     1] = f"-addr=:{cartservice_port}"
            # cartservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec']['command'][
            #     1] = f"-addr=:{cartservice_port}"

            # Choose a child microservice for the new microservice created and update environment variables.
            # First, look for an 'unused' child microservice.
            # If all are used, choose a 'used' child microservice randomly.
            curr_child_address_redis = child_addresses_redis['unused'].pop(0) if child_addresses_redis['unused'] \
                else random.choice(child_addresses_redis['used'])
            if curr_child_address_redis not in child_addresses_redis['used']:
                child_addresses_redis['used'].append(curr_child_address_redis)
            cartservice_deploy['spec']['template']['spec']['containers'][0]['env'][0][
                'value'] = curr_child_address_redis

            yaml.dump(cartservice_deploy, f_out)

    # This is a new parent microservice - update the relation to the chosen child microservice in the relations dictionary.
    child_to_parents_relations[curr_child_address_redis].append(new_cartservice_label)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(r'..\deploy_and_svc_yamls\cartservice-yamls\cartservice-svc.yaml', 'r') as f_in:
        with open(f'/yamls-to-apply/cartservice-apply/cartservice-svc-{idx}.yaml', 'w') as f_out:
            cartservice_svc = yaml.load(f_in, Loader=SafeLoader)
            cartservice_svc['metadata']['name'] = new_cartservice_label
            cartservice_svc['spec']['selector']['app'] = new_cartservice_label
            # Only change "outside" port (no need to change targetPort - which is the target port inside the container).
            cartservice_svc['spec']['ports'][0]['port'] = cartservice_port
            # cartservice_svc['spec']['ports'][0]['targetPort'] = cartservice_port

            yaml.dump(cartservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(cartservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_cartservice_address] = []

    return new_cartservice_address
