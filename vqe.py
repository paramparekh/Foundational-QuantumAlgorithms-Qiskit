import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE, NumPyEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import n_local
from qiskit.primitives import StatevectorEstimator as Estimator

def main():
    # Define Hamiltonian: B[0] Z + B[1] X
    np.random.seed(42)
    Bfield = np.random.rand(2)
    H = SparsePauliOp(['Z', 'X'], coeffs=[Bfield[0], Bfield[1]])
    
    counts = []
    values = []
    params = []
    deviation = []

    def store_intermediate_result(eval_count, parameters, mean, std):
        counts.append(eval_count)
        values.append(mean)
        params.append(parameters)
        deviation.append(std)

    # Variational Form
    var_form = n_local(H.num_qubits, "ry", "rx", "linear", reps=1, insert_barriers=True)
    var_form.draw('mpl').savefig('vqe_circuit.png')

    optimizer = COBYLA(maxiter=500, disp=True, tol=1e-6)
    estimator = Estimator()
    vqe = VQE(estimator, var_form, optimizer, callback=store_intermediate_result)
    
    # Run VQE
    vqe_result = vqe.compute_minimum_eigenvalue(H)
    
    # Exact result
    exact_result = NumPyEigensolver().compute_eigenvalues(operator=H)
    exact_energy = min(np.real(exact_result.eigenvalues))
    
    print('VQE result:', vqe_result.optimal_value, 'vs Exact:', exact_energy)

    # Convergence Plot
    plt.figure()
    plt.plot(counts, abs(exact_energy - values))
    plt.xlabel('Eval count')
    plt.ylabel('Energy diff from reference')
    plt.title('VQE Energy Convergence')
    plt.yscale('log')
    plt.legend(['Energy Gap'], loc='upper right')
    plt.savefig('vqe_convergence.png')

if __name__ == "__main__":
    main()
