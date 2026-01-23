from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np

def dj_oracle(case='balanced', n=3):
    oracle_qc = QuantumCircuit(n+1)
    
    if case == 'constant':
        if np.random.randint(2) == 1:
            oracle_qc.x(n)
    
    elif case == 'balanced':
        b_str = np.random.randint(2, size=n)
        for i in range(n):
            if b_str[i] == 1:
                oracle_qc.x(i)
        
        for i in range(n):
            oracle_qc.cx(i, n)
            
        for i in range(n):
            if b_str[i] == 1:
                oracle_qc.x(i)

    return oracle_qc

def run_dj(n=3, oracle_type='balanced'):
    qc = QuantumCircuit(n+1, n)
    
    qc.x(n)
    qc.h(n)
    
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    
    oracle = dj_oracle(oracle_type, n)
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
    qc, counts = run_dj(n=3, oracle_type='balanced')
    print("Counts:", counts)
    qc.draw('mpl').savefig('dj_circuit.png')
    plot_histogram(counts).savefig('dj_hist.png')
