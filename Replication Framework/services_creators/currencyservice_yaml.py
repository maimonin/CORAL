import yaml
from yaml.loader import SafeLoader
from utils import general_functions
from utils.general_functions import get_path


def create_currencyservice_yamls(idx, used_ports, child_to_parents_relations):
    """
    Create new YAML files for new currencyservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    :param idx: int: new currencyservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).
    :return new currencyservice microservice's address in the format of label:port.
    """

    new_currencyservice_port = general_functions.generate_new_port(used_ports)
    new_currencyservice_label = f"currencyservice-{idx}"
    new_currencyservice_address = f"{new_currencyservice_label}:{new_currencyservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(get_path(r'utils\currencyservice-yamls\currencyservice-deploy.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/currencyservice-apply/currencyservice-deploy-{idx}.yaml',
                'w') as f_out:
            currencyservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            currencyservice_deploy['metadata']['name'] = new_currencyservice_label
            currencyservice_deploy['spec']['selector']['matchLabels']['app'] = new_currencyservice_label
            currencyservice_deploy['spec']['template']['metadata']['labels']['app'] = new_currencyservice_label

            currencyservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_currencyservice_port
            currencyservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value']=str(new_currencyservice_port)
            currencyservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec'][
                'command'][1] = f"-addr=:{new_currencyservice_port}"
            currencyservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec'][
                'command'][1] = f"-addr=:{new_currencyservice_port}"

            yaml.dump(currencyservice_deploy, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(get_path(r'utils\currencyservice-yamls\currencyservice-svc.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/currencyservice-apply/currencyservice-svc-{idx}.yaml',
                'w') as f_out:
            currencyservice_svc = yaml.load(f_in, Loader=SafeLoader)

            currencyservice_svc['metadata']['name'] = new_currencyservice_label
            currencyservice_svc['spec']['selector']['app'] = new_currencyservice_label
            currencyservice_svc['spec']['ports'][0]['port'] = new_currencyservice_port
            currencyservice_svc['spec']['ports'][0]['targetPort'] = new_currencyservice_port

            yaml.dump(currencyservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_currencyservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_currencyservice_address] = []

    return new_currencyservice_address
