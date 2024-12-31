# Alerts Mechanism

The alerts mechanism submodule is part of the example application demonstrating a use case of the CORAL framework.

This submodule is designed for generating and managing security alerts. It integrates Sigma rules with provenance and service data to enhance threat detection and lateral movement identification in containerized environments.

Sigma rules are detection rules for security monitoring systems. They are defined in a YAML format and can be used with various SIEM systems.
_For more information on Sigma rules, see the References section at the end of this document._

This subdirectory contains code, data, and configurations for implementing and demonstrating alert mechanisms within the CORAL framework. 


## Features
- Security alert generation using Sigma rules.
- Service-to-rule mapping for clear alert association.
- Provenance data enrichment for contextual insights.
- Lateral movement scenario simulation.
- Example datasets for testing and demonstration.


## Prerequisites
- Python 3.8+
- Required Python libraries: pandas, yaml, json.
- Jupyter Notebook.
- Sigma rules (included in the `sigma_rules` subdirectory).


## Directory Structure

```
.
├── alerts_mechanism_sigma_rules.ipynb
├── alerts_svc_to_rules.csv
├── alerts_svc_to_rules_with_prov_data.csv
├── example_alert_generator.py
├── lateral_movement_example_alerts.csv
├── sigma_rules_values_with_names.json
├── sigma_rules
│   ├── application
│   ├── category
│   ├── cloud
│   ├── compliance
│   ├── linux
│   ├── macos
│   ├── network
│   ├── web
│   └── windows
```

### Files:
  - `alerts_mechanism_sigma_rules.ipynb`: Demonstrates security alert generation using Sigma rules and mapping to services and provenance data.
  - `alerts_svc_to_rules.csv`: Maps services to applied Sigma rules.
  - `alerts_svc_to_rules_with_prov_data.csv`: Enriched service-to-rule mapping with provenance data.
  - `example_alert_generator.py`: Simulates alert generation for predefined rules and scenarios.
  - `lateral_movement_example_alerts.csv`: Contains example alerts for lateral movement detection.
  - `sigma_rules_values_with_names.json`: Defines Sigma rule values.

### Subdirectories:
  - `sigma_rules`: Contains Sigma rule files defining alert mechanisms.
    - For more information on Sigma rules, see the References section below.


## Usage

1. Open `alerts_mechanism_sigma_rules.ipynb` Jupyter Notebook.
2. Execute cells sequentially to:
   - Parse Sigma rules. 
   - Map alerts to services and provenance data. 
   - Generate and analyze alerts.

* Alternatively, use the `example_alert_generator.py` script to simulate alerts for testing and demonstration purposes.

### Output

- CSV files for service-to-rule mappings:
  - `alerts_svc_to_rules.csv`
  - `alerts_svc_to_rules_with_prov_data.csv`
- CSV file for synthetic alerts demonstrating lateral movement scenarios:
  - `lateral_movement_example_alerts.csv`


## Components

* `alerts_mechanism_sigma_rules.ipynb`
  * This Jupyter notebook demonstrates the following:
    - Loading and parsing Sigma rules.
    - Mapping Sigma rules to specific Kubernetes services.
    - Integrating Sigma-generated alerts with provenance data for enhanced threat detection.


* `alerts_svc_to_rules.csv`
  * A CSV file mapping Kubernetes services to specific Sigma rules applied.
    - Columns:
      - `svc`: Name of the Kubernetes service.
      - `ports`: List of ports associated with the service.
      - `process_ids`: List of process IDs associated with the service.
      - `rules`: List of Sigma rules applied to the service.


* `alerts_svc_to_rules_with_prov_data.csv`
  * An extended version of `alerts_svc_to_rules.csv`, enriched with provenance data to:
    - Map services to provenance artifacts and processes.
    - Facilitate integration with provenance graphs for lateral movement detection.


* `example_alert_generator.py`
  * A Python script to simulate alerts based on predefined scenarios. This script can:
    - Generate synthetic alerts for testing purposes.
    - Simulate various lateral movement scenarios in a containerized environment.


* `lateral_movement_example_alerts.csv`
  * Contains sample alerts generated for lateral movement scenarios.


* `sigma_rules_values_with_names.json`
  * A JSON file containing mapping rules to their corresponding values.


* `sigma_rules` Subdirectory
  * Contains the individual Sigma rule files (.yml format) that define specific alerting conditions. 
  * These rules are critical for generating alerts that are:
    - Mapped to Kubernetes services.
    - Integrated with CORAL’s attack graph and provenance graph frameworks.
  * **For more information on Sigma rules, see the References section below.** 


## References

* [Sigma Rules GitHub Repository](https://github.com/SigmaHQ/sigma)

