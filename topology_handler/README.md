# Topology Handler

The Topology Handler is a component of the CORAL architecture. It is responsible for mapping and analyzing Kubernetes cluster topology by integrating static and dynamic information about pods, network policies, and services. This component consists of two submodules:

1. **Static Mapper**
2. **Dynamic Mapper**


## Features

The Topology Handler consists of two main components: the Static Mapper and the Dynamic Mapper.

### Static Mapper
The Static Mapper creates a detailed topology map of Kubernetes pods and their network policies. It focuses on extracting static information from the cluster, such as pod metadata, IP addresses, protocols, ports, and associated network policies.

* Key Features:
  - Scans Kubernetes cluster to extract pod metadata, network policies, and connections.
  - Integrates with Kubernetes via its Python client.
  - Generates topology details, including:
    - Pod-ID
    - IP
    - Pod-Inbound-List (tuple of Pod-ID, Protocol, Port)
    - Protocol
    - Port
  - Exports the results to a structured CSV file for further analysis.
  - Translates topology data into facts for further analysis.

### Dynamic Mapper
The Dynamic Mapper captures live network data using Cilium Hubble, processes this data, and generates a dynamic topology map. It supplements the static mapping by adding real-time insights into pod interactions.

* Key Features:
  - Monitors real-time pod communications using Cilium Hubble.
  - Processes live network traffic flows to extract details like protocol, source/target names, and ports.
  - Evaluates changes to determine if a new attack graph is required.
  - Exports the processed data to a CSV file.


## Architecture

### Static Mapper
* Purpose: Create a static topology map of Kubernetes pods and their network policies.
* Key Functions:
  * `create_topology()`: Extracts data from Kubernetes and builds a topology DataFrame. 
  * `run_topology_creation()`: Initiates API client configuration and topology creation.

### Dynamic Mapper
* Purpose: Build a dynamic topology map based on live network traffic. 
* Key Functions:
  * `run_hubble_observe()`: Captures live traffic data. 
  * `process_data()`: Processes captured traffic to generate dynamic topology. 
  * `run_full_script()`: Executes the full dynamic mapping workflow, including Hubble setup and data processing.


## Prerequisites

- Python 3.8+
- Python libraries:
  - Kubernetes Python Client
  - Pandas library


- **Static Mapper:**
  - Kubernetes cluster with pods labeled for network policies.
  - Access to the Kubernetes API.
- **Dynamic Mapper:**
  - Cilium and Hubble installed in the Kubernetes cluster.
  - Hubble relay service accessible via port forwarding.

  
* **Cilium Hubble**: 
  * Follow the [Cilium Hubble documentation](https://github.com/cilium/hubble) to set up and configure Hubble for use with your Kubernetes cluster. Ensure that the Hubble relay service is accessible and operational to enable dynamic topology mapping.
  * For further information, see references below.



## Directory Structure
```
.
├── static_mapper.py          # Extracts static topology data
├── dynamic_mapper.py         # Captures dynamic topology data
```


## Usage

### Static Mapper
* To generate the static topology mapping, run the `run_topology_creation()` function in the `static_mapper.py` script. 
  * This function starts a `kubectl proxy`, configures the Kubernetes API client, and creates the mapping.

* **Output:**
A CSV with static topology detail is saved in the designated assets' directory.

### Dynamic Mapper
* To execute the dynamic mapper, run the `run_full_script(dir_path, out_hubble)` function. This function performs:
  1. Downloading of Hubble dependencies.
  2. Establishing a `kubectl port-forward` for the Hubble relay service.
  3. Observing network flows using Hubble.
  4. Processing the observed data into a CSV file named `sub_graph_topology.csv`.

* **Output:**
A CSV file with dynamic topology data is saved in the specified directory.


## References

* [Cilium Hubble - GitHub](https://github.com/cilium/hubble)
* [Network Observability with Hubble - Cilium Documentation](https://docs.cilium.io/en/stable/observability/hubble/)
