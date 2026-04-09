# import packages

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

# first variational form and Z measurement

def get_var_formZ(params):

    qr = QuantumRegister(1, name="q")

    cr = ClassicalRegister(1, name='c')

    qc = QuantumCircuit(qr, cr)

    qc.u(params[0], params[1], params[2], qr[0])

    qc.measure(qr,cr)

    return qc

# variational form and X measurement

def get_var_formX(params):

    qr = QuantumRegister(1, name="q")

    cr = ClassicalRegister(1, name='c')

    qc = QuantumCircuit(qr, cr)

    qc.u(params[0], params[1], params[2], qr[0])

    qc.h(qr[0])

    qc.measure(qr,cr)

    return qc

from qiskit.circuit import Parameter

theta1 = Parameter('θ1')

theta2 = Parameter('θ2')

theta3 = Parameter('θ3')

ex_qc=get_var_formX([theta1,theta2,theta3])

ex_qc.draw('mpl')

ex_qc=get_var_formZ([theta1,theta2,theta3])

ex_qc.draw('mpl')

# proability distribution P(0) and P(1)

def get_probability_distribution(counts):

    mysum=sum([v for  v in counts.values()])

    keys=['0','1']

    output_distr =[]

    for key in keys:

        if key not in counts.keys():

            output_distr.append(0)

        else:

            output_distr.append(counts[key]/mysum)

    return output_distr

# choose backend to be the simulator

from qiskit_aer import AerSimulator 

backend_sim = AerSimulator()

NUM_SHOTS = 20000

# define energy for Hamiltonian - B[0] sigma_z - B[1] sigma_x

# B is a list of two objects B=[Bz, Bx]

def energy(output_distrZ,output_distrX,B):

    cost = -B[0]*(output_distrZ[0] -output_distrZ[1])-B[1]* (output_distrX[0] -output_distrX[1])

    return cost

# the objective function is to evaluate the energy cost by running the quantum circuits

def objective_function(params,B):

    # Obtain quantum circuit instances from the paramters

    qc1 = get_var_formZ(params)

    qc2 = get_var_formX(params)

    # Execute the quantum circuit to obtain the probability distribution associated with the current parameters

    runjob = backend_sim.run([qc1, qc2],shots=NUM_SHOTS)

    results=runjob.result()

    

    # Obtain the counts for each measured state, and convert those counts into a probability vector

    output_distr1 = get_probability_distribution(results.get_counts(qc1))

    output_distr2 = get_probability_distribution(results.get_counts(qc2))

    # Calculate the cost as the distance between the output distribution and the target distribution

    cost = energy(output_distr1,output_distr2,B)

    return cost

import numpy as np

np.set_printoptions(legacy='1.25')



from qiskit_algorithms.optimizers import COBYLA



nshots=NUM_SHOTS

# Initialize the COBYLA optimizer via Qiskit

optimizer = COBYLA(maxiter=500, disp=True,tol=1e-6)



Bfield =np.random.rand(2)

print('(Bz,Bx)=',Bfield)



# Create the initial parameters (noting that our single qubit variational form has 3 parameters)

params = np.random.rand(3)





def myobject(params):

    fvalue=objective_function(params,Bfield)

    return fvalue



counts = []

values = []

myparams = []

#def store_intermediate_result(eval_count, parameters, mean):  # qiskit_algorithm optimizer does not seem to support callback; only in its VQE

#        #print(eval_count,mean,parameters)

#        counts.append(eval_count)

#        values.append(mean)

#        myparams.append(parameters)



        

        

ret = optimizer.minimize(fun=myobject, x0=params)#, callback=store_intermediate_result) # qiskit_algorithm optimizer does not seem to support callback; only in its VQE



# 

qc1 = get_var_formZ(ret.x)

qc2 = get_var_formX(ret.x)

#from qiskit.visualization import circuit_drawer

#circuit_drawer(qc1)

#circuit_drawer(qc2)  cannot draw using the returned circuit!!

counts1 = backend_sim.run(qc1, shots=nshots).result().get_counts(qc1)

counts2 = backend_sim.run(qc2, shots=nshots).result().get_counts(qc2)

dst1=get_probability_distribution(counts1)

dst2=get_probability_distribution(counts2)





myEnergy=energy(dst1,dst2,Bfield)

exactEnergy=-np.sqrt(Bfield[0]**2+Bfield[1]**2)

print('Num of shots for each circuit=',nshots)

print('Estimated minimum energy=',myEnergy,' vs. exact=',exactEnergy,' error=',myEnergy-exactEnergy)

print("Sigma_z:", dst1)

print("Sigma_x:", dst2)

print("Parameters Found:", ret.x)

print(ret.x)

type(optimizer)

print(ret)

from scipy.optimize import minimize

Bfield =np.random.rand(2)

print('(Bz,Bx)=',Bfield)

exactEnergy=-np.sqrt(Bfield[0]**2+Bfield[1]**2)

print("Exact energy = {}".format(exactEnergy))

#counts = []

#values = []

#myparams = []

#def store_intermediate_result(parameters):

#        print(parameters)

#        myparams.append(parameters)

counts = []

values = []

myparams = []



def store_intermediateX(x):   # some optimizer in Scipy only store parameters not func values

        #print(eval_count,mean,parameters)

        myparams.append(x)

        counts.append(len(myparams))

    

def callback(intermediate_result):

        #print("   ",intermediate_result)

        #print(intermediate_result['fun'])

        #print(intermediate_result['x'])

        values.append(intermediate_result['fun'])

        myparams.append(intermediate_result['x'])

        counts.append(len(values))



params = np.random.rand(3)     



#Using directly SciPy optimizer

#ret2=minimize(myobject,params,options={ 'disp':True},callback=callback)

ret2=minimize(myobject,params,method='COBYLA',options={'maxiter':500, 'disp':True,'tol':1e-7},callback=store_intermediateX)

#ret2=minimize(myobject,params,method='L-BFGS-B',options={'maxiter':500, 'disp':True,'maxcor': 10, 'ftol': 2.220446049250313e-09, 'gtol': 1e-05, 'eps': 1e-08, 'maxfun': 15000, 'maxiter': 15000, 'iprint': - 1, 'maxls': 20, 'finite_diff_rel_step': None},callback=callback)

counts

print(ret2)

exactEnergy=-np.sqrt(Bfield[0]**2+Bfield[1]**2)

print('Exact energy= ',exactEnergy)

params = np.random.rand(3) 

print(params)



counts = []

values = []

myparams = []

#ret2=minimize(myobject,params,method='COBYLA',options={'maxiter':500, 'disp':True,'tol':1e-7},callback=store_intermediateX)

#ret2=minimize(myobject,params,method='L-BFGS-B',options={'maxiter':500, 'disp':True,'maxcor': 10, 'ftol': 1e-08, 'gtol': 1e-06, 'eps': 1e-08, 'maxfun': 15000, 'maxiter': 15000, 'iprint': - 1, 'maxls': 20, 'finite_diff_rel_step': None},callback=callback)

ret2=minimize(myobject,params,method='SLSQP',options={'maxiter':500, 'disp':True,'ftol':1e-7},callback=callback)

print(len(counts),len(values))

values

# It allows to use callback to keep track of convergence

import matplotlib.pyplot as plt 



plt.plot(counts, abs(exactEnergy - values))

plt.xlabel('Eval count')

plt.ylabel('Energy difference from solution reference value')

plt.title('Energy convergence')

plt.yscale('log')

plt.legend(loc='upper right')

print(ret2)

exactEnergy=-np.sqrt(Bfield[0]**2+Bfield[1]**2)

print(exactEnergy)

ret2=minimize(myobject,params,options={'disp':True},method='BFGS')

#ret2=minimize(myobject,ret2.x,method='BFGS',options={'maxiter':500, 'disp':True,'maxcor': 10, 'ftol': 2.220446049250313e-09, 'gtol': 1e-05, 'eps': 1e-08, 'maxfun': 15000, 'maxiter': 15000, 'iprint': - 1, 'maxls': 20},callback=store_intermediate_result)

print(ret2)

exactEnergy=-np.sqrt(Bfield[0]**2+Bfield[1]**2)

print('Exact energy is ',exactEnergy)

from qiskit.quantum_info.operators import Operator, Pauli, SparsePauliOp

#from qiskit.opflow import X, Z, I

from qiskit_algorithms import NumPyEigensolver

#from qiskit.aqua.components.variational_forms import RY, RYRZ, SwapRZ   #deprecated

from qiskit_algorithms import VQE

#from qiskit.circuit.library import TwoLocal  #deprecated

from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B, SLSQP, SPSA

def BzBxH(B):

    return SparsePauliOp(['Z','X'],coeffs=[B[0],B[1]]) #B[0]*Z + B[1]*X 

H=BzBxH(Bfield)

def store_intermediate_result(eval_count, parameters, mean, std):

            counts.append(eval_count)

            values.append(mean)

            params.append(parameters)

            deviation.append(std)

from qiskit.circuit.library import n_local

var_form=n_local(H.num_qubits, "ry", "rx", "linear", reps=1, insert_barriers=True)

print(var_form)

optimizer = COBYLA(maxiter=500, disp=True,tol=1e-6)

counts=[]

values=[]

params=[]

deviation=[]



var_form.draw('mpl')

from qiskit.primitives import StatevectorEstimator as Estimator

estimator=Estimator()

vqe = VQE(estimator,var_form, optimizer,callback=store_intermediate_result)

#backend = BasicAer.get_backend('statevector_simulator')

vqe_result = vqe.compute_minimum_eigenvalue(H)

print(vqe_result)

exact_result = NumPyEigensolver().compute_eigenvalues(operator=H)

exact_energy = min(np.real(exact_result.eigenvalues))

print('VQE result: ',vqe_result.optimal_value,' vs Exact: ',exact_energy)

# It allows to use callback to keep track of convergence

import matplotlib.pyplot as plt 



plt.plot(counts, abs(exact_energy - values))

plt.xlabel('Eval count')

plt.ylabel('Energy difference from solution reference value')

plt.title('Energy convergence')

plt.yscale('log')

plt.legend('E',loc='upper right')

three = n_local(3, rotation_blocks=['ry'], entanglement_blocks=['cx'], entanglement='linear',reps=2, insert_barriers=True)

three.decompose().draw('mpl')

from qiskit.circuit.library import efficient_su2

ansatz = efficient_su2(3,entanglement='reverse_linear', reps=2,insert_barriers=True)

ansatz.decompose().draw("mpl",style='textbook')

import qiskit

qiskit.__version__

# Built-in modules

import math



# Imports from Qiskit

from qiskit import QuantumCircuit

from qiskit.circuit.library import GroverOperator, MCMT, ZGate

from qiskit.visualization import plot_distribution



# Imports from Qiskit Runtime

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_ibm_runtime import SamplerV2 as Sampler

# To run on hardware, select the backend with the fewest number of jobs in the queue

service = QiskitRuntimeService()#channel="ibm_quantum")

backend = service.least_busy(operational=True, simulator=False)

backend.name

def grover_oracle(marked_states):

    """Build a Grover oracle for multiple marked states



    Here we assume all input marked states have the same number of bits



    Parameters:

        marked_states (str or list): Marked states of oracle



    Returns:

        QuantumCircuit: Quantum circuit representing Grover oracle

    """

    if not isinstance(marked_states, list):

        marked_states = [marked_states]

    # Compute the number of qubits in circuit

    num_qubits = len(marked_states[0])



    qc = QuantumCircuit(num_qubits)

    # Mark each target state in the input list

    for target in marked_states:

        # Flip target bit-string to match Qiskit bit-ordering

        rev_target = target[::-1]

        # Find the indices of all the '0' elements in bit-string

        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]

        # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)

        # where the target bit-string has a '0' entry

        qc.x(zero_inds)

        qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)

        qc.x(zero_inds)

    return qc

marked_states = ["011", "100"]



oracle = grover_oracle(marked_states)

oracle.draw(output="mpl", style="iqp")

grover_op = GroverOperator(oracle)

grover_op.decompose().draw(output="mpl", style="iqp")

optimal_num_iterations = math.floor(

    math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))

)

qc = QuantumCircuit(grover_op.num_qubits)

# Create even superposition of all basis states

qc.h(range(grover_op.num_qubits))

# Apply Grover operator the optimal number of times

qc.compose(grover_op.power(optimal_num_iterations), inplace=True)

# Measure all qubits

qc.measure_all()

qc.draw(output="mpl", style="iqp")

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager



from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()



target = backend.target

pm = generate_preset_pass_manager(target=target, optimization_level=3)



circuit_isa = pm.run(qc)

circuit_isa.draw(output="mpl", idle_wires=False, style="iqp")

# To run on local simulator:

#   1. Use the SatetvectorSampler from qiskit.primitives instead

#   or 2. Use Fake_backend, as we have chosen

sampler = Sampler(mode=backend)

sampler.options.default_shots = 10_000

job=sampler.run([circuit_isa])

print(job.job_id)

result = job.result()

dist = result[0].data.meas.get_counts()

#job_id='cy6r1ny7v8tg008fehs0'

#job = service.job(job_id)  #can retrieve job

plot_distribution(dist)

import qiskit_ibm_runtime



qiskit_ibm_runtime.version.get_version_info()

import qiskit



qiskit.version.get_version_info()

