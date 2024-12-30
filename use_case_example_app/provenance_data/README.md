# Provenance Data with CLARION for Kubernetes Environment
This document describes how to collect provenance data using CLARION's abilities, based on the SPADE framework, in a Kubernetes environment.

This document also includes the extension of associating services in the Kubernetes environment to the provenance data.


## Prerequisites
* Linux kernel version 5.4 or **OLDER**.
* SPADE requirements: https://github.com/ashish-gehani/SPADE/wiki/Requirements


## About SPADE and CLARION
SPADE is an open source project.<br>
The baseline for CLARION was the provenance inferred from Linux Audit, using SPADE's Audit Reporter: 
[Collecting system wide provenance on Linux with Audit](https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit).<br> 
CLARION adds namespace-awareness (relevant to containerized environments) to this provenance. This functionality has been incorporated into SPADE's Audit Reporter: 
[Configuring namespace reporting](https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#configuring-namespace-reporting).


## SPADE and CLARION Installation
1. SPADE installation: https://github.com/ashish-gehani/SPADE/wiki/Downloading-and-compiling#linux-and-macos
    * NOTE: build and compile SPADE by running `make KERNEL_MODULES=true` (instead of `make`).
2. Requirements for Linux Audit Reporter: https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#requirements


## Running CLARION
1. Start SPADE (server and controller): https://github.com/ashish-gehani/SPADE/wiki/Starting-and-controlling-SPADE
2. Create JSON output: https://github.com/ashish-gehani/SPADE/wiki/Creating-JSON-output
3. Start Audit Reporter with namespace reporting: https://github.com/ashish-gehani/SPADE/wiki/Collecting-system-wide-provenance-on-Linux-with-Audit#configuring-namespace-reporting
4. Record provenance data for your desired duration.
5. Stop recording provenance data:
   1. Stop the Audit Reporter: `remove reporter <class name>`
   2. Stop provenance data from being written to the JSON file: `remove storage JSON` (https://github.com/ashish-gehani/SPADE/wiki/Creating-JSON-output)

## Adding Associated Services to Provenance Data
After outputting the provenance data in JSON format, you can add the associated services to the provenance data by running a Python script.
### 1. Collecting Services Data
Run the following command in order to collect the services' data:

`kubectl get svc -n <namespace_name> -o json > services_data.json`

### 2. Adding Services to Provenance Data
Run the following Python script to output extended provenance data with associated services:
```bash
python3 add_services_to_provenance.py <path_to_provenance_data> <path_to_services_data>
```
The script will output the provenance data with the associated services in CSV format.