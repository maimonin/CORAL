import yaml
from yaml.loader import SafeLoader


def create_redis_cart_yamls(idx, used_ports, child_to_parents_relations):
    """
    Create new YAML files for new redis-cart microservice to be added to the cluster.
    YAML files created for new microservice include:
        Deployment YAML,
        Service YAML (1) - ClusterIP.

    :param idx: int: new redis-cart microservice's index.
    :param used_ports: list: list of currently used_ports in cluster.
    :param child_to_parents_relations: dictionary: lists for each child microservices (key) created during factory,
                to what parent microservices it is linked (value, list of parent microservices).

    :return new redis-cart microservice's address in the format of label:port.
    """

    redis_cart_port = 6379
    new_redis_cart_label = f"redis-cart-{idx}"
    new_redis_cart_address = f"{new_redis_cart_label}:{redis_cart_port}"

    # Read deployment YAML file template, and rewrite needed fields in order to create a new deployment YAML file
    # for the new microservice to be added.
    with open(r'../../google-microservices-demo/deploy_and_svc_yamls/redis-cart-yamls/redis-cart-deploy.yaml',
              'r') as f_in:
        with open(
                f'/yamls-to-apply/redis-cart-apply/redis-cart-deploy-{idx}.yaml',
                'w') as f_out:
            redis_cart_deploy = yaml.load(f_in, Loader=SafeLoader)

            redis_cart_deploy['metadata']['name'] = new_redis_cart_label
            redis_cart_deploy['spec']['selector']['matchLabels']['app'] = new_redis_cart_label
            redis_cart_deploy['spec']['template']['metadata']['labels']['app'] = new_redis_cart_label

            yaml.dump(redis_cart_deploy, f_out)

    # Read service YAML file template, and rewrite needed fields in order to create a new service YAML file for the
    # new microservice to be added.
    with open(r'../../google-microservices-demo/deploy_and_svc_yamls/redis-cart-yamls/redis-cart-svc.yaml', 'r') as f_in:
        with open(f'yamls-to-apply/redis-cart-apply/redis-cart-svc-{idx}.yaml', 'w') as f_out:
            redis_cart_svc = yaml.load(f_in, Loader=SafeLoader)

            redis_cart_svc['metadata']['name'] = new_redis_cart_label
            redis_cart_svc['spec']['selector']['app'] = new_redis_cart_label
            # Only change "outside" port (no need to change targetPort - which is the target port inside the container).
            redis_cart_svc['spec']['ports'][0]['port'] = redis_cart_port
            # redis_cart_svc['spec']['ports'][0]['targetPort'] = new_redis_cart_port

            yaml.dump(redis_cart_svc, f_out)

    # Add new microservice's service resource port to used ports list.
    used_ports.append(redis_cart_port)

    # This is a new child microservice - add it to relations dictionary.
    child_to_parents_relations[new_redis_cart_address] = []

    return new_redis_cart_address
