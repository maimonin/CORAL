import random
from utils import general_functions
from services_creators.frontend_yaml import *
from services_creators.adservice_yaml import *
from services_creators.productcatalogservice_yaml import *
from services_creators.recommendationservice_yaml import *
from services_creators.checkoutservice_yaml import *
from services_creators.shippingservice_yaml import *
from services_creators.currencyservice_yaml import *
from services_creators.paymentservice_yaml import *
from services_creators.emailservice_yaml import *
from services_creators.networkpolicis_yaml_separate_files import *


def validate(replications_dict):
    """
    Validate the replications' dictionary so that there are no more "child" microservices than their "parent" microservices.
    :param: replications_dict: dictionary: containing how many replications to create for each microservice.
    :raises: Exception: if there are more child microservices than parent microservices.
    """

    # Parent microservice - recommendationservice
    if 'productcatalogservice' in replications_dict and replications_dict['productcatalogservice'] > replications_dict[
        'recommendationservice']:
        raise Exception(
            "Number of productcatalogservice (child) pods greater than number of recommendationservice (parent) pods")

    # Parent microservice - cartservice
    if 'redis-cart' in replications_dict and replications_dict['redis-cart'] > replications_dict['cartservice']:
        raise Exception("Number of redis-cart (child) pods greater than number of cartservice (parent) pods")

    # Parent microserivce - checkoutservice
    if 'productcatalogservice' in replications_dict and replications_dict['productcatalogservice'] > replications_dict[
        'checkoutservice']:
        raise Exception(
            "Number of productcatalogservice (child) pods greater than number of checkoutservice (parent) pods")
    if 'cartservice' in replications_dict and replications_dict['cartservice'] > replications_dict['checkoutservice']:
        raise Exception("Number of cartservice (child) pods greater than number of checkoutservice (parent) pods")
    if 'shippingservice' in replications_dict and replications_dict['shippingservice'] > replications_dict[
        'checkoutservice']:
        raise Exception("Number of shippingservice (child) pods greater than number of checkoutservice (parent) pods")
    if 'currencyservice' in replications_dict and replications_dict['currencyservice'] > replications_dict[
        'checkoutservice']:
        raise Exception("Number of currencyservice (child) pods greater than number of checkoutservice (parent) pods")
    if 'paymentservice' in replications_dict and replications_dict['paymentservice'] > replications_dict[
        'checkoutservice']:
        raise Exception("Number of paymentservice (child) pods greater than number of checkoutservice (parent) pods")
    if 'emailservice' in replications_dict and replications_dict['emailservice'] > replications_dict['checkoutservice']:
        raise Exception("Number of emailservice (child) pods greater than number of checkoutservice (parent) pods")

    # Parent microservice - frontend
    if 'adservice' in replications_dict and replications_dict['adservice'] > replications_dict['frontend']:
        raise Exception("Number of adservice (child) pods greater than number of frontend (parent) pods")
    if 'recommendationservice' in replications_dict and replications_dict['recommendationservice'] > \
            replications_dict[
                'frontend']:
        raise Exception("Number of recommendationservice (child) pods greater than number of frontend (parent) pods")
    if 'productcatalogservice' in replications_dict and replications_dict['productcatalogservice'] > \
            replications_dict[
                'frontend']:
        raise Exception("Number of productcatalogservice (child) pods greater than number of frontend (parent) pods")
    if 'cartservice' in replications_dict and replications_dict['cartservice'] > replications_dict['frontend']:
        raise Exception("Number of cartservice (child) pods greater than number of frontend (parent) pods")
    if 'checkoutservice' in replications_dict and replications_dict['checkoutservice'] > replications_dict[
        'frontend']:
        raise Exception("Number of checkoutservice (child) pods greater than number of frontend (parent) pods")
    if 'shippingservice' in replications_dict and replications_dict['shippingservice'] > replications_dict[
        'frontend']:
        raise Exception("Number of shippingservice (child) pods greater than number of frontend (parent) pods")
    if 'currencyservice' in replications_dict and replications_dict['currencyservice'] > replications_dict[
        'frontend']:
        raise Exception("Number of currencyservice (child) pods greater than number of frontend (parent) pods")


def add_frontend(num_replicates,
                 adservice_addresses,
                 recommendationservice_addresses,
                 producatcatalogservice_addresses,
                 cartservice_addresses,
                 checkoutservice_addresses,
                 shippingservice_addresses,
                 currecyservice_addresses):
    """
    Create (num_replicates) X new frontend microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new frontend services.
    This function also receives child microservices' addresses, in order to write them to the parent microservice's (frontend) YAMLs.
    :param num_replicates: int: number of replicates to create of frontend microservice.
    :param adservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) adservice microservices,
            which are frontend's child microservices.
    :param recommendationservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) recommendationservice microservices,
            which are frontend's child microservices.
    :param producatcatalogservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) productcatalog microservices,
            which are frontend's child microservices.
    :param cartservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) cartservice microservices,
            which are frontend's child microservices.
    :param checkoutservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) checkoutservice microservices,
            which are frontend's child microservices.
    :param shippingservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) shippingservice microservices,
            which are frontend's child microservices.
    :param currecyservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) currecyservice microservices,
            which are frontend's child microservices.
    :return frontend_addresess dictionary: containing newly created frontend's microservices' addresses.
    """
    frontend_addresess = {"unused": [],
                          "used": []}

    for i in range(1, num_replicates + 1):
        new_frontend_address = create_frontend_yamls(idx=i, used_ports=used_ports,
                                                     child_to_parents_relations=child_to_parents_relations,
                                                     child_addresses_ad=adservice_addresses,
                                                     child_addresses_recommend=recommendationservice_addresses,
                                                     child_addresses_product=producatcatalogservice_addresses,
                                                     child_addresses_cart=cartservice_addresses,
                                                     child_addresses_checkout=checkoutservice_addresses,
                                                     child_addresses_shipping=shippingservice_addresses,
                                                     child_addresses_currency=currecyservice_addresses)
        frontend_addresess['unused'].append(new_frontend_address)

    return frontend_addresess


def add_adservice(num_replicates):
    """
    Create (num_replicates) X new adservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new adservice services.
    :param: num_replicates: int: number of replicates to create of adservice microservice.
    :return: adservice_addresess dictionary: containing newly created adservice's microservices' addresses.
    """
    adservice_addresses = {"unused": [],
                           "used": []}

    for i in range(1, num_replicates + 1):
        new_adservice_address = create_adservice_yamls(idx=i, used_ports=used_ports,
                                                       child_to_parents_relations=child_to_parents_relations)
        adservice_addresses['unused'].append(new_adservice_address)

    return adservice_addresses


def add_productcatalogservice(num_replicates):
    """
    Create (num_replicates) X new productcatalogservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new productcatalogservice services.
    :param: num_replicates: int: number of replicates to create of productcatalogservice microservice.
    :return: productcatalogservice_addresess dictionary: containing newly created productcatalogservice's microservices' addresses.
    """
    productcatalogservice_addresses = {"unused": [],
                                       "used": []}

    for i in range(1, num_replicates + 1):
        new_productcatalogservice_address = create_productcatalogservice_yamls(idx=i, used_ports=used_ports,
                                                                               child_to_parents_relations=child_to_parents_relations)
        productcatalogservice_addresses['unused'].append(new_productcatalogservice_address)

    return productcatalogservice_addresses


def add_recommendationservice(num_replicates, producatcatalogservice_addresses):
    """
    Create (num_replicates) X new recommendationservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new recommendationservice services.
    This function also receives child microservices addresses', in order to write them to the parent microservice's (recommendationservice) YAMLs.
    :param num_replicates: int: number of replicates to create of recommendationservice microservice.
    :param producatcatalogservice_addresses: dictionary: used and unused addresess of newly created (YAMLs) productcatalog microservices,
            which are recommendationservices' child microservices.
    :return: recommendationservice_addresess: dictionary: containing newly created recommendationservice's microservices' addresses.
    """
    recommendationservice_addresses = {"unused": [],
                                       "used": []}

    for i in range(1, num_replicates + 1):
        new_recommendationservice_address = create_recommendationservice_yamls(idx=i, used_ports=used_ports,
                                                                               child_to_parents_relations=child_to_parents_relations,
                                                                               child_addresses_product=producatcatalogservice_addresses)
        recommendationservice_addresses['unused'].append(new_recommendationservice_address)

    return recommendationservice_addresses



def add_checkoutservice(num_replicates, producatcatalogservice_addresses, cartservice_addresses,
                        shippingservice_addresses,
                        currecyservice_addresses, paymentservice_addresses, emailservice_addresses):
    """
    Create (num_replicates) X new checkoutservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new checkoutservice services.
    This function also receives child microservices addresses', in order to write them to the parent microservice's (checkoutservice) YAMLs.
    :param num_replicates: int: number of replicates to create of checkoutservice microservice.
    :param producatcatalogservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) productcatalog microservices,
            which are checkoutservice's child microservices.
    :param cartservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) cartservice microservices,
            which are checkoutservice's child microservices.
    :param shippingservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) shippingservice microservices,
            which are checkoutservice's child microservices.
    :param currecyservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) currecyservice microservices,
            which are checkoutservice's child microservices.
    :param paymentservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) paymentservice microservices,
            which are checkoutservice's child microservices.
    :param emailservice_addresses: dictionary: used and unused addresses of newly created (YAMLs) emailservice microservices,
            which are checkoutservice's child microservices.
    :return: checkoutservice_addresses: dictionary: containing newly created checkoutservice's microservices' addresses.
    """
    checkoutservice_addresses = {"unused": [],
                                 "used": []}

    for i in range(1, num_replicates + 1):
        new_checkout_address = create_checkoutservice_yamls(idx=i, used_ports=used_ports,
                                                            child_to_parents_relations=child_to_parents_relations,
                                                            child_addresses_product=producatcatalogservice_addresses,
                                                            child_addresses_cart=cartservice_addresses,
                                                            child_addresses_shipping=shippingservice_addresses,
                                                            child_addresses_currency=currecyservice_addresses,
                                                            child_addresses_payment=paymentservice_addresses,
                                                            child_addresses_email=emailservice_addresses)
        checkoutservice_addresses['unused'].append(new_checkout_address)

    return checkoutservice_addresses


def add_shippingservice(num_replicates):
    """
    Create (num_replicates) X new shippingservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new shippingservice services.
    :param: num_replicates: int: number of replicates to create of shippingservice microservice.
    :return: shippingservice_addresess dictionary: containing newly created shippingservice's microservices' addresses.
    """
    shippingservice_addresses = {"unused": [],
                                 "used": []}

    for i in range(1, num_replicates + 1):
        new_shippingservice_address = create_shippingservice_yamls(idx=i, used_ports=used_ports,
                                                                   child_to_parents_relations=child_to_parents_relations)
        shippingservice_addresses['unused'].append(new_shippingservice_address)

    return shippingservice_addresses


def add_currencyservice(num_replicates):
    """
    Create (num_replicates) X new currencyservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new currencyservice services.
    :param: num_replicates: int: number of replicates to create of currencyservice microservice.
    :return: currencyservice_addresess dictionary: containing newly created currencyservice's microservices' addresses.
    """
    currencyservice_addresess = {"unused": [],
                                 "used": []}

    for i in range(1, num_replicates + 1):
        new_currencyservice_address = create_currencyservice_yamls(idx=i, used_ports=used_ports,
                                                                   child_to_parents_relations=child_to_parents_relations)
        currencyservice_addresess['unused'].append(new_currencyservice_address)

    return currencyservice_addresess


def add_paymentservice(num_replicates):
    """
    Create (num_replicates) X new paymentservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new paymentservice services.
    :param: num_replicates: int: number of replicates to create of paymentservice microservice.
    :return: paymentservice_addresess dictionary: containing newly created paymentservice's microservices' addresses.
    """
    paymentservice_addresess = {"unused": [],
                                "used": []}

    for i in range(1, num_replicates + 1):
        new_paymentservice_address = create_paymentservice_yamls(idx=i, used_ports=used_ports,
                                                                 child_to_parents_relations=child_to_parents_relations)
        paymentservice_addresess['unused'].append(new_paymentservice_address)

    return paymentservice_addresess


def add_emailservice(num_replicates):
    """
    Create (num_replicates) X new emailservice microservices YAMLs.
    Also updates used_ports list with the new ports allocated to the new emailservice services.
    :param: num_replicates: int: number of replicates to create of emailservice microservice.
    :return: emailservice_addresess dictionary: containing newly created emailservice's microservices' addresses.
    """
    emailservice_addresess = {"unused": [],
                              "used": []}

    for i in range(1, num_replicates + 1):
        new_emailservice_address = create_emailservice_yamls(idx=i, used_ports=used_ports,
                                                             child_to_parents_relations=child_to_parents_relations)
        emailservice_addresess['unused'].append(new_emailservice_address)

    return emailservice_addresess


def replicate_microservices(replications_dict):
    """
    This function calls to each "add_microservice" function with the matching number of replications to create of the specific microservice.
    Before, calls validate to make sure the input is valid (no more child microservices than parent microservices).
    :param replications_dict: dictionary: containing how many replications to create for each microservice.
    """
    validate(replications_dict)

    ad_addresses = add_adservice(replications_dict['adservice'])
    productcatalog_addresses = add_productcatalogservice(replications_dict['productcatalogservice'])
    recommendation_addresses = add_recommendationservice(num_replicates=replications_dict['recommendationservice'],
                                                         producatcatalogservice_addresses=productcatalog_addresses)

    '''# cartservice and redis-cart are single, hard-coded microservices as they do not have a port environment variable,
    # and therefore cannot be replicated.'''
    general_functions.copy_files(source_folder=general_functions.get_path(r'utils/hard-coded-yamls/redis-cart-yamls'),
                                 destination_folder=general_functions.get_path(r'framework/yamls-to-apply/redis-cart-apply'))
    general_functions.copy_files(source_folder=general_functions.get_path(r'utils/hard-coded-yamls/cartservice-yamls'),
                                 destination_folder=general_functions.get_path(r'framework/yamls-to-apply/cartservice-apply'))
    # Update addresses and relations dictionaries.
    redis_cart_addresses = {'unused': ['redis-cart-1:6379'],
                            'used': []}
    cart_addresses = {'unused': ['cartservice-1:7070'],
                      'used': []}
    child_to_parents_relations['redis-cart-1:6379'] = ['cartservice-1']
    child_to_parents_relations['cartservice-1:7070'] = []

    shipping_addresses = add_shippingservice(replications_dict['shippingservice'])

    currency_addresses = add_currencyservice(replications_dict['currencyservice'])
    payment_addresses = add_paymentservice(replications_dict['paymentservice'])
    email_addresses = add_emailservice(replications_dict['emailservice'])
    checkout_addresses = add_checkoutservice(num_replicates=replications_dict['checkoutservice'],
                                             producatcatalogservice_addresses=productcatalog_addresses,
                                             cartservice_addresses=cart_addresses,
                                             shippingservice_addresses=shipping_addresses,
                                             currecyservice_addresses=currency_addresses,
                                             paymentservice_addresses=payment_addresses,
                                             emailservice_addresses=email_addresses)

    frontend_addresses = add_frontend(num_replicates=replications_dict['frontend'],
                                      adservice_addresses=ad_addresses,
                                      recommendationservice_addresses=recommendation_addresses,
                                      producatcatalogservice_addresses=productcatalog_addresses,
                                      cartservice_addresses=cart_addresses,
                                      checkoutservice_addresses=checkout_addresses,
                                      shippingservice_addresses=shipping_addresses,
                                      currecyservice_addresses=currency_addresses)


def generate_networkpolicies(child_to_parents_relations):
    """
    This function iterates through the child_to_parents_relations dictionary
    and for each child microservices creates network policies according to each parent microservice.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
            to what parent microservices it is linked (value, list of parent microservices).
    """

    for relation in child_to_parents_relations.items():
        # Create network policies only for microservices that have parents.
        if len(relation[1]) > 0:
            create_networkpolicy_seperate_files(child_address=relation[0], parents_ms_list=relation[1])


if __name__ == "__main__":
    global used_ports
    global config_client_api
    global child_to_parents_relations
    config_client_api = general_functions.config_api()
    used_ports = []
    child_to_parents_relations = {}

    rep_dict = {'adservice': 4,
            'productcatalogservice': 3,
            'recommendationservice': 4,
            'redis-cart': 1,
            'cartservice': 1,
            'shippingservice': 3,
            'currencyservice': 3,
            'paymentservice': 3,
            'emailservice': 3,
            'checkoutservice': 4,
            'frontend': 5}


    replicate_microservices(rep_dict)

    generate_networkpolicies(child_to_parents_relations)
