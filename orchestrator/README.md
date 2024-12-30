# Orchestrator

The Orchestrator is a core module in the CORAL framework that generates and analyzes container-based graph representations of microservices. It facilitates creating and manipulating subgraphs and builds topology graphs to support vulnerability analysis and attack modeling. The Orchestrator module includes scripts and data to process container topologies, create subgraphs, and manage graph-related functionalities.


## Overview

The Orchestrator component includes the following Python scripts:

1. `BuildContainersGraph.py`: Processes container topology data, generates graph models for vulnerability analysis, enables graph comparison, and creates embeddings for topology graphs.

2. `create_sub_graph.py`: Handles the creation of subgraphs by removing specified microservices and their connections from a full topology graph.



## Directory Structure

The Orchestrator module consists of the following files and directories:

```
├── BuildContainersGraph.py
├── create_sub_graph.py
├── listdirs.py
├── orchestrator_README.md
├── data
│   ├── cve_24_05_04_2023.csv
│   ├── cve_357_01_22_2023.csv
│   ├── static_topology_24_05_04_2023.csv
│   ├── static_topology_357_01_22_2023.csv
```

### `data/`

The data/ directory contains CSV files used by the Orchestrator module:

* `cve_*.csv`: CVE data files with details about vulnerabilities. 

* `static_topology_*.csv`: Container topology files defining the relationships and configurations of containers.



## Features

### `BuildContainersGraph.py`
- Reads and builds directed graphs from container topology files.
- Creates container interaction models for use with MulVAL. 
- Generates embeddings of topology graphs.
- Supports graph comparison using Jacquard similarity and embedding-based metrics. 
- Enables bulk graph generation and comparison for scalability.

### `create_sub_graph.py`
- Parses and removes specified microservices and their dependencies from a given topology. 
- Ensures stale connections are cleaned up after microservices are removed. 
- Allows random removal of microservices and connections based on configurable thresholds. 
- Outputs the resulting subgraph topology and CVE data.



## Requirements

- Python 3.8 or higher 
- Required Python libraries:
  - networkx 
  - karateclub 
  - matplotlib 
  - graphviz 
  - pandas 
  - numpy 
  - requests


## Usage

### `BuildContainersGraph.py`
To build and analyze container graphs:

`python BuildContainersGraph.py -a build -t <topology_file> -c <cve_file> -m <model_file>`

Options:
- `-a`: Specifies the action (build, update, compare, etc.).
- `-t`: Path to the container topology file.
- `-c`: Path to the CVE file.
- `-m`: Output file for the container model.


### `create_sub_graph.py`
This script:

1. Loads the full topology graph from `Topologies/ContainerStaticTopology.csv` and CVE data from `CVEs/CveList.csv`.
2. Removes a random subset of microservices and connections, unless explicitly specified.
3. Saves the resulting subgraph to `TopologyBulk/`.


## File Structure
* `Topologies/`: Contains the static topology graphs. 
* `CVEs/`: Stores the CVE data files. 
* `TopologyBulk/`: Outputs the generated subgraph files. 
* `AttackGraphs/`: Stores attack graphs created during analysis.
* `cisa_exploited_vulnerabilities/`: Contains known exploited vulnerabilities data.

