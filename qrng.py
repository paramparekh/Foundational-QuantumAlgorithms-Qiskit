from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def run_qrng(n_bits=8):
    qc = QuantumCircuit(n_bits, n_bits)
    
    for i in range(n_bits):
        qc.h(i)
        
    qc.measure(range(n_bits), range(n_bits))
    
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()
    
    return qc, counts

if __name__ == "__main__":
    qc, counts = run_qrng()
    print("Counts (Sample):", list(counts.keys())[:5])
    qc.draw('mpl').savefig('qrng_circuit.png')
    qc.draw('mpl').savefig('qrng_circuit.png')
    
    int_counts = {}
    for bitstr, count in counts.items():
        val = int(bitstr, 2)
        int_counts[val] = count
    
    plt.figure(figsize=(10, 6))
    sorted_keys = sorted(int_counts.keys())
    sorted_vals = [int_counts[k] for k in sorted_keys]
    
    plt.bar(sorted_keys, sorted_vals, color='#6F42C1', width=1.0)
    plt.title(f'QRNG Distribution (1024 shots, {8}-bit numbers)')
    plt.xlabel('Generated Integer Value (0-255)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('qrng_hist.png')
    print("Generated qrng_hist.png with integer distribution.")
