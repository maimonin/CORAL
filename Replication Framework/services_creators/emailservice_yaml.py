import yaml
from yaml.loader import SafeLoader
from utils import general_functions
from utils.general_functions import get_path


def create_emailservice_yamls(idx, used_ports, child_to_parents_relations):
    """
    Create new YAML files for new emailservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    :param idx: int: new emailservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).
    :return new emailservice microservice's address in the format of label:port.
    """

    new_emailservice_port = general_functions.generate_new_port(used_ports)
    new_emailservice_label = f"emailservice-{idx}"
    new_emailservice_address = f"{new_emailservice_label}:{new_emailservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(get_path(r'utils\emailservice-yamls\emailservice-deploy.yaml'),
              'r') as f_in:
        with open(f'yamls-to-apply/emailservice-apply/emailservice-deploy-{idx}.yaml',
                'w') as f_out:
            emailservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            emailservice_deploy['metadata']['name'] = new_emailservice_label
            emailservice_deploy['spec']['selector']['matchLabels']['app'] = new_emailservice_label
            emailservice_deploy['spec']['template']['metadata']['labels']['app'] = new_emailservice_label
            emailservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(
                new_emailservice_port)
            emailservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0][
                'containerPort'] = new_emailservice_port
            emailservice_deploy['spec']['template']['spec']['containers'][0]['env'][0][
                'value'] = f'{new_emailservice_port}'
            emailservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec'][
                'command'][1] = f"-addr=:{new_emailservice_port}"
            emailservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec'][
                'command'][1] = f"-addr=:{new_emailservice_port}"

            yaml.dump(emailservice_deploy, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(get_path(r'utils\emailservice-yamls\emailservice-svc.yml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/emailservice-apply/emailservice-svc-{idx}.yaml',
                'w') as f_out:
            emailservice_svc = yaml.load(f_in, Loader=SafeLoader)

            emailservice_svc['metadata']['name'] = new_emailservice_label
            emailservice_svc['spec']['selector']['app'] = new_emailservice_label
            emailservice_svc['spec']['ports'][0]['port'] = new_emailservice_port
            emailservice_svc['spec']['ports'][0]['targetPort'] = new_emailservice_port

            yaml.dump(emailservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_emailservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_emailservice_address] = []

    return new_emailservice_address
