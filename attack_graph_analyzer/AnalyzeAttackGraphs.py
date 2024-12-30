import json
import sys
import csv
from os.path import isfile, join
import statistics
import requests

DEBUG = True

class AnalysisResults:
    numAttackPointsList = []
    numVulnerablePodsList = []
    vulnerablePodsList = []  # List of PodStat objects

class PodStat:
    def __init__(self, podName, interactions, libs, cves, highestLikelihood):
        self.podName = podName
        self.interactions = interactions  # The number of the pod's interactions in the topology AG
        self.libs = libs  # The vulnerable libraries reside in the pod
        self.cves = cves  # The CVEs of the pod in the topology AG
        self.highestLikelihood = highestLikelihood  # The highest prediction scoring CVE (likelihood to be exploited)

class CveScore:
    def __init__(self, cve, score):
        self.cve = cve
        self.score = score

class LibCves:
    def __init__(self, lib, cves):
        self.lib = lib
        self.cves = cves


def printDebug(debugMessage):
    if DEBUG:
        print(debugMessage)


# Go over the attack graph in the given directory and gather interesting info
def analyzeAGs(inputDir):
    analysisResults = AnalysisResults()
    verticesFile = join(inputDir, "VERTICES.CSV")  # Nodes
    if not isfile(verticesFile):  # File does not exist
        printDebug(f"File {verticesFile} does not exist")
    else:
        csvInf = open(verticesFile, 'r')
        csvIn = csv.reader(csvInf, delimiter=',')
        nodes = []
        for row in csvIn:
            if len(row) <= 1:  # Jump over empty lines
                continue
            nodes.append(row[1].strip())
        csvInf.close()

        analyzeAgNodes(nodes, analysisResults)
        printDebug(f"Finished analyzing directory {inputDir}")

    return analysisResults


# 1. Find the number of attack points (entry points an attacker can exploit) in the AG.
#    How: Count the number of hacl() IRs in vertices file
# 2. Find the number of vulnerable software, accessible from the external world (external attacker)
#    How: Count the number of diamonds (vulnerablePod()) in vertices file.
#    This includes the level-1 vulnerable pods (steps 1), so we subtract it to find the “new” assets
#    an attacker may access.
# 3. Find the number of interactions of each pod in topology AG.
#    How: through dataFlow() in the topology’s AG (Vertices.csv) file.
# 4. Find the libraries of each pod in topology AG.
#    How: through residesOn() in the topology’s AG (Vertices.csv) file.
# 5. Find the CVEs of each lib in the topology AG.
#    How: through vulExists() in the topology’s AG (Vertices.csv) file.
# 5.1. Attach CVE to pod through libs
# 5.2. For each CVE find if it has an exploit and what is its exploitability score.
#      For each pod, save the highest exploitability score (if CVE has an exploit, the score is 100%).
#      How: with known_exploited_vulnerabilities.csv (from https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
#      and FIRST.org’s EPSS
def analyzeAgNodes(nodes, analysisResults):
    numAttackPoints = 0
    numVulnerablePods = 0
    libCvesList = []

    for node in nodes:
        if "hacl" in node:
            numAttackPoints += 1
        elif "vulnerablepod" in node.lower():
            numVulnerablePods += 1
            countPodsAppearances(node, analysisResults.vulnerablePodsList)
        elif "dataFlow" in node:
            podName = node[node.find('(') + 1:node.find(',')]
            countPodsInteractions(podName, analysisResults.vulnerablePodsList)
            podName = node[node.find(',') + 1:node.find(',\'')]
            countPodsInteractions(podName, analysisResults.vulnerablePodsList)
        elif "residesOn" in node:
            findPodsLibs(node, analysisResults.vulnerablePodsList)
        elif "vulExists" in node:
            findLibsCVEs(node, libCvesList)

    attachCveToPod(analysisResults.vulnerablePodsList, libCvesList)
    analysisResults.numAttackPointsList.append(numAttackPoints)
    analysisResults.numVulnerablePodsList.append(
        numVulnerablePods - numAttackPoints)
    findCVEsLikelihood(analysisResults.vulnerablePodsList)

# If the pod in the given AG node is already in the list of vulnerable pods, update its appearances;
# Otherwise, create a new object and put it in the vulnerable pods list
def countPodsAppearances(agNode, vulnerablePods):
    podName = agNode[agNode.find('(')+1:agNode.find(')')]
    podFound = False
    for vulnerablePod in vulnerablePods:
        if podName == vulnerablePod.podName:
            podFound = True
            break

    if not podFound:
        podStat = PodStat(podName, 0, [], [], 0)
        vulnerablePods.append(podStat)

# If the given pod is already in the list of vulnerable pods, update its interactions;
# Otherwise, create a new object and put it in the vulnerable pods list
def countPodsInteractions(podName, vulnerablePods):
    podFound = False
    for vulnerablePod in vulnerablePods:
        if podName == vulnerablePod.podName:
            vulnerablePod.interactions += 1
            podFound = True
            break

    if not podFound:
        podStat = PodStat(podName, 1, [], [], 0)
        vulnerablePods.append(podStat)

# If the pod in the given AG node is already in the list of vulnerable pods, update its libs;
# Otherwise, create a new object and put it in the vulnerable pods list
def findPodsLibs(agNode, vulnerablePods):
    podName = agNode[agNode.find('(')+1:agNode.find(',')]
    libName = agNode[agNode.find(',')+1:agNode.find('\'')-1]
    libVersion = agNode[agNode.find('\'')+1:agNode.find('\')')]
    lib = libName + '-' + libVersion
    podFound = False
    for vulnerablePod in vulnerablePods:
        if podName == vulnerablePod.podName:
            if lib not in vulnerablePod.libs:
                vulnerablePod.libs.append(lib)
            podFound = True
            break

    if not podFound:
        podStat = PodStat(podName, 0, [lib], [], 0)
        vulnerablePods.append(podStat)

# If the pod in the given AG node is already in the list of vulnerable pods, update its CVEs;
# Otherwise, create a new object and put it in the vulnerable pods list
def findLibsCVEs(agNode, libs):
    cve = agNode[agNode.find('(\'')+2:agNode.find('\',')]
    libName = agNode[agNode.find(',')+1:agNode.find(',\'')]
    libVersion = agNode[agNode.find(',\'')+2:agNode.find('\',\'')]
    libFull = libName + '-' + libVersion
    libFound = False
    for lib in libs:
        if libFull == lib.lib:
            if cve not in lib.cves:
                lib.cves.append(cve)
            libFound = True
            break

    if not libFound:
        libCves = LibCves(libFull, [cve])
        libs.append(libCves)

# In libCvesList CVE is related to lib, and in vulnerablePods lib is related to pod
def attachCveToPod(vulnerablePods, libCvesList):
    for vulnerablePod in vulnerablePods:
        for lib1 in vulnerablePod.libs:
            for lib2 in libCvesList:
                if lib1 == lib2.lib:
                    for cve in lib2.cves:
                        vulnerablePod.cves.append(cve)

# For each CVE, search it in the known exploited vulnerabilities; if found the likelihood is 100%
# Otherwise, use FIRST.org’s EPSS (exploit prediction score system) to find the likelihood
def findCVEsLikelihood(vulnerablePods):
    # Read stored CVE scores and fill with all other unique CVEs
    cveScoreFile = "CveScoreFile.csv"
    cveScores = readCveScoreFile(cveScoreFile)
    cveScores = findAllUniqueCves(cveScores, vulnerablePods)

    # Load known exploited vulnerabilities
    knownExploitedFile = "cisa_exploited_vulnerabilities/known_exploited_vulnerabilities.csv"
    csvInf = open(knownExploitedFile, 'r')
    csvIn = csv.reader(csvInf, delimiter=',')
    exploitedCves = []
    for row in csvIn:
        if len(row) <= 1 or not row[0].startswith("CVE-"):  # Jump over empty lines
            continue
        exploitedCves.append(row[0].strip())
    csvInf.close()

    for vulnerablePod in vulnerablePods:
        for cve in vulnerablePod.cves:
            if cve in exploitedCves:
                vulnerablePod.highestLikelihood = 1
                break
            else:
                epss = getCveScore(cve, cveScores)
                if epss == 0:
                    request = f'https://api.first.org/data/v1/epss?cve={cve}'
                    host_reply = requests.get(request)
                    # host_reply is JSON-like, extract epss and if greater than previous, save
                    json_object = json.loads(host_reply.content)
                    epss = float(json_object['data'][0]['epss'])
                    updateCveScore(cve, epss, cveScores)
                # If current epss is greater than previous one, save it
                if epss > vulnerablePod.highestLikelihood:
                    vulnerablePod.highestLikelihood = epss

    # Store CVE scores
    createCveScoreFile(cveScoreFile, cveScores)


# Read CVE score file. File format: cve,score
def readCveScoreFile(cveScoreFile):
    if not isfile(cveScoreFile):  # File does not exist
        return []
    csvInf = open(cveScoreFile, 'r')
    csvIn = csv.reader(csvInf, delimiter=',')
    cveScores = []
    for row in csvIn:
        if len(row) <= 1:  # Jump over empty lines
            continue
        cveScore = CveScore(row[0].strip(), float(row[1]))
        cveScores.append(cveScore)

    csvInf.close()
    return cveScores

# Create CVE score file for the given list
def createCveScoreFile(cveScoreFile, cveScores):
    fileStream = open(cveScoreFile, "w")
    for cveScore in cveScores:
        row = f"{cveScore.cve}, {cveScore.score}\n"
        fileStream.write(row)

    fileStream.close()

# Find all the unique CVEs in all the vulnerable pods
def findAllUniqueCves(cveScores, vulnerablePods):
    for vulnerablePod in vulnerablePods:
        for cve in vulnerablePod.cves:
            if not cveExists(cve, cveScores):
                cveScore = CveScore(cve, 0)
                cveScores.append(cveScore)

    return cveScores

# Check if the given CVE is in the cveScores list
def cveExists(cve, cveScores):
    for cveScore in cveScores:
        if cveScore.cve == cve:
            return True
    return False

# Get the EPSS of the given CVE
def getCveScore(cve, cveScores):
    epss = 0
    for cveScore in cveScores:
        if cveScore.cve == cve:
            epss = cveScore.score
            break
    return epss

# Update the given CVE score in the list
def updateCveScore(cve, epss, cveScores):
    for cveScore in cveScores:
        if cveScore.cve == cve:
            cveScore.score = epss
            break


def main():
    inputDir = "AttackGraphs/AG-11Services"  # The directory of attack graph to process
    if len(sys.argv) > 1:
        inputDir = sys.argv[1]

    print(f"The directory to process: {inputDir}")
    analysisResults = analyzeAGs(inputDir)
    print(f"List of number of attack points={analysisResults.numAttackPointsList}")
    print(f"List of number of vulnerable pods={analysisResults.numVulnerablePodsList}")
    print(f"# of vulnerable pods mean={round(statistics.mean(analysisResults.numVulnerablePodsList), 2)}; "
          f"max={max(analysisResults.numVulnerablePodsList)}")
    print(f"List of vulnerable pods:")
    print("Pod Name, Impact (Interactions), # CVEs, Likelihood (CVE Highest EPSS), Risk")
    for vulBin in analysisResults.vulnerablePodsList:
        # We consider the number of interactions of each pod as the impact of each pod.
        # Combined with the exploit probability (step 5), build a risk (impact x probability) assessment table.
        binImpact = vulBin.interactions
        binExploitProb = round(vulBin.highestLikelihood * 100, 2)
        print(f"{vulBin.podName}, {binImpact}, {len(vulBin.cves)}, {binExploitProb}, "
              f"{round(binImpact * binExploitProb)}")


if __name__ == "__main__":
    main()
