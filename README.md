# CORAL: Container Online Risk Assessment with Logical Attack Graphs
CORAL is a framework for continuous risk assessment of containerized environments using logical attack graphs. It efficiently identifies attack paths between containers without requiring graph rebuilding when the underlying architecture changes.

Learn more about CORAL in our published paper: [CORAL: Container Online Risk Assessment with Logical attack graphs](https://kwnsfk27.r.eu-west-1.awstrack.me/L0/https:%2F%2Fauthors.elsevier.com%2Fc%2F1kMqxc43v4Os7/1/0102019423793f90-7424c711-8ad0-4cd6-ab96-a0e6ce5bbf0a-000000/yclPzElDHU4wqmI8CXViq8q8IYI=407)

## Features
* Dynamic risk assessment for container environments using live attack graphs
* Efficient reuse of generated attack graphs through intelligent graph similarity detection
* Attack path risk evaluation model to identify and highlight the riskiest paths
* Support for large-scale container deployments (tested with up to 2,802 pods)
* Integration with Kubernetes environments
* Detection of lateral movement attacks using provenance graphs

## Architecture

CORAL consists of four main modules that work together to provide continuous risk assessment:

<img src="docs/CoralArchitecture.png" style="vertical-align:middle" alt="architecture" > 


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
* Performs vulnerability scanning using [Trivy](https://trivy.dev/latest/)
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

### 4. Attack Graph Analyzer
* Analyzes generated attack graphs to identify risks and attack paths
* Calculates risk scores for containers and attack paths
* Provides risk prioritization for vulnerability remediation
* Highlights critical attack paths requiring attention
* Integrates with provenance data for lateral movement detection

## Prerequisites

- Python 3.8+
- Kubernetes cluster
- [Trivy vulnerability scanner](https://trivy.dev/latest/)
- [Hubble for monitoring](https://github.com/cilium/hubble)

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure access:
   - Ensure kubectl is configured with cluster access
   - Configure Hubble for container monitoring
   - Set up Trivy for vulnerability scanning

## Directory Structure

```
├── attack_graph_analyzer/     # Attack graph analysis tools
├── docs/                      # Documentation and diagrams
├── orchestrator/              # Core orchestration logic
├── testbed/                   # Testing environment
│   ├── google-microservices-demo/  # Demo application
│   └── microservice_replication/   # Replication framework
├── topology_handler/          # Topology management
├── use_case_example_app/      # Example implementation
└── vulnerability-handler/     # Vulnerability scanning
```

## Getting Started

See individual component READMEs for detailed usage instructions:
- [Attack Graph Analyzer](attack_graph_analyzer/README.md)
- [Topology Handler](topology_handler/README.md)
- [Vulnerability Handler](vulnerability-handler/README.md)
- [Orchestrator](orchestrator/README.md)
- [Use Case Example](use_case_example_app/README.md)
- [Testbed](testbed/README.md)

## Performance

CORAL demonstrates excellent performance for large-scale deployments:
- Graph search is 2 orders of magnitude faster than regeneration
- Processes topologies with thousands of containers efficiently
- Example metrics:
  * 1,402 pods: 206 seconds for AG generation
  * Graph search in 1,000 topologies: 9.5 seconds
  * Net search time: 2.4 seconds (1% of AG generation time)

## Use Cases

CORAL supports various security use cases:
- Continuous risk assessment
- Attack path detection and prioritization
- Vulnerability mitigation planning
- Container loading decision support
- Security tool posture optimization
- Lateral movement detection
- Attack prediction


## Citation

```bibtex
@article{TAYOURI2025104296,
title = {CORAL: Container Online Risk Assessment with Logical attack graphs},
journal = {Computers & Security},
volume = {150},
pages = {104296},
year = {2025},
issn = {0167-4048},
doi = {https://doi.org/10.1016/j.cose.2024.104296},
url = {https://www.sciencedirect.com/science/article/pii/S0167404824006023},
author = {David Tayouri and Omri {Sgan Cohen} and Inbar Maimon and Dudu Mimran and Yuval Elovici and Asaf Shabtai},
keywords = {Container risk assessment, Attack graphs, Kubernetes, Vulnerability analysis, Risk exposure},
abstract = {Container-based architectures, with their highly volatile runtime configurations, rapid code changes, and dependence on third-party code, have raised security concerns. The first step in establishing solid security footing in a production application is understanding its risk exposure profile. Attack graphs (AGs), which organize the topology and identified vulnerabilities into possible attack paths as part of a larger graph, help organizations assess and prioritize risks and establish a baseline for countermeasure planning and remediation. Although AGs are valuable, their use in the container environment, where the AG must be repeatedly rebuilt due to frequent data changes, is challenging. In this paper, we present a novel approach for efficiently building container-based AGs that meets the needs of highly dynamic, real-life applications. We propose CORAL, a framework for identifying attack paths between containers, which does not require rebuilding the graph each time the underlying architecture (code or topology) changes. CORAL accomplishes this by intelligently disregarding changes that should not trigger AG build and reusing fragments of existing AGs. We propose a model to evaluate the attack paths’ risks and highlighting the riskiest path in any AG. We evaluate CORAL’s performance in maintaining an up-to-date AG for an environment with many containers. Our proposed framework demonstrated excellent performance for large topologies — searching similar topologies and reusing their AGs was two orders of magnitude faster than AG regeneration. We demonstrate how CORAL can assist in efficiently detecting lateral movement attacks in containerized environments using provenance graphs.}
}

```

