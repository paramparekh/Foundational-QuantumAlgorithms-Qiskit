from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np

def grover_oracle(target_state='101'):
    n = len(target_state)
    qc = QuantumCircuit(n)
    
    # Phase Oracle: Flip sign of |target>
    # Logic:
    # 1. Flip X on qubits that should be 0 in target (to make them 1)
    # 2. Multi-controlled Z (MCZ) or MCP(pi) effectively
    # 3. Flip X back
    
    # Apply X to '0' positions in target
    for i, char in enumerate(reversed(target_state)):
        if char == '0':
            qc.x(i)
            
    # MCZ (H -> MCX -> H on target bit? or specialized gate)
    # Qiskit has mcp or similar. Or we can just use multicontrol Z.
    # For n=2: CZ. For n=3: CCZ.
    if n == 2:
        qc.cz(0, 1)
    elif n == 3:
        # CCZ = H(t) CCX H(t)
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
    else:
        # Generic MCP
        qc.cp(np.pi, list(range(n-1)), n-1) # This might be wrong API
        pass 
        
    # Uncompute X
    for i, char in enumerate(reversed(target_state)):
        if char == '0':
            qc.x(i)
            
    return qc

def diffuser(n):
    qc = QuantumCircuit(n)
    # H
    for i in range(n):
        qc.h(i)
    # X
    for i in range(n):
        qc.x(i)
        
    # Multi-controlled Z
    if n == 2:
        qc.cz(0, 1)
    elif n == 3:
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
        
    # X
    for i in range(n):
        qc.x(i)
    # H
    for i in range(n):
        qc.h(i)
        
    return qc

def run_grover(target_state='101'):
    n = len(target_state)
    qc = QuantumCircuit(n, n)
    
    # Initialization
    for i in range(n):
        qc.h(i)
        
    # Iterations
    # Optimal iterations approx pi/4 * sqrt(N)
    # for N=4 (n=2), 1 iter.
    # for N=8 (n=3), 2 iters.
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
