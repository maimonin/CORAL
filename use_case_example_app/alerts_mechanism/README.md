# `alerts_mechanism` README

This subdirectory contains code, data, and configurations for implementing and demonstrating alert mechanisms within the CORAL framework. The primary focus is on generating, mapping, and integrating security alerts with provenance and attack graph data to enhance lateral movement detection and risk assessment.

## Directory Structure

- **Files:**
  - `alerts_mechanism_sigma_rules.ipynb`: A Jupyter notebook demonstrating the generation of security alerts using Sigma rules and their mapping to services and provenance data.
  - `alerts_svc_to_rules.csv`: A CSV mapping services to the Sigma rules applied.
  - `alerts_svc_to_rules_with_prov_data.csv`: An enriched version of `alerts_svc_to_rules.csv`, including provenance data correlations.
  - `example_alert_generator.py`: A Python script to simulate alert generation based on predefined rules and scenarios.
  - `lateral_movement_example_alerts.csv`: Example dataset of alerts related to lateral movement detection generated with `example_alert_generator.py`.
  - `sigma_rules_values_with_names.json`: A JSON file containing mapping rules to their corresponding values.

- **Subdirectory:**
  - `sigma_rules`: Contains Sigma rule files defining alert mechanisms.

---

## File Details

### `alerts_mechanism_sigma_rules.ipynb`
This Jupyter notebook demonstrates the following:
- Loading and parsing Sigma rules.
- Mapping Sigma rules to specific Kubernetes services.
- Integrating Sigma-generated alerts with provenance data for enhanced threat detection.

### `alerts_svc_to_rules.csv`
A CSV file mapping Kubernetes services to specific Sigma rules applied.
- **Columns:**
  - `svc`: Name of the Kubernetes service.
  - `ports`: List of ports associated with the service.
  - `process_ids`: List of process IDs associated with the service.
  - `rules`: List of Sigma rules applied to the service.

### `alerts_svc_to_rules_with_prov_data.csv`
An extended version of `alerts_svc_to_rules.csv`, enriched with provenance data to:
- Map services to provenance artifacts and processes.
- Facilitate integration with provenance graphs for lateral movement detection.

### `example_alert_generator.py`
A Python script to simulate alerts based on predefined scenarios. This script can:
- Generate synthetic alerts for testing purposes.
- Simulate various lateral movement scenarios in a containerized environment.

### `lateral_movement_example_alerts.csv`
Contains sample alerts generated for lateral movement scenarios.

### `sigma_rules_values_with_names.json`
A JSON file containing mapping rules to their corresponding values.

### Subdirectory: `sigma_rules`
Contains the individual Sigma rule files (.yml format) that define specific alerting conditions. These rules are critical for generating alerts that are:
- Mapped to Kubernetes services.
- Integrated with CORAL’s attack graph and provenance graph frameworks.

---

## Usage

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- Required Python libraries: os, pandas, yaml, json

### Running the Notebook
1. Open `alerts_mechanism_sigma_rules.ipynb` in Jupyter Notebook.
2. Install the required libraries if not already installed.
3. Execute cells sequentially to:
   - Parse Sigma rules.
   - Map alerts to services and provenance data.
   - Generate alerts.

