import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from tqdm import tqdm
from utils import transform_block
from qiskit.circuit.library import StatePreparation

simulator = AerSimulator()

def pad_to_power_of_2(vec):
    size = 2 ** int(np.ceil(np.log2(len(vec))))
    return np.pad(vec, (0, size - len(vec)))

# Hardware execution 
def run_on_hardware(qc):
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

    service = QiskitRuntimeService()
    backend = service.least_busy(simulator=False)

    # Transpile for real device
    qc_transpiled = transpile(qc, backend=backend, optimization_level=1)

    sampler = Sampler(mode=backend)
    job = sampler.run([qc_transpiled])
    result = job.result()

    # New result format (important fix)
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())

    return counts.get('0', 0) / total

# Swap Test
def swap_test(vec1, vec2, use_hardware=False):
    vec1 = pad_to_power_of_2(vec1)
    vec2 = pad_to_power_of_2(vec2)

    n = int(np.log2(len(vec1)))
    qc = QuantumCircuit(1 + 2*n, 1)

    # State preparation (hardware compatible)
    qc.append(StatePreparation(vec1), range(1, n+1))
    qc.append(StatePreparation(vec2), range(n+1, 2*n+1))

    qc.h(0)

    for i in range(n):
        qc.cswap(0, 1+i, 1+n+i)

    qc.h(0)
    qc.measure(0, 0)

    # Hardware
    if use_hardware:
        prob_0 = run_on_hardware(qc)

    # Simulator
    else:
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=256).result()
        counts = result.get_counts()
        prob_0 = counts.get('0', 0) / 256

    # Convert to similarity
    return max(0, 2 * prob_0 - 1)

# Quantum similarity
def quantum_similarity(a, b, use_hardware=False):
    if np.linalg.norm(a) < 1e-8 or np.linalg.norm(b) < 1e-8:
        return 0

    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    return swap_test(a, b, use_hardware)

# Main matching (SIMULATOR ONLY)
def find_best_matches_quantum(range_blocks, domain_blocks):
    matches = []

    for r in tqdm(range_blocks, desc="Quantum Processing"):
        best_block = None
        best_score = -1

        for d in domain_blocks:
            transformed = transform_block(d)

            for t in transformed:
                score = quantum_similarity(r, t, use_hardware=False)

                if score > best_score:
                    best_score = score
                    best_block = t

        matches.append(best_block)

    return matches