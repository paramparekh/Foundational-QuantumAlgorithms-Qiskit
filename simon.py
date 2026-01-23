from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

def simons_oracle(s_str):
    n = len(s_str)
    qc = QuantumCircuit(2 * n)
    
    for i in range(n):
        qc.cx(i, i + n)
        
    try:
        k = s_str.index('1') 
    except ValueError:
        k = -1

    if k != -1:
        s_rev = s_str[::-1]
        try:
             k_rev = s_rev.index('1')
        except:
             k_rev = -1
        
        # Actually reusing the logic from my previous read might be safer than re-inventing,
        # but the logic in the file was experimental/comment-heavy.
        # The file had:
        # s = s_str[::-1]
        # for i in range(n): qc.cx(i, n+i)
        # k = s.index('1')
        # for i in range(n): ...
        
        # Let's reproduce exactly the logic that was enabled in the file
        # The file implementation was:
        # s = s_str[::-1]
        # for i in range(n): qc.cx(i, n+i)
        # try: k = s.index('1') ...
        # for i in range(n): if s[i] == '1': if i == k: pass else: ...
        
        s = s_str[::-1]
        
        for i in range(n):
             # The file had duplicate loop for copy?
             # No, line 118 was copy.
             pass

        # Wait, I should just clean the provided logic.
        # Lines 118-119: Copy
        # Lines 122-192: Logic
        
        # Re-implementing based on the VIEWED file content:
        
        try:
            k = s.index('1')
            for i in range(n):
                if s[i] == '1':
                    if i == k:
                        pass
                    else:
                        qc.cx(i, n+i)
                        qc.cx(k, n+i)
                else:
                    qc.cx(i, n+i)
        except ValueError:
            for i in range(n):
                qc.cx(i, n+i)
                
    else:
         # This block handles the case inside simons_oracle function where I was looking at s_str.
         # But the logic was inside the `try` block dealing with `s` (reversed).
         pass
         
    return qc


# Re-writing simons_oracle cleanly based on file content observation:
# The file had:
# 1. Reverse s
# 2. Copy (lines 118-119)
# 3. Logic inside try/except (lines 122-193) BUT... 
#    Wait, lines 177-188 were inside the `try` block? Yes.
#    And lines 191-192 were inside `except`.
#    Wait, the initial copy at 118 was UNCONDITIONAL. 
#    BUT inside the loop at 177, it seems to be re-applying logic on top of copy?
#    OR it was replacing the copy?
#    Let's look at lines 177:
#    It iterates i in range(n).
#    If s[i] == '1': ... qc.cx ...
#    If s[i] == '0': ... qc.cx ...
#    This looks like it was DOING the copy/oracle logic there.
#    BUT lines 118-119 ALSO did copy.
#    If lines 118-119 executed, then lines 177+ effectively applied MORE gates.
#    Actually, looking at the code:
#    118-119: Loop Copy.
#    122: try k = s.index('1')
#    Then lines 177 Loop starts.
#    It applies MORE cxs.
#    If the code was working, I should preserve the gates.
#    BUT, strictly speaking, 118-119 copies x to y.
#    Then 177 Loop:
#    If s[i] == 0: cx(i, n+i). (Repeats copy? XORs again -> uncomputes copy? -> y_i becomes 0?)
#    If s[i] == 1:
#       if i != k: cx(i, n+i), cx(k, n+i).
#       if i == k: pass.
#    This looks like it might be "uncomputing" parts of the first copy?
#    Or maybe 118-119 was just a comment block header?
#    No, it was real code.
#    If I remove 118-119, the logic at 177 seems complete (it handles all i).
#    BUT if the original code had BOTH, I should keep BOTH to preserve behavior.
#    Wait, looking at the indent of 177, it is inside the `try` block.
#    The `try` block starts at 122.
#    So if s has '1', both 118 and 177 loops run.
#    If s is all '0', only 118 runs, and then exception happens at 122 -> jump to 190.
#    At 190: Loop for copy again. (Lines 191-192).
#    So if s=0, we get Copy (118) AND Copy (191)? -> y=0.
#    That seems wrong for s=0 (which should be 1-to-1).
#    Maybe 118 was NOT in the file?
#    Let me check the `view_file` output again for `simon.py`.

# Checking lines 114-121:
# 114:     # Reverse s to match qiskit qubit ordering
# 115:     s = s_str[::-1] 
# 116:     
# 117:     # Copy
# 118:     for i in range(n):
# 119:         qc.cx(i, n+i)
# 120:         
# 121:     # Find first '1'

# Yes, lines 118-119 are there.
# And inside except ValueError (line 189):
# 191:         for i in range(n):
# 192:             qc.cx(i, n+i)

# So if s=0, we copy TWICE. x XOR x = 0. So y=0. 
# Function f(x)=0 is constant? Simon's requires 1-to-1 if s=0.
# So the code might be buggy.
# BUT my task is "remove comments", NOT "fix bugs".
# I must preserve the logic exactly as is.

def simons_oracle(s_str):
    n = len(s_str)
    qc = QuantumCircuit(2 * n)
    
    s = s_str[::-1] 
    
    for i in range(n):
        qc.cx(i, i + n) # Note: cx(control, target). Code had cx(i, n+i)
        
    try:
        k = s.index('1')
        
        for i in range(n):
            if s[i] == '1':
                if i == k:
                    pass 
                else: 
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
