# Testbed Directory


## Overview
This directory contains the testbed setup as part of CORAL's evaluation. It includes two subdirectories:

1. `google-microservices-demo`: Contains the deployment configuration for Google's "Online Boutique" application, a microservice-based e-commerce app.
2. `microservice_replication`: Hosts the framework for replicating microservices to test scalability and interconnections within a Kubernetes environment.


## Directory Structure

### 1. `google-microservices-demo`
This subdirectory contains the "Online Boutique" application Kubernetes configuration files. It is composed of Kubernetes deployment and networking by the following components:

* `deploy_and_svc_yamls`: YAML files for deployment and service definitions of all microservices.
* `network-policies`: YAML files for defining network policies for each microservice to control inter-service communication.

### 2. `microservice_replication`
This subdirectory provides a framework for replicating the microservices of the "Online Boutique" application. It allows scalability testing by creating multiple replicas with unique configurations.

#### Components
* `framework`: Python scripts for generating replicated YAML files.
* `yamls-to-apply`: Contains generated YAML files for the replicated microservices.
  * Organized by service.


## References
- Google's Microservices Demo aaplication: [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo)

---

For additional details, see the CORAL paper, Section 4.1.