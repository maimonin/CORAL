import random
from datetime import datetime
import pandas as pd

def parse_remove_dep(x, microservices_to_remove):
    """
    Passes the inbound list and removes microservices_to_remove from it.
    :param x: str: Inbound list.
    :param microservices_to_remove: list: List of microservices to remove.
    :return: list: Inbound list without the microservices to remove.
    """
    ret = []
    l = x.strip('][').split(')')
    l2 = []
    for item in l:
        if item == '':
            continue
        item = item.strip('(')
        item = item.strip(',(')
        item = item.replace(" ", "")
        item = item.replace("'", "")
        split_item = item.strip(')(').split(',')
        if len(split_item) == 3:
            l2.append((split_item[0], int(split_item[1]), split_item[2]))
        else:
            l2.append(split_item[0])
    for item in l2:
        if item[0] not in microservices_to_remove:
            ret.append(item)

    return ret


def remove_microservices(df_full_graph_topology, df_full_graph_cve, microservices_to_remove):
    """
    Remove microservices from the full graph.
    :param df_full_graph_topology: DataFrame: Full graph topology.
    :param df_full_graph_cve: DataFrame: Full graph CVE.
    :param microservices_to_remove: list: List of microservices to remove.
    :return: DataFrame: Sub graph topology.
    :return: DataFrame: Sub graph CVE.
    """
    df_sub_graph_topology = df_full_graph_topology.copy()
    df_sub_graph_cve = df_full_graph_cve.copy()

    # Remove microservices from topology
    df_sub_graph_topology = df_sub_graph_topology[~df_sub_graph_topology['Pod-ID'].isin(microservices_to_remove)]
    df_sub_graph_topology['Pod-Inbound-List'] = df_sub_graph_topology['Pod-Inbound-List'].apply(
        lambda x: parse_remove_dep(x, microservices_to_remove))
    for microservice in df_sub_graph_topology['Pod-ID'].unique():
        df_sub_graph_topology, _ = remove_stale_connections(microservice, df_sub_graph_topology)
    # Remove microservices from CVE
    df_sub_graph_cve = df_sub_graph_cve[~df_sub_graph_cve['Pod-ID'].isin(microservices_to_remove)]
    return df_sub_graph_topology, df_sub_graph_cve


def remove_stale_connections(microservice, df_sub_graph_topology):
    """
    Remove stale connections from the sub graph.
    :param microservice:
    :param df_sub_graph_topology:
    :return: df: Sub graph topology with removed stale connections.
    :return: int: Number of removed stale connections.
    """
    count = 0
    if len(df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == microservice]['Pod-Inbound-List'].values[0]) == 0:
        #  find children
        children = [m for m in list(df_sub_graph_topology['Pod-ID'].unique()) if microservice in
                    [mic[0] for mic in
                     df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == m]['Pod-Inbound-List'].values[0]]]
        #if len(children) != 0:
            #print(f"Removed stale connection from microservice {microservice} to microservices {children}")
        # remove stale connections
        count = len(children)
        df_sub_graph_topology['Pod-Inbound-List'] = df_sub_graph_topology['Pod-Inbound-List'].apply(
            lambda x: [item for item in x if item[0] != microservice])
        # remove stale connections from children
        for child in children:
            df_sub_graph_topology, c = remove_stale_connections(child, df_sub_graph_topology)
            count += c
    return df_sub_graph_topology, count


def remove_connections_random(num_of_connections_to_remove, df_sub_graph_topology):
    """
    Remove connections from the sub graph randomly.
    :param num_of_connections_to_remove: int: Number of connections to remove. might remove more if branches have gone stale.
    :param df_sub_graph_topology: df: Sub graph topology.
    :return: df: Sub graph topology with removed connections.
    """
    i = 0
    while i < num_of_connections_to_remove:
        # Choose random microservice with connections
        microservices = [microservice for microservice in list(df_sub_graph_topology['Pod-ID'].unique()) if len(
            df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == microservice]['Pod-Inbound-List'].values[0]) > 0]
        # don't remove connections from frontend (only connection is Internet)
        microservices = [microservice for microservice in microservices if 'frontend' not in microservice]
        microservice = random.choice(microservices)
        # Choose random connection to remove
        connections_to_remove = random.sample(
            list(df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == microservice]['Pod-Inbound-List'].values[0]),
            1)
        # Remove connection
        df_sub_graph_topology.loc[df_sub_graph_topology['Pod-ID'] == microservice, 'Pod-Inbound-List'] = \
            df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == microservice]['Pod-Inbound-List'].apply(
                lambda x: [item for item in x if item not in connections_to_remove])
        #print(f"Removed connection {connections_to_remove} from microservice {microservice}")
        #  check if microservice has no more connections and remove stale connections
        df_sub_graph_topology, count = remove_stale_connections(microservice, df_sub_graph_topology)
        i += count + 1
    return df_sub_graph_topology


def create_subgraph(subgraph_topology, subgraph_cve):
    now = datetime.now().strftime('%m.%d.%Y_%H.%M.%S')
    if subgraph_topology is None:
        subgraph_topology = f"TopologyBulk/sub_graph_topology_{now}.csv"
    if subgraph_cve is None:
        subgraph_cve = f"TopologyBulk/sub_graph_cve_{now}.csv"

    df_full_graph_topology = pd.read_csv("Topologies/ContainerStaticTopology.csv")
    df_full_graph_cve = pd.read_csv("CVEs/CveList.csv")
    # if None, random number of microservices and connections will be removed
    # example: ['frontend_1', 'adservice_0','frontend_40']
    microservices_to_remove = None  # []
    # dict: key: microservice, value: list of connections to remove
    # example: {'microservice1': [('microservice2', 'tcp', 80), ('microservice3', 'tcp', 443)]}
    connections_to_remove = None  # {'recommendationservice_1':[('frontend_43', 6251, 'TCP')]}
    # for random removal, won't remove more than max_num_of_microservices_to_remove_ratio % of microservices and
    # max_num_of_connections_to_remove_ratio % of left connections
    max_num_of_microservices_to_remove_ratio = 0.02
    max_num_of_connections_to_remove_ratio = 0.02
    print(f"Number of microservices in full graph: {df_full_graph_topology.shape[0]}")
    print(
        f"Number of connections in full graph: {df_full_graph_topology['Pod-Inbound-List'].apply(lambda x: len([i for i in x if i != 'Internet'])).sum()}")
    # choose random microservices to remove
    if microservices_to_remove is None:
        num_of_microservices_to_remove = random.randint(1, int(
            df_full_graph_topology.shape[0] * max_num_of_microservices_to_remove_ratio))
        microservices_to_remove = random.sample(list(df_full_graph_topology['Pod-ID'].unique()),
                                                num_of_microservices_to_remove)
        print(f"Number of microservices to remove: {num_of_microservices_to_remove}")
        print(f"Microservices to remove: {microservices_to_remove}")
    # remove microservices
    df_sub_graph_topology, df_sub_graph_cve = remove_microservices(df_full_graph_topology, df_full_graph_cve,
                                                                   microservices_to_remove)
    # calculate number of connections left
    num_of_connections_left = df_sub_graph_topology['Pod-Inbound-List'].apply(
        lambda x: len([i for i in x if i != 'Internet'])).sum()
    print(f"Number of connections left: {num_of_connections_left}")
    if connections_to_remove is None:
        num_of_connections_to_remove = random.randint(1,
                                                      int(num_of_connections_left * max_num_of_connections_to_remove_ratio))
        print(f"Number of connections to remove: {num_of_connections_to_remove}")
        df_sub_graph_topology = remove_connections_random(num_of_connections_to_remove, df_sub_graph_topology)
    else:
        for microservice, connections in connections_to_remove.items():
            df_sub_graph_topology.loc[df_sub_graph_topology['Pod-ID'] == microservice, 'Pod-Inbound-List'] = \
                df_sub_graph_topology[df_sub_graph_topology['Pod-ID'] == microservice]['Pod-Inbound-List'].apply(
                    lambda x: [item for item in x if item not in connections])
            print(f"Removed connection {connections} from microservice {microservice}")
            # check if microservice has no more connections and remove stale connections
            df_sub_graph_topology, _ = remove_stale_connections(microservice, df_sub_graph_topology)
    # save sub graph
    df_sub_graph_topology.to_csv(subgraph_topology, index=False,
        columns=['Pod-ID', 'IP', 'Pod-Inbound-List', 'Protocol', 'Port'])
    df_sub_graph_cve.to_csv(subgraph_cve, index=False)

    return subgraph_topology, subgraph_cve

if __name__ == "__main__":
    create_subgraph(None, None)
