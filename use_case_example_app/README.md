# `use_case_example_app` Directory README

This directory contains code, data, and results related to the Use Cases and Example Applications sections (Sections 4.4 and 4.5) of the CORAL research paper. Below is the structure and a brief explanation of each subdirectory and file.

## Directory Structure

### Root: `use_case_example_app`
- **Files:**
  - `LM_Threat_Detection_only_provenance.ipynb`: Jupyter notebook demonstrating lateral movement threat detection based only on existing preprocessed provenance data.
  - `LM_Threat_Detection_w_alerts_and_attack.ipynb`: Jupyter notebook incorporating alerts and attack data with provenance analysis for lateral movement detection.

- **Subdirectories:**
  - `AG`
  - `alerts_mechanism`
  - `LM_attack_simulation`
  - `provenance_data`
  - `prov_graph_results`

---

### Subdirectory: `AG`
Contains data and visual representations of the attack graphs (AGs) generated using the CORAL framework.

- **Files:**
  - `ARCS.CSV`, `VERTICES.CSV`: CSV representations of the attack graph's arcs and vertices.
  - `AttackGraph.pdf`, `AttackGraph.txt`, `AttackGraph.xml`: Various formats of the attack graph for visualization and analysis.
  - `fig.4 example container ag.jpg`: Image representation of an example container attack graph.
  - `sub_graph_cve.csv`, `sub_graph_topology.csv`, `sub_graph_topology.p`: Subgraph data files.
  - `img.png`: General graphical representation of an intermediate output of an AG.

---

### Subdirectory: `alerts_mechanism`
Focuses on integrating security alerts with CORAL’s attack graphs.

- **Files:**
  - `alerts_mechanism_sigma_rules.ipynb`: Notebook demonstrating the generation and application of Sigma rules for security alerts.
  - `alerts_svc_to_rules.csv`, `alerts_svc_to_rules_with_prov_data.csv`: CSVs mapping alerts to services and rules, including provenance data.
  - `example_alert_generator.py`: Python script to simulate alert generation.
  - `lateral_movement_example_alerts.csv`: Example dataset of lateral movement-related alerts.
  - `sigma_rules_values_with_names.json`: JSON file containing Sigma rule definitions.

- **Subdirectory:**
  - `sigma_rules`: Contains Sigma rule files used for defining alert mechanisms.

---

### Subdirectory: `LM_attack_simulation`
Contains data and notebooks for simulating lateral movement attack scenarios and generating relevant logs.

- **Files:**
  - `attack_scenario123_*`: CSV and Excel files containing generated artifacts, edges, and processes for a simulated attack scenario.
  - `check_generated_attack.ipynb`: Notebook for analyzing the generated attack data.
  - `data_for_attack_simulation_logs.ipynb`: Notebook for preparing data for simulation logs.
  - `prov_with_generated_*`: Files combining provenance data with simulated attack data.
  - `recommendationservice_distinct_cve.csv`: Recommendationservice (testbed application microservice) CVE analysis.

---

### Subdirectory: `provenance_data`
Contains provenance data used for generating provenance graphs and further analysis.

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

---

### Subdirectory: `prov_graph_results`
Contains visual outputs of provenance graph analysis for Lateral Movement threat detection.

- **Files:**
  - Various `.png` files representing custom, aggregated, highlighted, and filtered provenance graphs.
  - Legend files explaining the visual elements of each graph.

---
