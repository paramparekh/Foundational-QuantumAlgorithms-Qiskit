from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def run_qrng(n_bits=8):
    # We can generate one bit at a time or n bits at once.
    # To be "true" RNG, we just measure |+> state.
    qc = QuantumCircuit(n_bits, n_bits)
    
    for i in range(n_bits):
        qc.h(i)
        
    qc.measure(range(n_bits), range(n_bits))
    
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    # Just one shot if we want a random number k bits long.
    # Or 1000 shots to show distribution is uniform.
    result = simulator.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()
    
    return qc, counts

if __name__ == "__main__":
    qc, counts = run_qrng()
    print("Counts (Sample):", list(counts.keys())[:5])
    qc.draw('mpl').savefig('qrng_circuit.png')
    plot_histogram(counts).savefig('qrng_hist.png')
