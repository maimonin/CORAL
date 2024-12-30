import array
import os
import csv
import sys
import getopt
import ast
import networkx as nx
import json
import numpy
from collections import namedtuple
import matplotlib.pyplot as plt
import graphviz
from math import *
from os import listdir
from os.path import isfile, join
import time
import create_sub_graph
from karateclub import Graph2Vec

DEBUG = False
Internet = "Internet"
dfFileName = "TopologyGraphsAndAG.json"
agFilesDir = "AttackGraphs"
NVDPATH = "nvd_json_files"
Unknown = "Unknown"

def printDebug(debugMessage):
    if DEBUG:
        print(debugMessage)

# Read given CSV file and create a directed graph
def readGraph(containerTopologyFile):
    # File format: Pod-ID,IP,Pod-Inbound-List,Protocol,Port.
    # Pod-Inbound-List is the list of pods communicating with PodName, in which port and with which protocol
    if not os.path.isfile(containerTopologyFile):  # File does not exist
        print(f"File {containerTopologyFile} does not exist")
        raise Exception()

    containerGraph = nx.DiGraph()
    csvinf = open(containerTopologyFile, 'r')
    csvin = csv.reader(csvinf, delimiter=',')
    for row in csvin:
        # Jump over empty lines, lines without inbound and title line
        if len(row) <= 2 or row[0] == 'Pod-ID' or row[2] == '':
            continue
        # podName = stripPodName(row[0].strip())  # Use stripPodName() for pod names such as 'frontend-5fc5754db6-f5h6c'
        podName = row[0].strip()
        if row[2].strip() == "[Internet]" or row[2].strip() == "['Internet']":
            podInbound = Internet
        else:
            podInbound = ast.literal_eval(row[2].strip())
        printDebug("Node Name: " + podName)
        if not containerGraph.has_node(podName):  # If this is a new node, add it
            containerGraph.add_node(podName, LOW=0, MEDIUM=0, HIGH=0, CRITICAL=0, UNKNOWN=0, Score=0, Network=0)

        # Handle node's inbound, which are between []
        printDebug("Going to handle inbound nodes of " + podName)
        printDebug("Node's Children: " + str(podInbound))
        if podInbound == Internet:
            if not containerGraph.has_node(Internet):  # If this is a new node, add it
                containerGraph.add_node(Internet, LOW=0, MEDIUM=0, HIGH=0, CRITICAL=0, UNKNOWN=0, Score=0, Network=0)
            containerGraph.add_edge(Internet, podName)  # Add edge
        else:
            for child in podInbound:
                # childName = stripPodName(child[0])
                childName = child[0].strip()
                childPort = child[1]
                childProtocol = child[2]
                printDebug("Node Name: " + childName)
                if not containerGraph.has_node(childName):  # If this is a new node, add it
                    containerGraph.add_node(childName, LOW=0, MEDIUM=0, HIGH=0, CRITICAL=0, UNKNOWN=0, Score=0, Network=0)
                containerGraph.add_edge(childName, podName, port=childPort, protocol=childProtocol)  # Add edge

    csvinf.close()
    return containerGraph

# Create MulVAL (container) model (interaction rules) for the given graph
def createContainersModel(containerGraph, cveFile, filePathToCreate):
    fileStream = open(filePathToCreate, "w")
    fileStream.write("attackGoal(vulnerablePod(Pod)).\n\n")
    for edge in containerGraph.edges(data=True):
        if edge[0] == Internet:
            fileStream.write("hacl('{}', {}, 'HTTP', '80').\n".format(
                Internet, edge[1].replace('.', '_').replace('-', '_')))
            continue
        # Create 'dataFlow' interaction rule for each edge
        # Replace '.', '-', ',', and ':' with '_', since MulVAL doesn't like them in names and constants
        protocol = edge[2]['protocol']
        port = edge[2]['port']
        fileStream.write("dataFlow({}, {}, '{}', '{}').\n".format(
            edge[0].replace('.', '_').replace('-', '_'), edge[1].replace('.', '_').replace('-', '_'), protocol, port))
    fileStream.write("\n")

    # Read CVE file and create 'residesOn' and 'vulExists' interaction rules
    if not os.path.isfile(cveFile):  # File does not exist
        print(f"File {cveFile} does not exist")
        raise Exception()

    # The loading of all the NVD CVE files takes a lot of time, so we use only the params in the given CVE file
    # cveDict = loadCves()
    # printDebug("CVEs are loaded")

    # CVE file format: Pod-ID,Software,Version,CVE-ID,CVE-Severity,CVE-Data
    csvinf = open(cveFile, 'r')
    csvin = csv.reader(csvinf, delimiter=',')
    for row in csvin:
        # Jump over empty lines, lines with too few parameters and title line
        if len(row) <= 6 or row[0] == 'Pod-ID':
            continue
        printDebug("Row to process: " + str(row))
        if row[0].strip() not in containerGraph.nodes:
            printDebug(f"{row[0]} not in the graph nodes, ignoring")
            continue
        podName = row[0].strip().replace('.', '_').replace('-', '_')
        software = row[1].strip().replace('.', '_').replace('-', '_').replace(':', '_').replace('/', '_')
        version = row[2].strip().replace('.', '_').replace('-', '_').replace(':', '_')
        cveId = row[3].strip()
        cveSeverity = row[4].strip()
        # cveTitle = row[5].strip()
        cvss = row[6].strip()
        accessVector, loseTypes = getCveParams(cvss)

        # If a constant starts with a number, MulVAL doesn’t like letters inside, so we wrap version with ''
        # MulVAL doesn’t like ‘/’ in constants, so we wrap software name with ‘’
        fileStream.write("residesOn({}, '{}', '{}').\n".format(podName, software, version))
        predicate = "vulExists('{}', '{}', '{}', '{}', '{}', '{}').\n".format(
            cveId, software, version, accessVector, loseTypes, cveSeverity)
        fileStream.write(predicate)

    csvinf.close()
    fileStream.close()

# Load the CVEs into dictionary (hash table) to enable fast search of CVEs' complementary parameters
def loadCves():
    # Build the list of NVD CVE Files to process
    nvdFiles = [file for file in listdir(NVDPATH) if isfile(join(NVDPATH, file))]
    printDebug(nvdFiles)

    cveDict = dict()
    for file in nvdFiles:
        jsonFile = open(join(NVDPATH, file), encoding='utf-8')
        try:
            jsonObject = json.load(jsonFile)
        except:
            print(f"Could not load {file} file.")
            continue
        for cve_item in jsonObject['CVE_Items']:
            if 'baseMetricV2' not in cve_item['impact']:
                continue
            # Get CVE-ID
            cveId = cve_item['cve']['CVE_data_meta']['ID']
            # Get severity level
            severity = cve_item['impact']['baseMetricV2']['severity']
            # get access vector
            accessVector = cve_item['impact']['baseMetricV2']['cvssV2']['accessVector']
            # Get CIA impact
            availability_loss = cve_item['impact']['baseMetricV2']['cvssV2']['availabilityImpact']
            data_loss = cve_item['impact']['baseMetricV2']['cvssV2']['confidentialityImpact']
            integrity_loss = cve_item['impact']['baseMetricV2']['cvssV2']['integrityImpact']
            ciaImpact = ""
            if availability_loss != "NONE":
                ciaImpact += "availability_loss,"
            elif data_loss != "NONE":
                ciaImpact += "data_loss,"
            elif integrity_loss != "NONE":
                ciaImpact += "data_modification,"

            if ciaImpact == "":
                ciaImpact = Unknown
            else:
                ciaImpact = ciaImpact[:-1]  # Remove last comma

            printDebug("CVE-ID: {}, Access Vector: {}, CIA Impact: {}, Severity: {}".format(
                cveId, accessVector, ciaImpact, severity))
            cveDict[cveId] = {"AccessVector": accessVector, "CiaImpact": ciaImpact, "Severity": severity}

    return cveDict

# For the given CVE return complementary parameters
def getCveParamsFromDict(cveDict, cveID):
    if cveID not in cveDict:
        return Unknown, Unknown, Unknown
    accessVector = cveDict[cveID]["AccessVector"]
    ciaImpact = cveDict[cveID]["CiaImpact"]
    severity = cveDict[cveID]["Severity"]
    return accessVector, ciaImpact, severity

# Find access vector and CIA impact from the given CVSS vector
def getCveParams(cvss):
    if "V3Vector" in cvss:
        vectorIndex = cvss.find("V3Vector")
    elif "V2Vector" in cvss:
        vectorIndex = cvss.find("V2Vector")
    else:
        return Unknown, Unknown

    accessVector = Unknown
    attackVectorIndex = cvss.find("AV:", vectorIndex)
    attackVectorLetter = cvss[attackVectorIndex + 3:attackVectorIndex + 4]
    match attackVectorLetter:
        case 'N':
            accessVector = "Network"
        case 'A':
            accessVector = "AdjacentNetwork"
        case 'L':
            accessVector = "Local"
        case 'P':
            accessVector = "Physical"

    confidentialityIndex = cvss.find("/C:", vectorIndex)
    confidentialityLetter = cvss[confidentialityIndex + 3:confidentialityIndex + 4]
    integrityLetter = cvss[confidentialityIndex + 7:confidentialityIndex + 8]
    availabilityLetter = cvss[confidentialityIndex + 11:confidentialityIndex + 12]
    ciaImpact = ""
    if confidentialityLetter != 'N':  # Not None
        ciaImpact += "C"
    if integrityLetter != 'N':  # Not None
        ciaImpact += "I"
    if availabilityLetter != 'N':  # Not None
        ciaImpact += "A"

    if ciaImpact == "":
        ciaImpact = Unknown
    else:
        ciaImpact = ciaImpact + "_loss"

    return accessVector, ciaImpact

# Compare between the two given graphs and return Graph Edit Distance (GED)
def findGed(containerGraph, containerGraphModified):
    ged = 1000
    distances = nx.optimize_edit_paths(containerGraph, containerGraphModified, upper_bound=50, timeout=10)
    for distance in distances:
        if distance[2] < ged:
            ged = distance[2]
    # _, ged = nx.optimal_edit_paths(containerGraph, containerGraphModified, upper_bound=50)
    return ged

# Compare between the two given graphs and return Jaccard similarity
def compareGraphs(containerGraph1, containerGraph2):
    """ This version is more clear but much slower
    intersection = 0
    notIntersection = 0
    for node1 in containerGraph1.nodes():
        found = False
        for node2 in containerGraph2.nodes():
            if node1 == node2:
                intersection += 1
                found = True
                break
        if not found:
            notIntersection += 1
    nodeSimilarity = intersection / (len(containerGraph2.nodes()) + notIntersection)

    intersection = 0
    notIntersection = 0
    for edge1 in containerGraph1.edges():
        found = False
        for edge2 in containerGraph2.edges():
            if edge1 == edge2:
                intersection += 1
                found = True
                break
        if not found:
            notIntersection += 1
    edgeSimilarity = intersection / (len(containerGraph2.edges()) + notIntersection)
    """

    intersectionCardinality = len(set.intersection(*[set(containerGraph1.nodes()), set(containerGraph2.nodes())]))
    unionCardinality = len(set.union(*[set(containerGraph1.nodes()), set(containerGraph2.nodes())]))
    nodeSimilarity = intersectionCardinality / float(unionCardinality)

    intersectionCardinality = len(set.intersection(*[set(containerGraph1.edges()), set(containerGraph2.edges())]))
    unionCardinality = len(set.union(*[set(containerGraph1.edges()), set(containerGraph2.edges())]))
    edgeSimilarity = intersectionCardinality / float(unionCardinality)

    return (nodeSimilarity + edgeSimilarity) / 2

# Replicate the given topology graph by converting node names to numbers starting from zero
# This is a mandatory requirement for Karate Club package for calculating embedding vector
def replicateGraphForEmbedding(containerGraph):
    nodeIndex = 0
    nodesDictionary = {}
    for node in containerGraph.nodes:
        nodesDictionary[node] = nodeIndex
        nodeIndex += 1

    newContainerGraph = nx.DiGraph()
    for edge in containerGraph.edges:
        newContainerGraph.add_edge(nodesDictionary[edge[0]], nodesDictionary[edge[1]])

    return newContainerGraph

# Get the (graph2vec) embedding of the given (topology) graph
def getEmbedding(graph):
    graphWithNumberedNodes = replicateGraphForEmbedding(graph)
    numEpochs = max(int(len(graph.nodes) / 7), 10)
    minCount = max(int(len(graph.nodes) / 75), 5)
    learningRate = 0.025 if len(graph.nodes) < 1000 else 0.0025
    model = Graph2Vec(learning_rate=learningRate, epochs=numEpochs, min_count=minCount)
    model.fit([graphWithNumberedNodes])
    embedding = model.get_embedding()
    return embedding

def euclideanDistance(x, y):
    return sqrt(sum(pow(a-b, 2) for a, b in zip(x, y)))

def squareRooted(x):
    return round(sqrt(sum([a*a for a in x])), 3)

def cosineSimilarity(x, y):
    numerator = sum(a*b for a, b in zip(x, y))
    denominator = squareRooted(x) * squareRooted(y)
    return round(numerator / float(denominator), 4)

# Compare between the two given graphs and return Embedding similarity
def compareGraphsWithEmbedding(containerGraph1, containerGraph2):
    embedding1 = getEmbedding(containerGraph1)
    embedding2 = getEmbedding(containerGraph2)
    # cosineSim = cosineSimilarity(embedding1[0], embedding2[0])  # Doesn't return relevant values
    euclideanDis = euclideanDistance(embedding1[0], embedding2[0])
    return round(1-euclideanDis, 4)

# If a row with the given model file exists - remove the row
def removeIfExists(modelFile, graphTuples):
    for graphTuple in graphTuples:
        if graphTuple[0] == modelFile:
            graphTuples.remove(graphTuple)
            break

# Remove pod's instance ID from the pod's name, e.g., change 'frontend-5fc5754db6-f5h6c' to 'frontend'
def stripPodName(podName):
    hyphen = podName.rfind('-')
    if hyphen == -1:
        return podName
    shortPodName = podName[0:hyphen]
    hyphen = shortPodName.rfind('-')
    if hyphen != -1:
        shortPodName = shortPodName[0:hyphen]
    return shortPodName

# Read list of tuples (ModelFile, TopologyGraph, graphEmbedding, AG) from DB file (JSON)
def readDb():
    graphTuples = []
    if os.path.isfile(dfFileName):  # File exists
        dbFile = open(dfFileName, "r")
        graphTuples = json.load(dbFile)
        dbFile.close()
    return graphTuples

# Write list of tuples (ModelFile, TopologyGraph, graphEmbedding, AG) to DB file (JSON)
def writeDb(graphTuples):
    dbFile = open(dfFileName, "w")
    json.dump(graphTuples, dbFile, indent=4)
    dbFile.close()

# Fetch the attack graph file, i.e., ModelFile with .dot extension in AttackGraphs dir
def fetchAgFile(modelFile):
    agFileName = f"{agFilesDir}/{modelFile[:modelFile.rfind('.')]}.dot"
    if not os.path.isfile(agFileName):  # File does not exist
        return None
    return agFileName

# Count the number of CVEs for each topology graph node, separate for each CVE severity
def countCves(containerGraph, cveFile):
    # Read CVE file and count the number of CVEs for each topology graph node
    if not os.path.isfile(cveFile):  # File does not exist
        print(f"File {cveFile} does not exist")
        raise Exception()

    # CVE file format: Pod-ID,Software,Version,CVE-ID,CVE-Severity,CVE-Data
    csvinf = open(cveFile, 'r')
    csvin = csv.reader(csvinf, delimiter=',')
    for row in csvin:
        # Jump over empty lines, lines with too few parameters and title line
        if len(row) <= 6 or row[0] == 'Pod-ID':
            continue
        printDebug("Row to process: " + str(row))
        podName = row[0].strip()  # .replace('.', '_').replace('-', '_')
        if podName not in containerGraph.nodes:
            printDebug(f"{podName} not in the graph nodes, ignoring")
            continue
        # software = row[1].strip().replace('.', '_').replace('-', '_').replace(':', '_')
        # version = row[2].strip().replace('.', '_').replace('-', '_').replace(':', '_')
        # cveId = row[3].strip()
        cveSeverity = row[4].strip()
        # cveTitle = row[5].strip()
        cvss = row[6].strip()
        accessVector, _ = getCveParams(cvss)
        containerGraph.nodes[podName][cveSeverity] += 1
        if accessVector == "Network" or accessVector == "AdjacentNetwork":
            containerGraph.nodes[podName]["Network"] += 1

    csvinf.close()

    maxScore = 0
    for node in containerGraph:
        low = containerGraph.nodes[node]["LOW"]
        medium = containerGraph.nodes[node]["MEDIUM"]
        high = containerGraph.nodes[node]["HIGH"]
        critical = containerGraph.nodes[node]["CRITICAL"]
        unknown = containerGraph.nodes[node]["UNKNOWN"]
        totalNumber = critical + high + medium + low + unknown
        network = containerGraph.nodes[node]["Network"]  # Number of CVEs that can be exploited remotely
        ratio = 0
        if totalNumber != 0:
            ratio = ceil(network / totalNumber * 100)
        # Calculate consolidated CVE score by combining CVE severities
        totalScore = critical * 4 + high * 3 + medium * 2 + low + unknown
        if totalScore > maxScore:
            maxScore = totalScore
        containerGraph.nodes[node]["Score"] = totalScore
        print("# CVEs of {}: LOW:{}, MEDIUM:{}, HIGH:{}, CRITICAL:{}, UNKNOWN:{}, Total Score:{}; Remote Exploit:{} ({}%)".format(
            node, low, medium, high, critical, unknown, totalScore, network, ratio))
    if DEBUG:
        factor = ceil(maxScore / 5)
        scoreColors = ["#40B080", "#FFF22F", "#FFAC30", "#FF5330", "#AD3820", "#732516"]
        colors = []
        for node in containerGraph:
            if containerGraph.nodes[node]["Score"] < 10:
                colors.append(scoreColors[0])
            else:
                # Calculate color according to node's CVE Score
                scoreCategory = int(containerGraph.nodes[node]["Score"] / factor) + 1
                color = scoreColors[scoreCategory]
                colors.append(color)
        layout = nx.circular_layout(containerGraph)
        nx.draw_networkx(containerGraph, layout, node_color=colors)
        plt.show()


def main():
    action = "build"
    # containerTopologyFile = "Topologies/ContainerStaticTopology.csv"  # The file of container topology to process
    # cveFile = "CVEs/CveList.csv"  # The file of relevant CVEs
    # containerModelFile = None
    containerTopologyFile = "Topologies/ContainerStaticTopology.csv"  # The file of container topology to process
    cveFile = "CVEs/CveList.csv"  # The file of relevant CVEs
    containerModelFile = "ContainerStaticTopology.p"
    containerGraph = None
    graphTuples = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:t:c:m:", ["action=", "topology=", "cve=", "model="])
    except getopt.GetoptError:
        print(f"Usage: {sys.argv[0]} -a action -t topology_file -c cve_file -m model_file")
        print("action: build/update/find/compare/compare_bulk/count")
        print("build - create container topology and model for MulVAL")
        print("build_bulk - create bulk of container topologies without models for MulVAL")
        print("update - update the AG for each container topology")
        print("find - find similar container topology in the database of container topologies")
        print("compare - compare between two container topologies and return their similarity score")
        print("compare_bulk - compare a container topology with bulk of topologies and return similarity scores")
        print("count - create container topology and count number of CVEs for each node")
        print("topology_file: CSV of container's topology")
        print("cve_file: CSV of CVEs")
        print("model: PDDL file of the container model for MulVAL")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--action"):
            action = arg
        elif opt in ("-t", "--topology"):
            containerTopologyFile = arg
        elif opt in ("-c", "--cve"):
            cveFile = arg
        elif opt in ("-m", "--model"):
            containerModelFile = arg

    timeStamp = time.time()
    if action in ("build", "find", "compare", "compare_bulk", "count"):
        print(f"The container topology file to read: {containerTopologyFile}")
        containerGraph = readGraph(containerTopologyFile)
        layout = nx.circular_layout(containerGraph)
        # layout = nx.shell_layout(containerGraph)
        nx.draw_networkx(containerGraph, layout)
        plt.savefig("graph", dpi=300)
        if DEBUG:
            plt.show()

    if action in ("build", "build_bulk", "update", "find"):
        graphTuples = readDb()

    duration = time.time() - timeStamp
    print(f"The initial steps took {duration} seconds")

    if action == "build":
        if containerModelFile is None:
            # The file to create with list of predicates for container model (dependencies)
            dirIndex = containerTopologyFile.rfind('/') + 1  # Exclude '/'; if no directory, change returned -1 to 0
            containerModelFile = containerTopologyFile[dirIndex:containerTopologyFile.rfind('.')] + ".p"

        print("The CVE file to read: " + cveFile)
        # Create MulVAL's input file (PDDL) of container model (connections between nodes and known relevant CVEs)
        createContainersModel(containerGraph, cveFile, containerModelFile)
        print(f"The container model file {containerModelFile} was created.")

        # Split the graph into disjunctive sub-graphs
        components = [containerGraph.subgraph(c).copy() for c in nx.connected_components(containerGraph.to_undirected())]
        print(f"Number of disjunctive sub-graphs: {len(components)}.")
        for subgraph in enumerate(components):
            if DEBUG:
                layout = nx.circular_layout(subgraph[1])
                nx.draw_networkx(subgraph[1], layout)
                plt.show()
            # Create model for split sub-graph
            dotIndex = containerModelFile.rfind('.')
            if dotIndex == -1:
                dotIndex = len(containerModelFile)
            subgraphModelFile = f"{containerModelFile[0:dotIndex]}-{str(subgraph[0]+1)}.p"
            createContainersModel(subgraph[1], cveFile, subgraphModelFile)
            print(f"The container model file {subgraphModelFile} was created.")
            # Add tuple (subgraphModelFile, subgraph[1], graphEmbedding, None) to the graphTuples list
            # that will be saved in DB file
            graphString = []
            for edge in nx.generate_edgelist(subgraph[1]):
                graphString.append(edge)
            try:
                graphEmbedding = getEmbedding(subgraph[1])
            except RuntimeError:
                print("Creating the embedding of the topology graph is failed.")
                graphEmbedding = array.array('i')
            row = (subgraphModelFile, graphString, graphEmbedding.tolist(), None)
            removeIfExists(subgraphModelFile, graphTuples)  # If a row with the same model file exists - remove it
            graphTuples.append(row)

        writeDb(graphTuples)

    elif action == "build_bulk":
        for i in range(500):
            print(i)
            containerTopologyFile, cveFile = create_sub_graph.create_subgraph(None, None)
            containerGraph = readGraph(containerTopologyFile)
            if containerModelFile is None:
                # The file to create with list of predicates for container model (dependencies)
                dirIndex = containerTopologyFile.rfind('/') + 1  # Exclude '/'; if no directory, change returned -1 to 0
                containerModelFile = containerTopologyFile[dirIndex:containerTopologyFile.rfind('.')] + ".p"

            # Split the graph into disjunctive sub-graphs
            components = [containerGraph.subgraph(c).copy() for c in nx.connected_components(containerGraph.to_undirected())]
            print(f"Number of disjunctive sub-graphs: {len(components)}.")
            for subgraph in enumerate(components):
                # Create model file name for split sub-graph
                dotIndex = containerModelFile.rfind('.')
                if dotIndex == -1:
                    dotIndex = len(containerModelFile)
                subgraphModelFile = f"{containerModelFile[0:dotIndex]}-{str(subgraph[0]+1)}.p"
                # Add tuple (subgraphModelFile, subgraph[1], graphEmbedding, None) to the graphTuples list
                # that will be saved in DB file
                graphString = []
                for edge in nx.generate_edgelist(subgraph[1]):
                    graphString.append(edge)
                if len(graphString) == 0:
                    continue
                graphEmbedding = getEmbedding(subgraph[1])
                row = (subgraphModelFile, graphString, graphEmbedding.tolist(), None)
                removeIfExists(subgraphModelFile, graphTuples)  # If a row with the same model file exists - remove it
                graphTuples.append(row)
            containerModelFile = None

        writeDb(graphTuples)
        print(f"Number of tuples in the graph: {len(graphTuples)}")

    elif action == "update":
        # For each AG that is None, fetch attack graph, i.e., ModelFile with .dot extension in AttackGraphs dir
        for graphTuple in graphTuples:
            if graphTuple[3] is None:
                agFile = fetchAgFile(graphTuple[0])
                if agFile is not None:
                    graphTuple[3] = agFile
                    print(f"{graphTuple[0]} updated with AG {graphTuple[2]}")
        # Save updated graph tuples
        writeDb(graphTuples)

    elif action == "find":
        # Split the graph into disjunctive sub-graphs
        components = [containerGraph.subgraph(c).copy() for c in nx.connected_components(containerGraph.to_undirected())]
        print(f"Number of disjunctive sub-graphs: {len(components)}.")
        SimilarGraphs = namedtuple('SimilarGraphs', 'similarity graphtuple')
        for subgraph in enumerate(components):
            # Search for the most similar graph to each subgraph
            # Step 1 - use embedding similarity to find most 5% similar graphs
            graphEmbedding = getEmbedding(subgraph[1])
            similarGraphs = []
            for graphTuple in graphTuples:
                euclideanDis = euclideanDistance(graphEmbedding[0], numpy.asarray(graphTuple[2])[0])
                currentSimilarity = round(1 - euclideanDis, 4)
                similarGraphs.append(SimilarGraphs(currentSimilarity, graphTuple))
            similarGraphs.sort(key=lambda x: getattr(x, 'similarity'), reverse=True)
            topSimilar = max(int(len(similarGraphs)*0.05), 5)
            topSimilarGraphs = similarGraphs[0:topSimilar]

            # Step 2 - find most similar graph using Jaccard similarity
            graphSimilarity = 0
            mostSimilarTuple = None
            for similarGraph in topSimilarGraphs:
                graphTuple = getattr(similarGraph, 'graphtuple')
                graph = nx.parse_edgelist(graphTuple[1], create_using=nx.DiGraph)
                currentSimilarity = compareGraphs(subgraph[1], graph)
                if currentSimilarity > graphSimilarity:
                    graphSimilarity = currentSimilarity
                    mostSimilarTuple = graphTuple
            # If found with similarity >= 90%, return related AG
            if graphSimilarity >= 0.9:
                print("Found graph with similarity of {}; Topology: {}; AG: {}".format(
                    graphSimilarity, mostSimilarTuple[0], mostSimilarTuple[3]))
                if DEBUG and mostSimilarTuple[3] is not None:
                    # Plot .dot file to pdf
                    dotGraph = graphviz.Source.from_file(mostSimilarTuple[3], format='pdf', engine='dot')
                    dotGraph.render(mostSimilarTuple[3][:mostSimilarTuple[3].rfind('.')])
            else:
                print("Did not find any similar graph")

    elif action == "compare":
        containerTopologyFileToCompare = "Topologies/ContainerStaticTopology2.csv"
        containerGraph2 = readGraph(containerTopologyFileToCompare)
        if DEBUG:
            layout = nx.circular_layout(containerGraph2)
            nx.draw_networkx(containerGraph2, layout)
            plt.show()

        graphSimilarity = compareGraphs(containerGraph, containerGraph2)
        print(f"The Jaccard similarity between {containerGraph} and {containerGraph2} is {graphSimilarity}")
        euclideanDis = compareGraphsWithEmbedding(containerGraph, containerGraph2)
        print(f"The embedding similarity between {containerGraph} and {containerGraph2} is {euclideanDis} (Euclidean)")

    elif action == "compare_bulk":
        bulk = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150]
        for i in bulk:
            containerTopologyFileToCompare = f"Topologies/ContainerStaticTopology-357 Services-Less {i} Nodes.csv"
            containerGraph2 = readGraph(containerTopologyFileToCompare)
            graphSimilarity = compareGraphs(containerGraph, containerGraph2)
            print(f"The Jaccard similarity between {containerGraph} and {containerGraph2} is {graphSimilarity}")
            euclideanDis = compareGraphsWithEmbedding(containerGraph, containerGraph2)
            print(f"The embedding similarity between {containerGraph} and {containerGraph2} is {euclideanDis} (Euclidean)")

    elif action == "count":
        print("The CVE file to read: " + cveFile)
        countCves(containerGraph, cveFile)

    duration = time.time() - timeStamp
    print(f"The action took {duration} seconds")


if __name__ == "__main__":
    main()
