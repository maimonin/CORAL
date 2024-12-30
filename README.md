# CORAL: Container Online Risk Assessment with Logical Attack Graphs
CORAL is a framework for continuous risk assessment of containerized environments using logical attack graphs. It efficiently identifies attack paths between containers without requiring graph rebuilding when the underlying architecture changes.

## Features
* Dynamic risk assessment for container environments using live attack graphs
* Efficient reuse of generated attack graphs through intelligent graph similarity detection
* Attack path risk evaluation model to identify and highlight the riskiest paths
* Support for large-scale container deployments (tested with up to 2,802 pods)
* Integration with Kubernetes environments
* Detection of lateral movement attacks using provenance graphs

## Architecture

CORAL consists of four main modules that work together to provide continuous risk assessment:

### 1. Topology Handler
Manages container topology information through two submodules:
* Static Mapper:
  * Scans container configurations and policy files
  * Creates static topology using K8s Python Client
  * Extracts pod information and network policies
  * Generates topology in CSV format with Pod-ID, IP, and Pod-Inbound-List
  * Translates topology into MulVAL facts

* Dynamic Mapper:
  * Monitors real-time communication between pods using [Hubble](https://github.com/cilium/hubble)
  * Creates dynamic topology based on actual container interactions
  * Analyzes topology changes that could affect attack surface
  * Determines when to trigger new attack graph generation
  * Handles pod updates and connection changes

### 2. Vulnerability Handler
* Performs vulnerability scanning using Trivy
* Identifies known vulnerabilities (CVEs) in K8s clusters
* Outputs comprehensive vulnerability data including:
  * Pod identification
  * Software versions
  * CVE IDs
  * Severity levels
  * CVSS scores

### 3. Orchestrator
* Core component managing attack graph generation and optimization
* Implements efficient graph generation through:
  * Division of topology into non-intersecting zones
  * Storage and reuse of generated attack graphs
  * Graph similarity detection using embedding techniques
  * Jaccard similarity coefficient for precise comparison
* Manages database of stored attack graphs
* Determines when to generate new graphs vs reuse existing ones

