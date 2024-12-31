# Provenance Data with CLARION for Kubernetes Environment

This submodule outlines the process of collecting provenance data using CLARION's capabilities, based on the SPADE framework, within a Kubernetes environment. It also includes an extension for associating Kubernetes services with the provenance data.

* This document describes how to collect provenance data using CLARION's abilities, based on the SPADE framework, in a Kubernetes environment.
* This document also describes the extension of associating services in the Kubernetes environment to the provenance data.

For more information on CLARION, SPADE, and the Linux Audit Reporter, please refer to the **_SPADE and CLARION_** and/or the **_References_** sections.


## Features
- Namespace-aware provenance tracking for containerized environments. 
- Integration with SPADE's Linux Audit Reporter for system-wide provenance collection. 
- Extended capabilities to associate Kubernetes services with provenance data.


## Prerequisites
* Computing environment with Linux kernel version 5.4 or **OLDER**.
* SPADE tool installed.
  * SPADE requirements: https://github.com/ashish-gehani/SPADE/wiki/Requirements
* Kubernetes cluster with `kubectl` installed and configured.
* Python 3.8 or later.
* Python packages - see `requirements.txt`.


## Directory Structure
```.
├── alerts_mechanism_sigma_rules.ipynb
├── alerts_svc_to_rules.csv
├── alerts_svc_to_rules_with_prov_data.csv
├── example_alert_generator.py
├── lateral_movement_example_alerts.csv
├── sigma_rules_values_with_names.json
├── sigma_rules
```

## Usage

### SPADE and CLARION
See the **_SPADE and CLARION_** section below for detailed instructions on how to install and collect provenance data in a Kubernetes environment using the SPADE framework and the CLARION extension.

### Adding Associated Services to Provenance Data

After outputting the provenance data in JSON format, you can add the associated services to the provenance data by running a Python script.

1. Collecting Services Data:
* Run the following command in order to collect the services' data:
  * `kubectl get svc -n <namespace_name> -o json > services_data.json`

2. Adding Services to Provenance Data 
* Run the following Python script to output extended provenance data with associated services:
  * ```python3 add_services_to_provenance.py <path_to_provenance_data> <path_to_services_data>```
  * The script will output the provenance data with the associated services in CSV format.


### Example for Running

1. **Collect Provenance Data:** Use the SPADE framework with its CLARION extension to collect provenance data from your Kubernetes cluster.


2. **Collect Kubernetes Services Data:** Execute the following command to gather Kubernetes service information:
   * ```kubectl get svc -n <namespace_name> -o json > services_data.json```


3. **Add Services to Provenance Data:** Use the provided Python script to link services with provenance data:
   * ``` add_services_to_provenance.py <path_to_provenance_data> <path_to_services_data> ```


4. **Preprocess Provenance Data:** Use the provided Python script to preprocess the provenance data:
   * ``` preprocess_provenance_data.py ```

### Output
The provenance data is exported in a CSV format, including service associations derived from Kubernetes metadata.



---



## SPADE and CLARION

* SPADE (Support for Provenance Auditing in Distributed Environments) is an open source project, originating from scientific articles. 
* The baseline for CLARION was the provenance inferred from Linux Audit, using SPADE's Audit Reporter:
  * [Collecting system wide provenance on Linux with Audit](https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit).
* CLARION adds namespace-awareness (relevant to containerized environments) to this provenance. 
  * This functionality has been incorporated into SPADE's Audit Reporter: 
  [Configuring namespace reporting](https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#configuring-namespace-reporting).


### SPADE and CLARION Installation
1. SPADE installation: 
   * https://github.com/ashish-gehani/SPADE/wiki/Downloading-and-compiling#linux-and-macos
   * NOTE: build and compile SPADE by running `make KERNEL_MODULES=true` (instead of `make`).
2. Requirements for Linux Audit Reporter: 
   * https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#requirements


### Running CLARION
1. Start SPADE (server and controller): 
   * https://github.com/ashish-gehani/SPADE/wiki/Starting-and-controlling-SPADE
2. Create JSON output: 
   * https://github.com/ashish-gehani/SPADE/wiki/Creating-JSON-output
3. Start Audit Reporter with namespace reporting: 
   * https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#configuring-namespace-reporting
4. Record provenance data for your desired duration.
5. Stop recording provenance data:
   1. Stop the Audit Reporter: 
      * `remove reporter <class name>`
   2. Stop provenance data from being written to the JSON file: 
      * `remove storage JSON` 
      * https://github.com/ashish-gehani/SPADE/wiki/Creating-JSON-output



---




## References

1. SPADE: https://github.com/ashish-gehani/SPADE
2. Linux Audit Reporter: https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit
3. CLARION: https://www.usenix.org/conference/usenixsecurity21/presentation/chen-xutong
