from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import matplotlib.pyplot as plt

def run_bb84(n_bits=20):
    # Simulation of BB84
    
    # 1. Alice generates random bits
    alice_bits = np.random.randint(2, size=n_bits)
    
    # 2. Alice chooses random bases (0=Z, 1=X)
    alice_bases = np.random.randint(2, size=n_bits)
    
    # 3. Encode qubits
    # We will simulate the circuit for each qubit? 
    # Or just one big circuit? For 100 bits, 100 qubits is fine for simulator.
    
    qc = QuantumCircuit(n_bits, n_bits)
    
    for i in range(n_bits):
        # Prepare state
        # If bit=1, Apply X to make |1>
        if alice_bits[i] == 1:
            qc.x(i)
            
        # If basis=1 (X), apply H to make |+> or |->
        if alice_bases[i] == 1:
            qc.h(i)
            
    qc.barrier()
    
    # Channel: No noise in this simple demo
    
    # 4. Bob chooses random bases
    bob_bases = np.random.randint(2, size=n_bits)
    
    # 5. Bob measures
    for i in range(n_bits):
        # If basis=1 (X), apply H before Z-measurement
        if bob_bases[i] == 1:
            qc.h(i)
            
        qc.measure(i, i)
        
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1).result()
    counts = result.get_counts()
    
    # Measured bits (Bob's results)
    measured_str = list(counts.keys())[0] # String of bits '01010...'
    # Qiskit bitstring is reversed (bit 0 is rightmost)
    bob_bits = np.array([int(c) for c in measured_str[::-1]])
    
    # 6. Sifing
    # Keep bits where bases matched
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
    
    # Plotting effectiveness
    # Just a simple bar chart of Key Length vs Initial Length?
    plt.figure(figsize=(6, 4))
    plt.bar(['Initial Bits', 'Sifted Key'], [len(a_bits), len(key_a)])
    plt.ylabel('Count')
    plt.title('BB84 Key Sifting')
    plt.savefig('bb84_stats.png')
