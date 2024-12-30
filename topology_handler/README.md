# Topology Handler Component

The **Topology Handler** is a component of the CORAL architecture. It is responsible for mapping and analyzing Kubernetes cluster topology by integrating static and dynamic information about pods, network policies, and services. This component consists of two submodules:

1. **Static Mapper**
2. **Dynamic Mapper**

---

## Submodules Overview

### 1. Static Mapper
The **Static Mapper** creates a detailed topology map of Kubernetes pods and their network policies. It focuses on extracting static information from the cluster, such as pod metadata, IP addresses, protocols, ports, and associated network policies.

#### Key Features:
- Generates topology details, including:
  - Pod-ID
  - IP
  - Pod-Inbound-List (tuple of Pod-ID, Protocol, Port)
  - Protocol
  - Port
- Exports the results to a structured CSV file for further analysis.
- Integrates with Kubernetes via its Python client.

#### Usage:
To generate the static topology mapping, run the `run_topology_creation()` function. This function starts a `kubectl proxy`, configures the Kubernetes API client, and creates the mapping.

**Output:**
A CSV file named `topology_mapping_static.csv` is saved in the designated assets directory.

---

### 2. Dynamic Mapper
The **Dynamic Mapper** captures live network data using Cilium Hubble, processes this data, and generates a dynamic topology map. It supplements the static mapping by adding real-time insights into pod interactions.

#### Key Features:
- Captures live traffic data using Hubble.
- Processes network flows to extract details like protocol, source/target names, and ports.
- Combines processed data into a structured format with similar attributes as the static mapper.
- Adds special rows for key services like `frontend`.
- Exports the processed data to a CSV file.

#### Usage:
To execute the dynamic mapper, run the `run_full_script(dir_path, out_hubble)` function. This function performs:
1. Downloading Hubble dependencies.
2. Establishing a `kubectl port-forward` for the Hubble relay service.
3. Observing network flows using Hubble.
4. Processing the observed data into a CSV file named `sub_graph_topology.csv`.

**Output:**
A CSV file with dynamic topology data is saved in the specified directory.

---

## Prerequisites

### Common Requirements:
- Python 3.x
- Kubernetes Python Client
- Pandas library
- Cilium Hubble CLI installed and configured
- Permissions to access Kubernetes API and Hubble relay service

### Static Mapper:
- Kubernetes cluster with pods labeled for network policies.
- Access to the Kubernetes API.

### Dynamic Mapper:
- Cilium and Hubble installed in the Kubernetes cluster.
- Hubble relay service accessible via port forwarding.

---

## File Structure

- **static_mapper.py**: Contains functions for extracting static topology information.
- **dynamic_mapper.py**: Contains functions for capturing and processing live network flows.
- **Output Files**:
  - `topology_mapping_static.csv` (static data)
  - `sub_graph_topology.csv` (dynamic data)

---

