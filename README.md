# ⚛️ Foundational Quantum Algorithms

[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6F42C1.svg?style=for-the-badge&logo=qiskit&logoColor=white)](https://qiskit.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)]()

> *Exploration of fundamental quantum computing algorithms implemented using Qiskit.*

---

## 🌌 Overview

This repository contains implementations of five cornerstone algorithms in quantum computing. Each implementation demonstrates a unique quantum advantage, ranging from exponential speedups in oracle problems to hybrid quantum-classical optimization and information-theoretic cryptography.

## ⚡ Algorithms Implemented

| Algorithm | Type | Quantum Advantage | Key Concept |
|-----------|------|-------------------|-------------|
| **VQE** | Optimization | Hybrid | Variational Quantum Eigensolver to compute minimum eigenvalues of Hamiltonians. |
| **Grover's Search** | Search | Quadratic | Amplifying amplitude of target state $|w\rangle$ in $O(\sqrt{N})$ steps. |
| **Simon's Algorithm** | Oracle | Exponential | Distinguishing $1$-to-$1$ vs $2$-to-$1$ functions using period finding $f(x) = f(x \oplus s)$. |
| **Deutsch-Jozsa** | Oracle | Exponential | Determining if a function is Constant or Balanced with a single query. |
| **QKD (BB84)** | Cryptography | Info-Theoretic | Secure key exchange observing qubit polarization states $|\psi\rangle$. |

## 🛠️ Installation & Usage

To run these simulations locally and generate your own quantum reports:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/paramparekh/Foundational-QuantumAlgorithms-Qiskit.git
    cd Foundational-QuantumAlgorithms-Qiskit
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Simulations & Generate Report**
    ```bash
    python generate_report.py
    ```
    This will execute all algorithms, generate circuit/histogram images, and compile them into `index.html`.

## 🧬 Repository Structure

```
├── vqe.py             # Variational Quantum Eigensolver
├── grover.py          # Amplification of target state
├── simon.py           # Hidden subgroup problem
├── deutsch_jozsa.py   # Constant vs Balanced Oracle
├── qkd_bb84.py        # BB84 Key Distribution Protocol
├── generate_report.py # Automation script
└── index.html         # Generated dashboard
```

## 🔗 Report

Explore the interactive report with circuit diagrams, measurement histograms, and theoretical breakdowns deployed on GitHub Pages:
**[View Interactive Report Here!](https://paramparekh.github.io/Foundational-QuantumAlgorithms-Qiskit/)**

*Also check out my implementation of [Quantum Error Correction Fundamentals](https://github.com/paramparekh/Quantum-Error-Correction-Fundamentals)!*

---

<div align="center">
  <sub>Implemented with ❤️ and Superposition by Param Parekh</sub>
</div>
