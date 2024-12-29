import yaml
from yaml.loader import SafeLoader
from utils import general_functions
import random

from utils.general_functions import get_path


def create_frontend_yamls(idx, used_ports, child_to_parents_relations,
                          child_addresses_ad,
                          child_addresses_recommend,
                          child_addresses_product,
                          child_addresses_cart,
                          child_addresses_checkout,
                          child_addresses_shipping,
                          child_addresses_currency):
    """
    Create new YAML files for new frontend microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (2) -
                ClusterIP,
                LoadBalancer.
    :param idx: new frontend microservice's index.
    :param used_ports: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).

    Child microservices addresses parameters:
    :param child_addresses_ad: dictionary: used and unused addresses of newly created (YAMLs) adservice microservices,
            which are frontend's child microservices.
    :param child_addresses_recommend: dictionary: used and unused addresses of newly created (YAMLs) recommendationservice microservices,
            which are frontend's child microservices.
    :param child_addresses_product: dictionary: used and unused addresses of newly created (YAMLs) productcatalog microservices,
            which are frontend's child microservices.
    :param child_addresses_cart: dictionary: used and unused addresses of newly created (YAMLs) cartservice microservices,
            which are frontend's child microservices.
    :param child_addresses_checkout: dictionary: used and unused addresses of newly created (YAMLs) checkoutservice microservices,
            which are frontend's child microservices.
    :param child_addresses_shipping: dictionary: used and unused addresses of newly created (YAMLs) shippingservice microservices,
            which are frontend's child microservices.
    :param child_addresses_currency: dictionary: used and unused addresses of newly created (YAMLs) currecyservice microservices,
            which are frontend's child microservices.
    :return new frontend microservice's address in the format label:port.
    """

    new_frontend_port = general_functions.generate_new_port(used_ports)
    new_frontend_label = f"frontend-{idx}"
    new_frontend_address = f"{new_frontend_label}:{new_frontend_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(get_path(r'utils\frontend-yamls\frontend-deploy.yaml'), 'r') as f_in:
        with open(
                f'yamls-to-apply/frontend-apply/frontend-deploy-{idx}.yaml',
                'w') as f_out:
            frontend_deploy = yaml.load(f_in, Loader=SafeLoader)

            frontend_deploy['metadata']['name'] = new_frontend_label
            frontend_deploy['spec']['selector']['matchLabels']['app'] = new_frontend_label
            frontend_deploy['spec']['template']['metadata']['labels']['app'] = new_frontend_label

            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(
                new_frontend_port)
            frontend_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_frontend_port
            frontend_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['httpGet'][
                'port'] = new_frontend_port
            frontend_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['httpGet'][
                'port'] = new_frontend_port
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = f'{new_frontend_port}'

            # Choose a child microservice for the new microservice created and update environment variables.
            # First, look for an 'unused' child microservice.
            # If all are used, choose a 'used' child microservice randomly.
            curr_child_address_product = child_addresses_product['unused'].pop(0) if child_addresses_product[
                'unused'] else random.choice(child_addresses_product['used'])
            if curr_child_address_product not in child_addresses_product['used']:
                child_addresses_product['used'].append(curr_child_address_product)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][1][
                'value'] = curr_child_address_product

            curr_child_address_currency = child_addresses_currency['unused'].pop(0) if child_addresses_currency[
                'unused'] else random.choice(child_addresses_currency['used'])
            if curr_child_address_currency not in child_addresses_currency['used']:
                child_addresses_currency['used'].append(curr_child_address_currency)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][2][
                'value'] = curr_child_address_currency

            curr_child_address_cart = child_addresses_cart['unused'].pop(0) if child_addresses_cart[
                'unused'] else random.choice(child_addresses_cart['used'])
            if curr_child_address_cart not in child_addresses_cart['used']:
                child_addresses_cart['used'].append(curr_child_address_cart)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][3][
                'value'] = curr_child_address_cart

            curr_child_address_recommend = child_addresses_recommend['unused'].pop(0) if child_addresses_recommend[
                'unused'] else random.choice(child_addresses_recommend['used'])
            if curr_child_address_recommend not in child_addresses_recommend['used']:
                child_addresses_recommend['used'].append(curr_child_address_recommend)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][4][
                'value'] = curr_child_address_recommend

            curr_child_address_shipping = child_addresses_shipping['unused'].pop(0) if child_addresses_shipping[
                'unused'] else random.choice(child_addresses_shipping['used'])
            if curr_child_address_shipping not in child_addresses_shipping['used']:
                child_addresses_shipping['used'].append(curr_child_address_shipping)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][5][
                'value'] = curr_child_address_shipping

            curr_child_address_checkout = child_addresses_checkout['unused'].pop(0) if child_addresses_checkout[
                'unused'] else random.choice(child_addresses_checkout['used'])
            if curr_child_address_checkout not in child_addresses_checkout['used']:
                child_addresses_checkout['used'].append(curr_child_address_checkout)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][6][
                'value'] = curr_child_address_checkout

            curr_child_address_ad = child_addresses_ad['unused'].pop(0) if child_addresses_ad[
                'unused'] else random.choice(child_addresses_ad['used'])
            if curr_child_address_ad not in child_addresses_ad['used']:
                child_addresses_ad['used'].append(curr_child_address_ad)
            frontend_deploy['spec']['template']['spec']['containers'][0]['env'][7][
                'value'] = curr_child_address_ad

            yaml.dump(frontend_deploy, f_out)

    # This is a new parent microservice - update the relations to the chosen child microservices in the relations dictionary.
    child_to_parents_relations[curr_child_address_product].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_currency].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_cart].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_recommend].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_shipping].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_checkout].append(new_frontend_label)
    child_to_parents_relations[curr_child_address_ad].append(new_frontend_label)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(get_path(r'utils\frontend-yamls\frontend-svc-clusterip.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/frontend-apply/frontend-svc-clusterip-{idx}.yaml',
                'w') as f_out:
            frontend_svc_cluster_ip = yaml.load(f_in, Loader=SafeLoader)

            frontend_svc_cluster_ip['metadata']['name'] = new_frontend_label
            frontend_svc_cluster_ip['spec']['selector']['app'] = new_frontend_label
            frontend_svc_cluster_ip['spec']['ports'][0]['port'] = new_frontend_port
            frontend_svc_cluster_ip['spec']['ports'][0]['targetPort'] = new_frontend_port

            yaml.dump(frontend_svc_cluster_ip, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(get_path(r'utils\frontend-yamls\frontend-svc-loadbalancer.yaml'),
              'r') as f_in:
        with open(
                f'yamls-to-apply/frontend-apply/frontend-svc-loadbalancer-{idx}.yaml',
                'w') as f_out:
            frontend_svc_loadbalancer = yaml.load(f_in, Loader=SafeLoader)

            frontend_svc_loadbalancer['metadata']['name'] = f'frontend-external-{idx}'
            frontend_svc_loadbalancer['spec']['selector']['app'] = new_frontend_label
            frontend_svc_loadbalancer['spec']['ports'][0]['port'] = new_frontend_port
            frontend_svc_loadbalancer['spec']['ports'][0]['targetPort'] = new_frontend_port

            yaml.dump(frontend_svc_loadbalancer, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_frontend_port)

    # Frontend microservice is NOT a child microservice in the application's architecture.
    # child_to_parents_relations[new_frontend_address] = []

    return new_frontend_address
