# Microservice Replication Framework

The Microservice Replication Framework enables the replication of existing microservices to create scalable, functional, and interconnected applications. It ensures that all replicated microservices are reachable from a frontend and maintains critical parent-child relationships between services.


## Features
* Simplified creation of complex applications via microservice replication.
* Dynamic generation of Kubernetes YAML configurations for Services, Deployments, and Network Policies.
* Automatic validation of replication dictionaries to maintain logical microservice dependencies.
* Integration with Kubernetes for deployment and scaling.


## Architecture

The framework revolves around a replication engine that processes microservice definitions and generates corresponding Kubernetes resources. It ensures:
1. **Replication Definition**:
   - Creates a new Kubernetes Service, Deployment, and Network Policy for each replicated microservice.
   - Adjusts critical environment variables (e.g., ports, service names, addresses) to enable unique operation.
2. **Validation**:
   - Ensures parent-child consistency across microservices.
   - Prevents over-replication of child services beyond their parent dependencies.
3. **Deployment Output**:
   - Generates YAML files for immediate application to a Kubernetes cluster.
   - Outputs the topology for visualization and debugging.

### Microservice-based Application

The replication framework in the CORAL research project is based on replicating the "Online Boutique" application.  The framework extends the application's scalability and functionality by replicating its microservices and ensuring their interconnectivity.

<a href="https://github.com/GoogleCloudPlatform/microservices-demo" target="_blank">Online Boutique</a>  is a cloud-first microservices demo application. Online Boutique consists of an 11-tier microservices application. The application is a web-based e-commerce app where users can browse items, add them to the cart, and purchase them.
<img src="../../../docs/architecture-diagram.png" style="vertical-align:middle" alt="architecture" >
  
  
### General Functions 
This module (`framework_general_funcs.py`) provides foundational utilities for Kubernetes interactions, port management, and deployment visualization:

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


### Microservice Factory 
This module (`microservices_factory.py`) manages microservice replication and YAML file generation:

- **Validation**:
  - Ensures correct parent-child relationships between microservices using `validate`.
- **Replication**:
  - Dynamically generates and configures replicas for each microservice using specialized functions.
  - Supports generating environment-specific YAML configurations, handling dependencies, and managing address allocations.
- **Hardcoded Services**:
  - Prepares and integrates hardcoded microservices (e.g., `redis-cart` and `cartservice`) into the replication process.
- **Network Policies**:
  - Generates network policies based on child-to-parent service relationships using `generate_networkpolicies`.

#### Service-Specific Scripts
Each microservice in the framework has a dedicated script for generating its Kubernetes Deployment and Service YAML files. These scripts dynamically configure and create the necessary resources to deploy the microservices within the Kubernetes cluster.

Scripts for all microservices (except for hard-coded YAMLs), follow a similar pattern:
* Use templates to dynamically generate YAML configurations. 
* Handle microservice-specific parameters (e.g., ports, environment variables). 
* Ensure consistency across all replicated services.


* **For example:** `adservice_yaml.py`
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
  * Input:
    * `idx`: Index for the specific adservice replica. 
    * `used_ports`: List of currently allocated ports in the cluster. 
    * `child_to_parents_relations`: Dictionary mapping child microservices to their parent services.
  * Output:
    * Deployment and Service YAML files for the adservice in the `yamls-to-apply/adservice-apply/` directory. 
    * Returns the new microservice's address in the format label:port (e.g., adservice-1:8080).

#### Hard-Coded YAMLs Scripts
- Some microservices, such as cartservice and redis-cart, rely on predefined configurations and cannot be dynamically replicated. These microservices have fixed ports and specific requirements, making them essential components of the application. 
- Hard-coded YAMLs for cartservice and `redis-cart are included in the framework but cannot be dynamically scaled due to limitations in exposing necessary environment variables. These microservices are crucial to the functionality of the application and are handled as static components during replication.


### Network Policy Management

The framework supports the creation of Kubernetes NetworkPolicies for managing ingress traffic between microservices. It leverages templates to dynamically generate policies tailored to the replicated microservices and their dependencies.

This functionality is implemented in two scripts:

* `networkpolicies_yaml.py`
  - **Purpose**: Generates NetworkPolicy YAML files for each child microservice.
  - **Key Functionality**:
    - `create_networkpolicy`:
      - Creates NetworkPolicies for child microservices based on their parent relationships.
      - Dynamically updates the ingress rules and service port in the NetworkPolicy YAML.
      - Outputs YAML files for deployment in Kubernetes.

* `networkpolicis_yaml_separate_files.py`
  - **Purpose**: Creates separate NetworkPolicy YAML files for each parent-child microservice relationship.
  - **Key Functionality**:
    - `create_networkpolicy_seperate_files`:
      - Produces distinct YAML files for each ingress rule, ensuring a one-to-one mapping between a child microservice and its parent.
      - Adjusts template fields such as `podSelector` and ingress `ports` dynamically.

The Network Policy scripts follow the following pattern: 
  1. **Input**:
     - The child-to-parent relationships for microservices.
     - Template YAML for NetworkPolicies.
  2. **Execution**:
     - Iterates over each child microservice.
     - Creates one or more YAML files per child, based on the number of parent microservices.
  3. **Output**:
     - YAML files in the specified directory for application to the Kubernetes cluster.

  
## Prerequisites

* Python 3.8+ and required Python libraries (see `requirements.txt`)
* Kubernetes configuration files of an existing application (e.g., Online Boutique)
* Kubernetes cluster with `kubectl` configured


## Directory Structure

```
.
├── framework/
│   ├── hard-coded-yamls/
│   │   ├── cartservice-yamls/
│   │   │   ├── cartservice-deploy-1.yaml
│   │   │   ├── cartservice-svc-1.yaml
│   │   ├── redis-cart-yamls/
│   │       ├── redis-cart-deploy-1.yaml
│   │       ├── redis-cart-svc-1.yaml
│   ├── netpol-yaml-templates/
│   │   ├── netpol-template-selector.yaml
│   │   ├── netpol-template-selector0.yaml
│   │   ├── netpol-template-selector1.yaml
│   │   ├── netpol-template-selector2.yaml
│   │   ├── netpol-template-selector3.yaml
│   ├── yamls-to-apply/
│   │   ├── adservice-apply/
│   │   ├── cartservice-apply/
│   │   ├── checkoutservice-apply/
│   │   ├── currencyservice-apply/
│   │   ├── emailservice-apply/
│   │   ├── frontend-apply/
│   │   ├── paymentservice-apply/
│   │   ├── productcatalogservice-apply/
│   │   ├── recommendationservice-apply/
│   │   ├── redis-cart-apply/
│   │   ├── shippingservice-apply/
│   ├── adservice_yaml.py
│   ├── cartservice_yaml.py
│   ├── checkoutservice_yaml.py
│   ├── currencyservice_yaml.py
│   ├── emailservice_yaml.py
│   ├── framework_general_funcs.py
│   ├── frontend_yaml.py
│   ├── microservices_factory.py
│   ├── networkpolicies_yaml.py
│   ├── networkpolicis_yaml_separate_files.py
│   ├── paymentservice_yaml.py
│   ├── productcatalogservice_yaml.py
│   ├── README.md
│   ├── recommendationservice_yaml.py
│   ├── redis_cart_yaml.py
│   ├── shippingservice_yaml.py
```

  
##  Usage

1. **Provide Input Dictionary**:
   Define the replication requirements for each microservice in a 'replication dictionary', for example:
```
  rep_dict = {
      'adservice': 2,
      'productcatalogservice': 3,
      'recommendationservice': 2,
      'redis-cart': 1,
      'cartservice': 1,
      'shippingservice': 2,
      'currencyservice': 2,
      'paymentservice': 2,
      'emailservice': 1,
      'checkoutservice': 2,
      'frontend': 3
  }
```
2. **Run the Framework**:
   Execute the scripts to validate, replicate, and generate YAML files. Use the main script:
```
 microservices_factory.py
```
3. **Apply to Kubernetes**:
   Apply the generated YAML files to the Kubernetes cluster to deploy the application and enforce network policies:
```
kubectl apply -f yamls-to-apply/
```
4. **Visualize Topology**:
   Use the `draw_topology` function (under `framework_general_funcs.py`) to analyze the service topology.


### Output
- Generated YAML files for Deployments, Services, and Network Policies.
- Example directory structure:
```
├── yamls-to-apply/
│   ├── adservice-apply/
│   │   ├── adservice-deploy-1.yaml
│   │   ├── adservice-svc-1.yaml
│   ├── cartservice-apply/
│   │   ├── cartservice-deploy-1.yaml
│   │   ├── cartservice-svc-1.yaml
```

### Example for Running

#### Input
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

####  Output
YAML files for the replicated application, which depict the following architecture:

<img src="../../../docs/example%20archi.png" style="vertical-align:middle" alt="example architecture" >
