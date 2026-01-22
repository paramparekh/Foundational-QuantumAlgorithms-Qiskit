from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

def simons_oracle(s_str):
    """
    Generates a Simon's oracle for a hidden string s.
    """
    n = len(s_str)
    qc = QuantumCircuit(2 * n)
    
    # Copy first n qubits to second n qubits (CNOTs)
    for i in range(n):
        qc.cx(i, i + n)
        
    # If s has a 1 at index j, find the first 1 at index k (k < j)
    # and XOR the second register bit j with bit k.
    # A simpler oracle: 1-to-1 mapping if s=00..0, 2-to-1 if s != 0.
    # To ensure f(x) = f(x ^ s), we can just XOR the second register
    # with s if the standard copy happened ?
    # Let's use a standard construction for specific s.
    
    # Construction:
    # 1. Copy x to y: |x>|0> -> |x>|x>
    # 2. XOR masked bits? 
    # A robust way:
    # f(x) = x if we want 1-to-1 (s=0)
    # But for s!=0, we need f(x) = f(x^s).
    # Strategy: Find lowest index k where s[k] = '1'. 
    # For all i != k, output x_i.
    # For i == k, output x_k XOR (x dot s). This doesn't strictly work easily.
    
    # Better standard construction:
    # 1. Send x to y.
    # 2. If s is not all zeros:
    #    Find the MSB of s (say index m).
    #    For every other index j where s[j] == '1', CNOT x_m -> y_j.
    #    This ensures colliding inputs map to same output?
    #    Let's check: x and x^s.
    #    They differ at bits where s is 1.
    #    This construction is specific. Let's stick to a known correct one.
    
    # Simple Random Permutation/Matrix approach is hard to code generically in small script without advanced linear algebra helpers.
    # Let's use a simple hardcoded or logical construction.
    # If s = "11" (n=2).
    # pairs: 00 & 11, 01 & 10.
    # map 00->00, 11->00. 01->01, 10->01.
    # This works.
    
    # General construction from Qiskit textbook examples often uses:
    # Copy contents, then for 1 in s, start CNOTs.
    
    # Let's assume s is provided. 
    # We'll implement a specific oracle logic for the demo or a general one.
    # General one:
    # 1. CNOT x_i to y_i for all i. 
    # 2. Find first '1' in s at index k.
    # 3. For all j > k where s[j] == '1': CNOT x_k to y_j. (XORing the "control" bit into others)
    # 4. Special handling might be needed to really mask it 2-to-1.
    
    # Actually, standard example: 
    # f(x) should be such that f(x) = f(x + s).
    # Let k be the first index where s_k = 1.
    # We output x_i for i != k, and constant 0 (or dependent) for x_k?
    # If we drop the k-th bit of output, we get 2^(n-1) unique outputs. Every pair (x, x+s) maps to same.
    # Yes.
    
    # Implementation:
    # 1. Copy x to y. (CNOTs)
    # 2. Find first k such that s[k] == '1'.
    # 3. For this k, we want to "erase" information about x_k vs x_k ^ 1.
    #    Actually simple way: Do NOT copy x_k to y_k. And for any other j where s[j]=1, we CNOT x_k -> y_j to mix it in?
    #    Let's just output x with the k-th bit XORed into other s-bits?
    
    # Let's go with the Qiskit Textbook approach for s='11' etc.
    # "We copy the first n qubits to the second n qubits using CNOT gates."
    # "Use the first 1-bit in s as a control to flip the others?"
    
    # Correct robust algorithm for oracle construction:
    # 1. Create a matrix M of rank n-1 such that M*s = 0.
    # 2. The function is x -> Mx.
    # This is easy to implement.
    # Output y = x transformed by some CNOTs to reduce rank?
    # Actually, simpler:
    # Find first k where s[k] = '1'. 
    # For all i, if i == k, do nothing (output qubit remain 0? No, that loses injectivity for limit case).
    # We want 2-to-1.
    # Map x to y.
    # For every j such that s[j] == 1 and j != k:
    #   CNOT(x_k, y_j)
    # And finally, we need to ensure x_k is not revealed?
    # CNOT(x_k, y_k) ??
    # If we just do CNOT x_k -> y_j for all j where s_j=1, it doesn't quite work.
            
    # Let's stick to the simplest working version for a report:
    # Hardcode s='11' for 2 qubits as default demo often used.
    # s=11: x0,x1. 00->00, 11->00, 01->10, 10->10? (No)
    # 00->00, 11->00
    # 01->01, 10->01 
    # This means y0 = x0+x1, y1 = x0+x1 ? No that's 1 bit output.
    
    # Let's trust the standard "Qiskit Textbook" style oracle for s='11'
    # qc.cx(0, 2)
    # qc.cx(0, 3)
    # qc.cx(1, 2)
    # qc.cx(1, 3)
    # ... this produces XOR sum. Not quite.
    
    # Plan: Just implement the main algorithm shell and a working oracle "Simons Oracle"
    pass

    # Reverse s to match qiskit qubit ordering
    s = s_str[::-1] 
    
    # Copy
    for i in range(n):
        qc.cx(i, n+i)
        
    # Find first '1'
    try:
        k = s.index('1')
        # For all j where s[j] == 1, CNOT k to j in the second register?
        # Actually, simply XORing bit k of second register with all other bits j where s[j]=1 
        # effectively links them.
        # But we need to destroy information about x_k.
        # To make it 2-to-1:
        # We need y to be the same for x and x+s.
        # If we take the copy y = x.
        # y + s = x + s. We want y(x) = y(x+s).
        # This implies standard bitwise operations.
        
        # Let's use the standard "reduction" method.
        # Use CNOTs to make the output invariant under XORing input by s.
        # If s has a 1 at k. 
        # For every j != k such that s[j] == '1':
        #   CNOT(n+k, n+j) (target is second register)
        # Then we measure second register? 
        # Simon's algorithm measures the FIRST register. The second is auxiliary.
        # We just need the oracle to populate the second register such that |x>|0> -> |x>|f(x)> 
        # where f(x) = f(x+s).
        
        # Simple construction:
        # 1. CNOT x_i -> y_i for all i.
        # 2. Find first k where s_k = 1.
        # 3. CNOT x_k -> y_k (Result: y_k = x_k). 
        # 4. For any OTHER m where s_m = 1: CNOT x_k -> y_m. 
        #    Now y_m = x_m + x_k.
        #    If input is x+s: (x+s)_m = x_m + 1. (x+s)_k = x_k + 1.
        #    New y_m = (x_m + 1) + (x_k + 1) = x_m + x_k. (XOR rule: 1+1=0).
        #    So y_m is invariant!
        # 5. What about y_k? We have y_k = x_k.
        #    Input x+s -> y_k' = x_k + 1.
        #    This is NOT invariant. 
        #    We must NOT output x_k in the k-th position?
        #    We can just not "read" it or overwrite it?
        #    We can XOR y_k with itself? No.
        #    We need f(x) to NOT depend on the bit that flips.
        #    If s='1...', bit 0 is the pivot.
        #    We simply DO NOT Copy x_k to y_k?
        #    If we don't copy x_k to y_k, y_k=0.
        #    Then y is invariant? 
        #    Wait, y_m = x_m + x_k?
        #    Input x: y_m = x_m + x_k
        #    Input x+s: y_m' = (x_m+1) + (x_k+1) = x_m + x_k. Invariant.
        #    So for all m where s_m=1 (m!=k), y_m is invariant.
        #    For m where s_m=0, y_m = x_m. Input x+s -> s_m=0 -> x_m'=x_m. Invariant.
        #    So the strategy is:
        #    - Find pivot k (first 1 in s).
        #    - For all i:
        #        if s[i] == '0': copy x_i to y_i (CNOT x_i, y_i)
        #        if s[i] == '1' and i != k: copy x_i to y_i (CNOT x_i, y_i) AND CNOT x_k to y_i.
        #        if i == k: Do nothing to y_k (leave 0).
        #    This makes y invariant under flipping the bits set in s (tied to k).
        
        for i in range(n):
            if s[i] == '1':
                if i == k:
                    pass # Leave y_k as 0
                else: 
                    # y_i = x_i + x_k
                    qc.cx(i, n+i)
                    qc.cx(k, n+i)
            else:
                # y_i = x_i
                qc.cx(i, n+i)
                
    except ValueError:
        # s is all zeros, 1-to-1 mapping. Just copy.
        for i in range(n):
            qc.cx(i, n+i)

    return qc

def run_simon(s_str='11'):
    n = len(s_str)
    # Circuit: 2n qubits. n clbits.
    qc = QuantumCircuit(2*n, n)
    
    # 1. Hadamard on first n
    for i in range(n):
        qc.h(i)
        
    # 2. Oracle
    qc.barrier()
    oracle = simons_oracle(s_str)
    qc = qc.compose(oracle)
    qc.barrier()
    
    # 3. Measure second n (optional in some implementations, but good to simulate 'query')
    # Standard Simon's: We actually just measure the first n after another H.
    # The second register measurement is often omitted or just traced out.
    
    # 4. Hadamard on first n
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    
    # 5. Measure first n
    qc.measure(range(n), range(n))
    
    # Run
    simulator = Aer.get_backend('aer_simulator')
    # Transpile
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=1024).result()
    counts = result.get_counts()
    
    return qc, counts

if __name__ == "__main__":
    qc, counts = run_simon('11')
    print("Counts:", counts)
    qc.draw('mpl').savefig('simon_circuit.png')
    plot_histogram(counts).savefig('simon_hist.png')
