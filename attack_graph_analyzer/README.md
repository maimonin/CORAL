# Attack Graph Analyzer

The Attack Graph Analyzer is a critical module of the CORAL framework. It focuses on analyzing attack graphs (AGs) generated from container topologies to evaluate container risks and identify potential vulnerabilities. The analyzer calculates risk metrics, highlights attack paths, and provides detailed assessments of vulnerabilities within containerized environments.


## Overview

The Attack Graph Analyzer includes the following functionalities:

- Extracts and analyzes attack points and vulnerable pods from an AG.
- Assesses the risk associated with each pod based on CVEs and interactions.
- Identifies vulnerable libraries and links them to CVEs.
- Evaluates the likelihood of exploitability using external vulnerability databases such as:
  - _CISA Known Exploited Vulnerabilities Catalog_
  - _FIRST.org’s EPSS (Exploit Prediction Scoring System)_


## Features

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

### Risk Assessment:
- Computes pod risk as a product of interaction impact and exploit likelihood.
- Outputs a risk table for prioritized mitigation.



## Usage

### Running the Analyzer
To analyze attack graphs:
```bash
python AnalyzeAttackGraphs.py <input_directory>
```
- `<input_directory>`: Path to the directory containing the AG files (e.g., `VERTICES.CSV`).

### Output
The script provides:
1. A list of the number of attack points and vulnerable pods.
2. A summary of vulnerable pods including:
   - Pod name
   - Number of interactions (impact)
   - Number of CVEs
   - Highest exploit likelihood (EPSS or known exploits)
   - Overall risk score



## File Structure

- **`AnalyzeAttackGraphs.py`**: Main script for attack graph analysis.
- **`cisa_exploited_vulnerabilities/`**: Directory containing the CISA Known Exploited Vulnerabilities catalog.
- **`CveScoreFile.csv`**: Stores cached CVE scores for reuse.
