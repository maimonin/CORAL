# Orchestrator

The Orchestrator is a core module in the CORAL framework that generates and analyzes container-based graph representations of microservices. It facilitates creating and manipulating subgraphs and builds topology graphs to support vulnerability analysis and attack modeling. The Orchestrator module includes scripts and data to process container topologies, create subgraphs, and manage graph-related functionalities.


## Features

The Orchestrator component includes the following Python submodules:

1. `BuildContainersGraph.py`
   - Reads and constructs directed graphs from container topology files. 
   - Generates container interaction models for MulVAL (logical attack graphs). 
   - Supports graph comparison using Jacquard similarity and embedding-based metrics. 
   - Produces embeddings of topology graphs for further analysis. 
   - Facilitates bulk generation of container models.

2. `create_sub_graph.py`
   - Removes specified microservices and their connections from a full topology graph. 
   - Ensures stale connections are cleaned up post-microservice removal. 
   - Provides configurable thresholds for random removal of microservices and connections. 
   - Outputs resulting subgraph topologies and associated CVE data.


## Prerequisites
- Python 3.8 or higher 
- Required Python libraries:
  - networkx 
  - karateclub 
  - matplotlib 
  - pandas 
  - numpy
  - graphviz


## Directory Structure

```
.
├── BuildContainersGraph.py
├── create_sub_graph.py
├── README.md
├── data
│   ├── cve_24_05_04_2023.csv
│   ├── cve_357_01_22_2023.csv
│   ├── static_topology_24_05_04_2023.csv
│   ├── static_topology_357_01_22_2023.csv
```

### `data/`

* `cve_*.csv`: Contains CVE data files with details about vulnerabilities. 
* `static_topology_*.csv`: Includes container topology files defining relationships and configurations of containers.


## Usage

### `BuildContainersGraph.py`
To build and analyze container graphs, run:

`BuildContainersGraph.py -a build -t <topology_file> -c <cve_file> -m <model_file>`

Options:
- `-a`: Specifies the action (build, update, compare, etc.).
- `-t`: Path to the container topology file.
- `-c`: Path to the CVE file.
- `-m`: Output file for the container model.


### `create_sub_graph.py`
To create sub-graphs, run:
```
create_sub_graph.py
```

Functionalities:
1. Loads the full topology graph and CVE data. 
2. Removes a subset of microservices and connections (randomly or specified). 
3. Outputs the resulting subgraph files to the data/ directory.

File Structure:
* `Topologies/`: Contains the static topology graphs. 
* `CVEs/`: Stores the CVE data files. 
* `TopologyBulk/`: Outputs the generated subgraph files. 
* `AttackGraphs/`: Stores attack graphs created during analysis.
* `cisa_exploited_vulnerabilities/`: Contains known exploited vulnerabilities data.

### Output

* **Graph models:** For use with tools like MulVAL. 
* **Subgraph topologies:** CSV files describing the reduced topology and its associated vulnerabilities.