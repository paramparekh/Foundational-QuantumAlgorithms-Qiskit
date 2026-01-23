from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import matplotlib.pyplot as plt

def run_bb84(n_bits=20):
    
    alice_bits = np.random.randint(2, size=n_bits)
    
    alice_bases = np.random.randint(2, size=n_bits)
    
    qc = QuantumCircuit(n_bits, n_bits)
    
    for i in range(n_bits):
        if alice_bits[i] == 1:
            qc.x(i)
            
        if alice_bases[i] == 1:
            qc.h(i)
            
    qc.barrier()
    
    bob_bases = np.random.randint(2, size=n_bits)
    
    for i in range(n_bits):
        if bob_bases[i] == 1:
            qc.h(i)
            
        qc.measure(i, i)
        
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1).result()
    counts = result.get_counts()
    
    measured_str = list(counts.keys())[0] 
    bob_bits = np.array([int(c) for c in measured_str[::-1]])
    
    matches = (alice_bases == bob_bases)
    sifted_key_alice = alice_bits[matches]
    sifted_key_bob = bob_bits[matches]
    
    return alice_bits, alice_bases, bob_bits, bob_bases, sifted_key_alice, sifted_key_bob

if __name__ == "__main__":
    a_bits, a_bases, b_bits, b_bases, key_a, key_b = run_bb84(10)
    print("Alice Bits:  ", a_bits[:20])
    print("Alice Bases: ", a_bases[:20])
    print("Bob Bases:   ", b_bases[:20])
    print("Bob Bits:    ", b_bits[:20])
    print("Sifted Key A:", key_a[:10])
    print("Sifted Key B:", key_b[:10])
    print("Match Rate:  ", np.mean(key_a == key_b))
    
    plt.figure(figsize=(6, 4))
    plt.bar(['Initial Bits', 'Sifted Key'], [len(a_bits), len(key_a)])
    plt.ylabel('Count')
    plt.title('BB84 Key Sifting')
    plt.savefig('bb84_stats.png')
