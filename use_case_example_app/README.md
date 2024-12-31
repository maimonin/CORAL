# Use Case: Example Application - Lateral Movement Threat Detection

This module demonstrates the practical implementation of CORAL's framework by addressing use cases from the research, focusing on continuous risk assessment and lateral movement detection within containerized environments.

**This directory contains code, data, and results related to the **_Use Cases and Example Applications_** sections (Sections 4.4 and 4.5) of the CORAL research article.**


## Features
- Integration with Kubernetes environments. 
- Demonstrates lateral movement threat detection. 
- Utilizes provenance and attack graphs for enhanced detection. 
- Supports real-time analysis using dynamic topologies and vulnerability scans.


## Architecture

The main notebooks focus on lateral movement threat detection using provenance and attack graphs. Below are their highlights/features:

### `LM_Threat_Detection_only_provenance.ipynb`
- Objective: Analyze and detect lateral movement threats using only provenance data. 
- Processes:
  - Import provenance data in JSON format. 
  - Construct and visualize attack and provenance graphs using network and provenance data. 
  - Analyze vertices and arcs in the attack and provenance graphs to detect critical paths.

### `LM_Threat_Detection_w_alerts_and_attack.ipynb`
- Objective: Integrate alerts and attack data with provenance data for enhanced threat detection. 
- Processes:
  - Incorporate Kubernetes service mappings, attack graphs, alert datasets and provenance data converted to provenance graphs. 
  - Combine provenance data with alerts to refine detection capabilities. 
  - Highlight paths of lateral movement using interactive visualization of provenance graphs.


## Prerequisites
- Python 3.8+.
- Required Python libraries (see requirements.txt).
- Jupyter Notebook.
- Kubernetes cluster with configured `kubectl`.
- **Use Case Example Application submodules data and code:**
  - Attack Graphs (AG).
  - Alerts Mechanism.
  - Lateral Movement Attack Simulation.
  - Provenance Data.


## Directory Structure

```
.
├── LM_Threat_Detection_only_provenance.ipynb
├── LM_Threat_Detection_w_alerts_and_attack.ipynb
├── AG/
├── alerts_mechanism/
├── LM_attack_simulation/
├── provenance_data/
├── prov_graph_results/

```

- Files:
  - `LM_Threat_Detection_only_provenance.ipynb`: Jupyter notebook demonstrating lateral movement threat detection based only on existing preprocessed provenance data.
  - `LM_Threat_Detection_w_alerts_and_attack.ipynb`: Jupyter notebook incorporating alerts and attack data with provenance analysis for lateral movement detection.

- Subdirectories:
  - `AG/`: Contains data and visual representations of attack graphs. 
  - `alerts_mechanism/`: Files defining alert mechanisms using Sigma rules. 
  - `provenance_data/`: Stores provenance data for graph creation. 
  - `prov_graph_results/`: Visual outputs of provenance graph analysis.


## Usage

### Example for Running

1. Run `LM_Threat_Detection_only_provenance.ipynb`:
   - Load provenance data (prov_JSON files). 
   - Generate and analyze attack graphs to identify critical lateral movement paths.
2. Run `LM_Threat_Detection_w_alerts_and_attack.ipynb`:
   - Incorporate alerts and attack datasets. 
   - Refine analysis by integrating alerts with provenance data for prioritized detection.

### Output
- Provenance graphs in multiple formats along the analysis process. 
- Highlighted lateral movement paths.
- Integrated provenance and alert mappings.


---


## Contents

* Subdirectory: `AG`
  * Contains data and visual representations of the attack graphs (AGs) generated using the CORAL framework.
  - **Files:**
    - `ARCS.CSV`, `VERTICES.CSV`: CSV representations of the attack graph's arcs and vertices.
    - `AttackGraph.pdf`, `AttackGraph.txt`, `AttackGraph.xml`: Various formats of the attack graph for visualization and analysis.
    - `fig.4 example container ag.jpg`: Image representation of an example container attack graph.
    - `sub_graph_cve.csv`, `sub_graph_topology.csv`, `sub_graph_topology.p`: Subgraph data files.
    - `img.png`: General graphical representation of an intermediate output of an AG.

  
* Subdirectory: `alerts_mechanism`
  * Focuses on integrating security alerts with CORAL’s attack and provenance graphs.
  - **Files:**
    - `alerts_mechanism_sigma_rules.ipynb`: Notebook demonstrating the generation and application of Sigma rules for security alerts.
    - `alerts_svc_to_rules.csv`, `alerts_svc_to_rules_with_prov_data.csv`: CSVs mapping alerts to services and rules, including provenance data.
    - `example_alert_generator.py`: Python script to simulate alert generation.
    - `lateral_movement_example_alerts.csv`: Example dataset of lateral movement-related alerts.
    - `sigma_rules_values_with_names.json`: JSON file containing Sigma rule definitions.
  - **Subdirectories:**
    - `sigma_rules`: Contains Sigma rule files used for defining alert mechanisms.


* Subdirectory: `LM_attack_simulation`
  * Contains data and notebooks for simulating lateral movement attack scenarios and generating relevant logs.
  - **Files:**
    - `attack_scenario123_*`: CSV and Excel files containing generated artifacts, edges, and processes for a simulated attack scenario.
    - `check_generated_attack.ipynb`: Notebook for analyzing the generated attack data.
    - `data_for_attack_simulation_logs.ipynb`: Notebook for preparing data for simulation logs.
    - `prov_with_generated_*`: Files combining provenance data with simulated attack data.
    - `recommendationservice_distinct_cve.csv`: Recommendationservice (testbed application microservice) CVE analysis.


* Subdirectory: `provenance_data`
  * Contains provenance data used for generating provenance graphs and further analysis.
  - **Files:**
    - `add_services_to_provenance.py`: Script for adding service information to provenance data.
    - `app_artifact.csv`, `app_edges.csv`, `app_process.csv`: Base datasets for artifacts, edges, and processes.
    - `create_k8s_svc_df.py`: Script for creating Kubernetes service datasets.
    - `provenance_analysis.ipynb`: Notebook for analyzing provenance data.
    - `provenance_data_preprocess.py`: Preprocessing script for provenance datasets.
    - `provenance_data_README.md`: Documentation for this subdirectory.
  - **Subdirectories:**
    - `prov_JSON`: JSON-format provenance datasets.
    - `prov_Neo4j`: Neo4j-compatible provenance datasets.
    - `prov_PostgreSQL`: PostgreSQL-compatible provenance database dump.


* Subdirectory: `prov_graph_results`
  * Contains visual outputs of provenance graph analysis for Lateral Movement threat detection.
  - **Files:**
    - Various `.png` files representing custom, aggregated, highlighted, and filtered provenance graphs.
    - Legend files explaining the visual elements of each graph.
