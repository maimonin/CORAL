# Lateral Movement Attack Simulation

This submodule contains data and scripts for simulating lateral movement (LM) attack scenarios in containerized environments and specifically in provenance logs. 

It is part of the CORAL framework's use cases for demonstrating attack graph generation and provenance-based threat detection.


## Features

- Simulation of attack scenarios with generated artifacts, edges, and processes. 
- Integration with provenance logs to enhance attack analysis. 
- Tools for analyzing and verifying attack data consistency. 
- Jupyter notebooks for data preparation and verification.


## Prerequisites

- Python 3.8+ 
- Jupyter Notebook 
- Pandas and other relevant Python libraries 
- Data files for provenance and simulation

## Directory Structure
```
.
├── alerts_mechanism_sigma_rules.ipynb
├── alerts_svc_to_rules.csv
├── alerts_svc_to_rules_with_prov_data.csv
├── example_alert_generator.py
├── lateral_movement_example_alerts.csv
├── sigma_rules_values_with_names.json
```

### Files:
- `attack_scenario123_gen_artifacts.csv`: CSV file containing the generated artifacts for a simulated attack scenario.
- `attack_scenario123_gen_edges.csv`: CSV file containing the generated edges representing relationships or interactions in the simulated attack.
- `attack_scenario123_gen_processes.csv`: CSV file containing details of processes involved in the simulated attack.
- `attack_scenario123_gen_processes.xlsx`: Excel version of the processes data for ease of use.
- `attack_scenario123_sim_gen_prov_logs.xlsx`: Excel file containing simulated provenance logs.
- `check_generated_attack.ipynb`: Jupyter notebook for analyzing and verifying the generated attack scenario data.
- `data_for_attack_simulation_logs.ipynb`: Jupyter notebook for preparing and integrating data for attack simulation logs.
- `prov_with_generated_artifacts.csv`: Combined provenance data and generated artifact data.
- `prov_with_generated_edges.csv`: Combined provenance data and generated edges.
- `prov_with_generated_processes.csv`: Combined provenance data and generated processes.
- `recommendationservice_distinct_cve.csv`: CSV file containing CVEs for recommendationservice (a microservice of the testbed application).


## Usage

Run the provided Jupyter notebooks to analyze, verify, and integrate data for lateral movement attack simulation.

### Analyzing Simulated Attack Data
* Use `check_generated_attack.ipynb` to:
  - Cross-verify the consistency of the simulated data.
  - Identify potential anomalies or insights related to the attack scenario.

### Preparing Provenance Logs
* Use `data_for_attack_simulation_logs.ipynb` to:
  - Preprocess and integrate attack data with provenance logs.
  - Generate outputs suitable for visualization and integration into the CORAL framework.


## Components

* `attack_scenario123_gen_artifacts.csv`
* `attack_scenario123_gen_edges.csv`
* `attack_scenario123_gen_processes.csv`
  - These CSV files represent the foundational data for the simulated attack scenario:
    - **Artifacts**: Key objects or files manipulated during the attack.
    - **Edges**: Relationships or interactions between artifacts and processes.
    - **Processes**: Details about the processes executed as part of the attack.


* `attack_scenario123_sim_gen_prov_logs.xlsx`
  * Excel file containing detailed simulated provenance logs for the attack scenario. These logs provide insights into data flow and process interactions.


* `check_generated_attack.ipynb`
  * This Jupyter notebook analyzes the simulated attack data to:
    - Verify the consistency of artifacts, edges, and processes.
    - Ensure all generated data aligns with expected patterns for the attack scenario.
  * **Key operations include:**
    - Parsing provenance data.
    - Cross-referencing processes, edges, and artifacts.
    - Identifying discrepancies or anomalies in the generated data.


* `data_for_attack_simulation_logs.ipynb`
  * This notebook prepares and integrates data for provenance log generation. It includes:
    - Loading and preprocessing artifact, process, and edge data.
    - Combining provenance data with simulated attack artifacts for seamless integration.
    - Generating outputs for use in visualization and analysis.


* `prov_with_generated_*`
  * These files combine provenance data with the generated attack artifacts, edges, and processes to create comprehensive datasets for attack analysis.


* `recommendation_distinct_cve.csv`
  * Recommendationservice (testbed application "Online Boutique" microservice) CVE analysis.
