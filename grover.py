from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np

def grover_oracle(target_state='101'):
    n = len(target_state)
    qc = QuantumCircuit(n)
    
    for i, char in enumerate(reversed(target_state)):
        if char == '0':
            qc.x(i)
            
    if n == 2:
        qc.cz(0, 1)
    elif n == 3:
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
    else:
        qc.cp(np.pi, list(range(n-1)), n-1)
        pass 
        
    for i, char in enumerate(reversed(target_state)):
        if char == '0':
            qc.x(i)
            
    return qc

def diffuser(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.x(i)
        
    if n == 2:
        qc.cz(0, 1)
    elif n == 3:
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
        
    for i in range(n):
        qc.x(i)
    for i in range(n):
        qc.h(i)
        
    return qc

def run_grover(target_state='101'):
    n = len(target_state)
    qc = QuantumCircuit(n, n)
    
    for i in range(n):
        qc.h(i)
        
    iters = 1 if n==2 else 2
    
    oracle = grover_oracle(target_state)
    diff = diffuser(n)
    
    for _ in range(iters):
        qc = qc.compose(oracle)
        qc = qc.compose(diff)
        
    qc.measure(range(n), range(n))
    
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()
    
    return qc, counts

if __name__ == "__main__":
    qc, counts = run_grover('101')
    print("Counts:", counts)
    qc.draw('mpl').savefig('grover_circuit.png')
    plot_histogram(counts).savefig('grover_hist.png')
