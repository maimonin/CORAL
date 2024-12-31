# Attack Graph Analyzer

The Attack Graph Analyzer is a critical module of the CORAL framework. It focuses on analyzing attack graphs (AGs) generated from container topologies to evaluate container risks and identify potential vulnerabilities. The analyzer calculates risk metrics, highlights attack paths, and provides detailed assessments of vulnerabilities within containerized environments.


## Features

- **Attack Point Analysis:** Counts potential entry points for attackers. 
- **Vulnerability Assessment:** Identifies vulnerable containers and their associated libraries and CVEs. 
- **Interaction Mapping:** Measures the interactions of each container in the topology. 
- **Risk Calculation:** Combines interaction data with exploit likelihood scores to assess container risks. 
- **CVE Likelihood Scoring:** Integrates with external data sources (e.g., FIRST.org's EPSS and CISA) to calculate the likelihood of CVE exploitation.

### Key Metrics Analyzed:

1. **Attack Points**:
   - Identifies entry points an attacker could exploit.
   - Counts `hacl()` interaction rules from AG files.

2. **Vulnerable Pods**:
   - Finds pods exposed to external threats.
   - Analyzes `vulnerablePod()` nodes in the AG.

3. **Pod Interactions**:
   - Determines the number of interactions each pod has.
   - Based on `dataFlow()` relations in the AG.

4. **Libraries and CVEs**:
   - Maps libraries to CVEs using `residesOn()` and `vulExists()` rules in the AG.

5. **Exploitability Likelihood**:
   - Checks if a CVE has a known exploit using CISA.
   - Uses EPSS for CVE exploitability scoring when no known exploit is found.


## Prerequisites
- Python 3.8+
- Required Python packages:
  - statistics
  - requests
- CSV files containing attack graph data:
  - VERTICES.CSV: Nodes of the attack graph. 
  - known_exploited_vulnerabilities.csv: Known vulnerabilities dataset from CISA. 
- Internet access for fetching CVE likelihood scores from FIRST.org.


## Usage

### Example for Running

1. Prepare the input directory:
   - Place VERTICES.CSV in the specified input directory (e.g., `AttackGraphs/AG-11Services`). 
   - Include known_exploited_vulnerabilities.csv in the cisa_exploited_vulnerabilities/ directory.

2. To analyze attack graphs, run the script:
```
AnalyzeAttackGraphs.py
```

3. View the output:
   - Detailed analysis will be printed to the console. 
   - Includes lists of attack points, vulnerable pods, their interactions, CVEs, and risk assessments.


### Output
The script provides summarized results, including:
1. A list of the number of attack points and vulnerable pods.
2. A summary of risk assessment for each vulnerable pod based on interactions and exploit probabilities  including:
   - Pod name
   - Number of interactions (impact)
   - Number of CVEs
   - Highest exploit likelihood (EPSS or known exploits)
   - Overall risk score
