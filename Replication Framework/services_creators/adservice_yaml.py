import yaml
from yaml.loader import SafeLoader
from utils import general_functions
from utils.general_functions import get_path


def create_adservice_yamls(idx, used_ports, child_to_parents_relations):
    """
    Create new YAML files for new adservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    :param idx: int: new adservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster (by Kubernetes services).
    :param child_to_parents_relations: dictionary: lists for each child microservice (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).
    :return new adservice microservice's address in the format of label:port.
    """

    new_adservice_port = general_functions.generate_new_port(used_ports)
    new_adservice_label = f"adservice-{idx}"
    new_adservice_address = f"{new_adservice_label}:{new_adservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(get_path(r'utils\adservice-yamls\adservice-deploy.yaml'),
              'r') as f_in:
        with open(f'yamls-to-apply/adservice-apply/adservice-deploy-{idx}.yaml',
                'w') as f_out:
            adservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            adservice_deploy['metadata']['name'] = new_adservice_label
            adservice_deploy['spec']['selector']['matchLabels']['app'] = new_adservice_label
            adservice_deploy['spec']['template']['metadata']['labels']['app'] = new_adservice_label

            adservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_adservice_port
            adservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = f'{new_adservice_port}'
            adservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(new_adservice_port)
            adservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec']['command'][
                1] = f"-addr=:{new_adservice_port}"
            adservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec']['command'][
                1] = f"-addr=:{new_adservice_port}"

            yaml.dump(adservice_deploy, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(get_path(r'utils\adservice-yamls\adservice-svc.yaml'), 'r') as f_in:
        with open(f'yamls-to-apply/adservice-apply/adservice-svc-{idx}.yaml',
                'w') as f_out:
            adservice_svc = yaml.load(f_in, Loader=SafeLoader)

            adservice_svc['metadata']['name'] = new_adservice_label
            adservice_svc['spec']['selector']['app'] = new_adservice_label
            adservice_svc['spec']['ports'][0]['port'] = new_adservice_port
            adservice_svc['spec']['ports'][0]['targetPort'] = new_adservice_port

            yaml.dump(adservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_adservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_adservice_address] = []

    return new_adservice_address
