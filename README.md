# BFT2f Algorithm Implementation

## Overview

This project implements the **BFT2f algorithm**, an extension of the PBFT (Practical Byzantine Fault Tolerance) algorithm, designed to tolerate Byzantine failures in distributed systems. The implementation is provided as a Python library that supports system liveness and consistency under various fault scenarios.
---

## Features

- **Byzantine Fault Tolerance:** Tolerates up to `f` faulty replicas while ensuring liveness and consistency.
- **Graceful Degradation:** Limits malicious impact when failures exceed `f` but are less than or equal to `2f`.
- **Modular Design:** Separate components for replicas, clients, and message types.
- **Automated Testing:** Extensive tests for unit and scenario-based validations.
- **Hash Chain Integrity:** Ensures operation sequence consistency and security.

---

## Scenarios

1. **Up to `f` Replicas Fail:**
   - Full liveness and consistency are maintained.
2. **Failures Between `f` and `2f`:**
   - Constrained malicious behavior with potential minor consistency violations.
3. **More than `2f` Failures:**
   - System behavior may be compromised, requiring external intervention.

---

## Requirements

### Prerequisites

- **Python 3.8+**
- Optional: **Git**

### Dependencies

No external libraries are required; all necessary components are part of Python's standard library.

---

## Setup and Usage

### Installation

1. Clone the repository:
   ```bash
   git clone https://dvcs.apice.unibo.it/pika-lab/courses/ds/projects/ds-project-pacilli-pieri-ay2324
   cd ds-project-pacilli-pieri-ay2324
   ```

2. Install dependencies (if any future dependencies are added):
    ```bash
    pip install -r requirements.txt
    ```
3. Configure your environment to recognize the library path:
   - **VSCode**
     ```json
     "python.analysis.extraPaths": ["path_to/BFT2F_library"]
     ```
   - **Command Line**
     ```bash
     export PYTHONPATH=$PYTHONPATH:/path_to/BFT2F_library
     ```
### Running the software
1. Initialize a client and a replica in a Python script:
   ```python
   from BFT2F_library.client import Client
   from BFT2F_library.replica import Replica
      
   client = Client(host="localhost", port=6000, f=1)
   replica = Replica(host="localhost", port=5000, f=1)
   ```
3. Trigger the client request:
   ```python
   client.make_request('log in')
   ```

--- 
## Testing
1. Run unit tests:
   ```bash
   python -m unittest <test_filename>.py
   ```
3. Run scenario-based tests:
   ```bash
   python <filename>.py
   ```
---

## Authors
Benedetta Pacilli - benedetta.pacilli@studio.unibo.it <br/>
Valentina Pieri - valentina.pieri5@studio.unibo.it

---

## References
- Miguel Castro and Barbara Liskov, Practical Byzantine Fault Tolerance, OSDI '99. 
- Jinyuan Li and David Mazières, Beyond One-Third Faulty Replicas in Byzantine Fault Tolerant Systems, NSDI 2007.
