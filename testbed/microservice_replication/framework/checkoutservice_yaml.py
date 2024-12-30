import yaml
from yaml.loader import SafeLoader
import framework_general_funcs as general_functions
import random


def create_checkoutservice_yamls(idx, used_ports, child_to_parents_relations,
                                 child_addresses_product,
                                 child_addresses_cart,
                                 child_addresses_shipping,
                                 child_addresses_currency,
                                 child_addresses_payment,
                                 child_addresses_email):
    """
    Create new YAML files for new checkoutservice microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.
    This function also uses child microservices addresses for relevant fields in parent checkoutservice microservice's YAMLs
        and updates the child microservices addresses dictionary accordingly.


    :param idx: int: new checkoutservice microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).

    Child microservices addresses parameters:
    :param child_addresses_product: dictionary: used and unused addresses of newly created (YAMLs) productcatalog microservices,
            which are checkoutservice's child microservices.
    :param child_addresses_cart: dictionary: used and unused addresses of newly created (YAMLs) cartservice microservices,
            which are checkoutservice's child microservices.
    :param child_addresses_shipping: dictionary: used and unused addresses of newly created (YAMLs) shippingservice microservices,
            which are checkoutservice's child microservices.
    :param child_addresses_currency: dictionary: used and unused addresses of newly created (YAMLs) currecyservice microservices,
            which are checkoutservice's child microservices.
    :param child_addresses_payment: dictionary: used and unused addresses of newly created (YAMLs) paymentservice microservices,
            which are checkoutservice's child microservices.
    :param child_addresses_email: dictionary: used and unused addresses of newly created (YAMLs) emailservice microservices,
            which are checkoutservice's child microservices.


    :return new checkoutservice microservice's address in the format of label:port.
    """

    new_checkoutservice_port = general_functions.generate_new_port(used_ports)
    new_checkoutservice_label = f"checkoutservice-{idx}"
    new_checkoutservice_address = f"{new_checkoutservice_label}:{new_checkoutservice_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                         r'checkout-yamls\checkoutservice-deploy.yaml'), 'r') as f_in:
        with open(f'yamls-to-apply/checkoutservice-apply/checkoutservice-deploy-{idx}.yaml',
                'w') as f_out:
            checkoutservice_deploy = yaml.load(f_in, Loader=SafeLoader)

            checkoutservice_deploy['metadata']['name'] = new_checkoutservice_label
            checkoutservice_deploy['spec']['selector']['matchLabels']['app'] = new_checkoutservice_label
            checkoutservice_deploy['spec']['template']['metadata']['labels']['app'] = new_checkoutservice_label
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][0]['value'] = str(new_checkoutservice_port)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = new_checkoutservice_port
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['readinessProbe']['exec']['command'][
                1] = f"-addr=:{new_checkoutservice_port}"
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['livenessProbe']['exec']['command'][
                1] = f"-addr=:{new_checkoutservice_port}"
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][0][
                'value'] = f'{new_checkoutservice_port}'

            # Choose a child microservice for the new microservice created and update environment variables.
            # First, look for an 'unused' child microservice.
            # If all are used, choose a 'used' child microservice randomly.
            curr_child_address_product = child_addresses_product['unused'].pop(0) if child_addresses_product[
                'unused'] else random.choice(child_addresses_product['used'])
            if curr_child_address_product not in child_addresses_product['used']:
                child_addresses_product['used'].append(curr_child_address_product)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][1][
                'value'] = curr_child_address_product

            curr_child_address_shipping = child_addresses_shipping['unused'].pop(0) if child_addresses_shipping[
                'unused'] else random.choice(child_addresses_shipping['used'])
            if curr_child_address_shipping not in child_addresses_shipping['used']:
                child_addresses_shipping['used'].append(curr_child_address_shipping)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][2][
                'value'] = curr_child_address_shipping

            curr_child_address_payment = child_addresses_payment['unused'].pop(0) if child_addresses_payment[
                'unused'] else random.choice(child_addresses_payment['used'])
            if curr_child_address_payment not in child_addresses_payment['used']:
                child_addresses_payment['used'].append(curr_child_address_payment)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][3][
                'value'] = curr_child_address_payment

            curr_child_address_email = child_addresses_email['unused'].pop(0) if child_addresses_email[
                'unused'] else random.choice(child_addresses_email['used'])
            if curr_child_address_email not in child_addresses_email['used']:
                child_addresses_email['used'].append(curr_child_address_email)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][4][
                'value'] = curr_child_address_email

            curr_child_address_currency = child_addresses_currency['unused'].pop(0) if child_addresses_currency[
                'unused'] else random.choice(child_addresses_currency['used'])
            if curr_child_address_currency not in child_addresses_currency['used']:
                child_addresses_currency['used'].append(curr_child_address_currency)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][5][
                'value'] = curr_child_address_currency

            curr_child_address_cart = child_addresses_cart['unused'].pop(0) if child_addresses_cart[
                'unused'] else random.choice(child_addresses_cart['used'])
            if curr_child_address_cart not in child_addresses_cart['used']:
                child_addresses_cart['used'].append(curr_child_address_cart)
            checkoutservice_deploy['spec']['template']['spec']['containers'][0]['env'][6][
                'value'] = curr_child_address_cart

            yaml.dump(checkoutservice_deploy, f_out)

    # This is a new parent microservice - update the relations to the chosen child microservices in the relations dictionary.
    child_to_parents_relations[curr_child_address_product].append(new_checkoutservice_label)
    child_to_parents_relations[curr_child_address_shipping].append(new_checkoutservice_label)
    child_to_parents_relations[curr_child_address_payment].append(new_checkoutservice_label)
    child_to_parents_relations[curr_child_address_email].append(new_checkoutservice_label)
    child_to_parents_relations[curr_child_address_currency].append(new_checkoutservice_label)
    child_to_parents_relations[curr_child_address_cart].append(new_checkoutservice_label)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(general_functions.get_path(r'..\..\google-microservices-demo\deploy_and_svc_yamls',
                                         'checkout-yamls\checkoutservice-svc.yaml'),
              'r') as f_in:
        with open(f'yamls-to-apply/checkoutservice-apply/checkoutservice-svc-{idx}.yaml',
                'w') as f_out:
            checkoutservice_svc = yaml.load(f_in, Loader=SafeLoader)

            checkoutservice_svc['metadata']['name'] = new_checkoutservice_label
            checkoutservice_svc['spec']['selector']['app'] = new_checkoutservice_label
            checkoutservice_svc['spec']['ports'][0]['port'] = new_checkoutservice_port
            checkoutservice_svc['spec']['ports'][0]['targetPort'] = new_checkoutservice_port

            yaml.dump(checkoutservice_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(new_checkoutservice_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_checkoutservice_address] = []

    return new_checkoutservice_address
