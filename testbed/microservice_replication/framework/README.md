# Microservice Replication Framework



## Concept
* Creating a complex application by replicating existing microservices.
* All replicated microservices should function, and be reachable from a frontend.


## Original Application
<a href="https://github.com/GoogleCloudPlatform/microservices-demo" target="_blank">Online Boutique</a>  is a cloud-first microservices demo application. Online Boutique consists of an 11-tier microservices application. The application is a web-based e-commerce app where users can browse items, add them to the cart, and purchase them.

<img src="../../../docs/architecture-diagram.png" style="vertical-align:middle" alt="architecture" > 


## Framework

### Input
A dictionary describing each microservice, and it’s number of replicas.
```
rep_dict = {'adservice': 6,
            'productcatalogservice': 5,
            'recommendationservice': 6,
            'redis-cart': 1,
            'cartservice': 1,
            'shippingservice': 5,
            'currencyservice': 5,
            'paymentservice': 5,
            'emailservice': 5,
            'checkoutservice': 6,
            'frontend': 7}
```

### Validation
* Ensures that no child microservice has more replicas than its parent.
* Many parents can share the same child, but each parent uses exactly one child.

### Output
* YAML files matching the replicated application.
* These files can be applied to a Kubernetes cluster to deploy the new application.


### Replication Definition
* Each replication creates a new Kubernetes Service, Deployment, and Network Policy.
* All replicated services use the same Docker image, with adjusted environment variables, such as:
  - Port
  - Service name
  - Address
  - Children addresses
* Microservices that do not expose required environment variables, such as `redis` and `cartservice`, cannot be replicated.


## Example

### Input
```
rep_dict = {'adservice': 1,
            'productcatalogservice': 1,
            'recommendationservice': 1,
            'redis-cart': 1,
            'cartservice': 1,
            'shippingservice': 1,
            'currencyservice': 1,
            'paymentservice': 1,
            'emailservice': 1,
            'checkoutservice': 1,
            'frontend': 2}
```

###  Output
YAML files for the replicated application, which depict the following architecture:

<img src="../../../docs/example%20archi.png" style="vertical-align:middle" alt="example architecture" >


---



## Framework Components


### General Functions (`framework_general_funcs.py`)
This module provides foundational utilities for Kubernetes interactions, port management, and deployment visualization:

- **Path Management**: 
  - `get_path`: Joins relative paths to a repository path.

- **File Operations**:
  - `copy_files`: Copies files from a source to a destination.

- **Kubernetes API Integration**:
  - `config_api`: Configures the Kubernetes API client.
  - `print_deployments`: Retrieves and prints details of Kubernetes deployments.

- **Port Management**:
  - `get_used_ports`: Retrieves currently allocated ports in the Kubernetes cluster.
  - `generate_new_port`: Generates and validates a new port.

- **Topology Visualization**:
  - `draw_topology`: Visualizes the network of services based on a given topology dataframe.
  - 


### Microservice Factory (`microservices_factory.py`)
This module manages microservice replication and YAML file generation:

- **Validation**:
  - Ensures correct parent-child relationships between microservices using `validate`.

- **Replication**:
  - Dynamically generates and configures replicas for each microservice using specialized functions.
  - Supports generating environment-specific YAML configurations, handling dependencies, and managing address allocations.

- **Hardcoded Services**:
  - Prepares and integrates hardcoded microservices (e.g., `redis-cart` and `cartservice`) into the replication process.

- **Network Policies**:
  - Generates network policies based on child-to-parent service relationships using `generate_networkpolicies`.


### Network Policy Management

#### Overview
The framework supports the creation of Kubernetes NetworkPolicies for managing ingress traffic between microservices. It leverages templates to dynamically generate policies tailored to the replicated microservices and their dependencies.

#### Scripts

##### `networkpolicies_yaml.py`
- **Purpose**: Generates NetworkPolicy YAML files for each child microservice.
- **Key Functionality**:
  - `create_networkpolicy`:
    - Creates NetworkPolicies for child microservices based on their parent relationships.
    - Dynamically updates the ingress rules and service port in the NetworkPolicy YAML.
    - Outputs YAML files for deployment in Kubernetes.

##### `networkpolicis_yaml_separate_files.py`
- **Purpose**: Creates separate NetworkPolicy YAML files for each parent-child microservice relationship.
- **Key Functionality**:
  - `create_networkpolicy_seperate_files`:
    - Produces distinct YAML files for each ingress rule, ensuring a one-to-one mapping between a child microservice and its parent.
    - Adjusts template fields such as `podSelector` and ingress `ports` dynamically.

#### Process
1. **Input**:
   - The child-to-parent relationships for microservices.
   - Template YAML for NetworkPolicies.

2. **Execution**:
   - Iterates over each child microservice.
   - Creates one or more YAML files per child, based on the number of parent microservices.

3. **Output**:
   - YAML files in the specified directory for application to the Kubernetes cluster.


---


## Service-Specific Scripts
Each microservice in the framework has a dedicated script for generating its Kubernetes Deployment and Service YAML files. These scripts dynamically configure and create the necessary resources to deploy the microservices within the Kubernetes cluster.

**For example:**

### `adservice_yaml.py`

* Purpose:
  * Manages the creation of YAML files for the adservice microservice.
  * Configures Deployment and ClusterIP Service resources.

* Key Functionality:
  * `create_adservice_yamls`: 
    * Generates a Deployment YAML file with:
      * Unique metadata.name and matchLabels. 
      * Updated containerPort and environment variables. 
      * Configured readinessProbe and livenessProbe. 
    * Creates a Service YAML file with:
      * Unique metadata.name and selector. 
      * Configured port and targetPort. 
      * Ensures the service is added to the used ports list and updates child-to-parent relations for network policies.
      * 
* Inputs:
  * `idx`: Index for the specific adservice replica. 
  * `used_ports`: List of currently allocated ports in the cluster. 
  * `child_to_parents_relations`: Dictionary mapping child microservices to their parent services.

* Output:
  * Deployment and Service YAML files for the adservice in the `yamls-to-apply/adservice-apply/` directory. 
  * Returns the new microservice's address in the format label:port (e.g., adservice-1:8080).

### General Note on Service-Specific Scripts
Scripts for other microservices, follow a similar pattern:

* Use templates to dynamically generate YAML configurations. 
* Handle microservice-specific parameters (e.g., ports, environment variables). 
* Ensure consistency across all replicated services.

### Scripts for Hard-Coded YAMLs
Some microservices, such as cartservice and redis-cart, rely on predefined configurations and cannot be dynamically replicated. These microservices have fixed ports and specific requirements, making them essential components of the application.

Hard-coded YAMLs for cartservice and `redis-cart are included in the framework but cannot be dynamically scaled due to limitations in exposing necessary environment variables. These microservices are crucial to the functionality of the application and are handled as static components during replication.


---



## Workflow
1. **Provide Input Dictionary**:
   Define the replication requirements for each microservice in `rep_dict`.

2. **Run the Framework**:
   Execute the scripts to validate, replicate, and generate YAML files.

3. **Apply to Kubernetes**:
   Use the generated YAML files to deploy the application and enforce network policies.

4. **Visualize Topology**:
   Use the `draw_topology` function to analyze the service topology.

---
