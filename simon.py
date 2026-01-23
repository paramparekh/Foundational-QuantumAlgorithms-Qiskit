from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

def simons_oracle(s_str):
    n = len(s_str)
    qc = QuantumCircuit(2 * n)
    
    s = s_str[::-1] 
    
    for i in range(n):
        qc.cx(i, i + n)
        
    try:
        k = s.index('1')
        for i in range(n):
            if s[i] == '1':
                if i != k:
                    qc.cx(i, n+i)
                    qc.cx(k, n+i)
            else:
                qc.cx(i, n+i)
                
    except ValueError:
        for i in range(n):
            qc.cx(i, n+i)

    return qc

def run_simon(s_str='11'):
    n = len(s_str)
    qc = QuantumCircuit(2*n, n)
    
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    oracle = simons_oracle(s_str)
    qc = qc.compose(oracle)
    qc.barrier()
    
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    
    qc.measure(range(n), range(n))
    
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()
    
    return qc, counts

if __name__ == "__main__":
    qc, counts = run_simon('11')
    print("Counts:", counts)
    qc.draw('mpl').savefig('simon_circuit.png')
    plot_histogram(counts).savefig('simon_hist.png')
