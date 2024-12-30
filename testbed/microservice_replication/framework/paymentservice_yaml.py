import yaml
from yaml.loader import SafeLoader
import framework_general_funcs as general_functions


def create_paymentservice_yamls(idx, used_ports, child_to_parents_relations):
    """
    Create new YAML files for new paymentservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.

    :param idx: int: new paymentservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).

    :return new paymentservice microservice's address in the format of label:port.
    """

    new_paymentservice_port = general_functions.generate_new_port(used_ports)
    new_paymentservice_label = f"paymentservice-{idx}"
    new_paymentservice_address = f"{new_paymentservice_label}:{new_paymentservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                         r'paymentservice-yamls\paymentservice-deploy.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/paymentservice-apply/paymentservice-deploy-{idx}.yaml',
                'w') as f_out:
            paymentservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            paymentservice_deploy['metadata']['name'] = new_paymentservice_label
            paymentservice_deploy['spec']['selector']['matchLabels']['app'] = new_paymentservice_label
            paymentservice_deploy['spec']['template']['metadata']['labels']['app'] = new_paymentservice_label
            paymentservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(
                new_paymentservice_port)
            paymentservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_paymentservice_port
            paymentservice_deploy['spec']['template']['spec']['containers'][0]['env'][0][
                'value'] = f'{new_paymentservice_port}'
            paymentservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec'][
                'command'][1] = f"-addr=:{new_paymentservice_port}"
            paymentservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec'][
                'command'][1] = f"-addr=:{new_paymentservice_port}"

            yaml.dump(paymentservice_deploy, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                         r'paymentservice-yamls\paymentservice-svc.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/paymentservice-apply/paymentservice-svc-{idx}.yaml',
                'w') as f_out:
            paymentservice_svc = yaml.load(f_in, Loader=SafeLoader)

            paymentservice_svc['metadata']['name'] = new_paymentservice_label
            paymentservice_svc['spec']['selector']['app'] = new_paymentservice_label
            paymentservice_svc['spec']['ports'][0]['port'] = new_paymentservice_port
            paymentservice_svc['spec']['ports'][0]['targetPort'] = new_paymentservice_port

            yaml.dump(paymentservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_paymentservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_paymentservice_address] = []

    return new_paymentservice_address
