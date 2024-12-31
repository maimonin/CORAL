# Testbed

This directory is part of the CORAL framework and serves as the evaluation environment for the CORAL paper. The testbed is based on Google's "Online Boutique" cloud microservice demo and a custom microservice replication framework to test scalability and dynamic containerized environments.

It contains two primary subdirectories:
1. `google-microservices-demo`: Contains the deployment configuration for Google's "Online Boutique" application, a microservice-based e-commerce app.
2. `microservice_replication`: Hosts the framework for replicating microservices to test scalability and interconnections within a Kubernetes environment.


## Features

* **Industry Standard Demo Application:** Google's microservice-based e-commerce application for demonstrating Kubernetes technologies.
* **Deployment Configurations:** Predefined YAML files for setting up the "Online Boutique" demo application.
* **Microservice Replication:** Framework for scaling the testbed with configurable replicas.
* **Scalable Environment:** Designed to emulate operational Kubernetes environments.


## Directory Structure

```
.
├── google-microservices-demo
│   ├── deploy_and_svc_yamls         # Deployment and service YAML files
│   │   ├── adservice-yamls
│   │   ├── cartservice-yamls
│   │   ├── checkout-yamls
│   │   ├── currencyservice-yamls
│   │   ├── emailservice-yamls
│   │   ├── frontend-yamls
│   │   ├── paymentservice-yamls
│   │   ├── productcatalogservice-yamls
│   │   ├── recommendationservice-yamls
│   │   ├── redis-cart-yamls
│   │   └── shippingservice-yamls
│   └── network-policies             # Network policies for microservices
├── microservice_replication
│   ├── framework                    # Python scripts for replication
│   │   ├── hard-coded-yamls
│   │   │   ├── cartservice-yamls
│   │   │   └── redis-cart-yamls
│   │   ├── netpol-yaml-templates
│   │   ├── yamls-to-apply
│   │   │   ├── adservice-apply
│   │   │   ├── cartservice-apply
│   │   │   ├── checkoutservice-apply
│   │   │   ├── currencyservice-apply
│   │   │   ├── emailservice-apply
│   │   │   ├── frontend-apply
│   │   │   ├── paymentservice-apply
│   │   │   ├── productcatalogservice-apply
│   │   │   ├── recommendationservice-apply
│   │   │   ├── redis-cart-apply
│   │   │   └── shippingservice-apply
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
│   ├── recommendationservice_yaml.py
│   ├── redis_cart_yaml.py
│   └── shippingservice_yaml.py
```

### 1. `google-microservices-demo` Directory
This subdirectory contains the "Online Boutique" application Kubernetes configuration files. It is composed of Kubernetes deployment and networking by the following components:

* `deploy_and_svc_yamls`: YAML files for deployment and service definitions of all microservices.
* `network-policies`: YAML files for defining network policies for each microservice to control inter-service communication.

#### Online Boutique Demo Application

The ["Online Boutique"](https://github.com/GoogleCloudPlatform/microservices-demo) is a web-based e-commerce demo application consisting of 11 microservices that showcase Kubernetes (K8s) technologies. Users can browse items, add them to their cart, and make purchases. 

Key characteristics of the application:
* Simple, scalable, and dynamic.
* Built using microservices written in different programming languages.
* Communicates using gRPC (an open-source remote procedure call framework).

The application was deployed in two environments to ensure diverse testing:
* Privately managed Kubernetes cluster.
* Amazon Elastic Kubernetes Service (EKS).

### 2. `microservice_replication` Directory
This subdirectory provides a framework for replicating the microservices of the "Online Boutique" application. It allows scalability testing by creating multiple replicas with unique configurations. 
The subdirectory contains the following components:

* `framework`: Python scripts for generating replicated YAML files.
  * `yamls-to-apply`: Contains generated YAML files for the replicated microservices, organized by service.

#### Microservice Replication Framework

To simulate large-scale deployments and test interconnectivity, the testbed incorporates a replication framework. 
The replication process ensures:
* New Kubernetes services, deployments, and network policies are created for each replica. 
* Each replica has distinct environment variables (e.g., port, service name, address). 
* Complete interconnectivity between all replicated microservices.

This approach enables controlled topology changes for scalability and realistic test conditions.


## Prerequisites

* Python 3.8+

* **Computing Environment:**
  * AWS EC2 Machines: 
    * Instance Type: t3.xlarge 
      * 4 vCPUs 
      * 16 GB Memory 
      * 5 Gbps Network burst bandwidth 
    * Storage: 1 x 100 GB gp3 (general purpose SSD) Root volume 
    * Processor: Intel Xeon Scalable Processor (Skylake-SP or Cascade Lake) or AMD EPYC 7000 
    * Operating System:
      * Ubuntu 18.04 
      * Linux Kernel 5.4.0 
      * AMD (x86_64) Architecture
  * **Node Configuration:**
    * Two machines (1 master, 1 worker) for less than 50 pods.
    * Four machines (1 master, 3 workers) for more than 50 pods.

* **Kubernetes Cluster:**
  * With `kubectl` configured.
  * Self-managed with kubeadm.
  * Container Runtime Interface (CRI): containerd.
  * Container Network Interface (CNI): Calico.


## Usage

1. Setup the computing environment.

2. Setup the Kubernetes cluster.

3. Deploy the "Online Boutique" application by applying deployment and service configurations:
  ```
  kubectl apply -f google-microservices-demo/deploy_and_svc_yamls/
  kubectl apply -f google-microservices-demo/network-policies/
  ```
  For detailed information about the application, see its official repository: [Google's Microservices Demo](https://github.com/GoogleCloudPlatform/microservices-demo).

4. Replicate microservices using the Microservice Replication Framework scripts by running the main replication script:
  ```
  microservice_replication/framework/microservices_factory.py
  ```
  See framework subdirectory README for detailed usage instructions: [Microservice Replication Framework](microservice_replication/framework/README.md).

5. Deploy the replicated microservices by applying the generated YAML files:
  ```
  kubectl apply -f microservice_replication/yamls-to-apply/
  ```


## References

* [CORAL article](https://doi.org/10.1016/j.cose.2024.104296), Section 4.1 "_Testbed setup_", for additional details.
* Google's Microservices Demo GitHub repository: https://github.com/GoogleCloudPlatform/microservices-demo