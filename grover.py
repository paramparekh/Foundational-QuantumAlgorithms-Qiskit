import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def grover_oracle(marked_states):
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)
    for target in marked_states:
        rev_target = target[::-1]
        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
        qc.x(zero_inds)
        qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
        qc.x(zero_inds)
    return qc

def main():
    marked_states = ["011", "100"]
    oracle = grover_oracle(marked_states)
    grover_op = GroverOperator(oracle)
    
    optimal_num_iterations = math.floor(
        math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
    )
    
    qc = QuantumCircuit(grover_op.num_qubits)
    qc.h(range(grover_op.num_qubits))
    qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
    qc.measure_all()
    
    qc.draw(output="mpl", style="iqp").savefig('grover_circuit.png')
    
    backend = FakeFez()
    target = backend.target
    pm = generate_preset_pass_manager(target=target, optimization_level=3)
    circuit_isa = pm.run(qc)
    
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = 10_000
    job = sampler.run([circuit_isa])
    result = job.result()
    dist = result[0].data.meas.get_counts()
    
    print("Grover counts:", dist)
    plot_distribution(dist).savefig('grover_hist.png')

if __name__ == "__main__":
    main()
