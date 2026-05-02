# Quantum Fractal Image Compression with Quantum Kernel Optimization

## 📌 Overview

This project implements a **Quantum-Inspired Fractal Image Compression system** that compares classical similarity measures with a **quantum kernel approach** using a swap test circuit.

The goal is to explore how quantum computing techniques can improve similarity detection in fractal compression by mapping image data into a high-dimensional Hilbert space.

---

## 🧠 Key Concepts

* Fractal Image Compression (self-similarity)
* Quantum Kernel Methods
* Swap Test (quantum similarity estimation)
* Hybrid Classical-Quantum Pipeline
* IBM Quantum Hardware Execution

---

## ⚙️ Methodology

### 1. Image Preprocessing

* Convert image to grayscale
* Resize to small resolution (16×16 or 32×32)
* Normalize pixel values

---

### 2. Block Splitting

The image is divided into:

* **Range Blocks** → Target blocks to approximate
* **Domain Blocks** → Candidate source blocks

---

### 3. Transformations

Each domain block undergoes transformations:

* Rotation (90°, 180°, 270°)
* Horizontal flip
* Vertical flip

This enables better matching via self-similarity.

---

### 4. Classical Similarity

Similarity between blocks is computed using:

* Dot product (cosine similarity after normalization)

---

### 5. Quantum Similarity (Core Contribution)

Each block is encoded as a quantum state:

* Amplitude encoding
* Normalized vector → quantum state

Similarity is computed using a swap test:

$$
|\langle \psi | \phi \rangle|^2 = 2P(0) - 1
$$

Where:

* (P(0)) is the probability of measuring the ancilla qubit in state 0.

---

### 6. Quantum Circuit

The swap test circuit includes:

* State preparation (StatePreparation)
* Hadamard gate
* Controlled-SWAP gates
* Measurement

---

### 7. Matching Process

For each range block:

* Compare with all transformed domain blocks
* Select best match based on similarity score

---

### 8. Reconstruction

The image is reconstructed using:

* Best matching transformed blocks

---

## ⚛️ IBM Quantum Hardware

* The swap test was executed on real quantum hardware via IBM Quantum.
* Due to hardware limitations:

  * Only small vector comparisons were executed
  * Full pipeline was run on a simulator

---

## 📊 Results

### Metrics Used

* **MSE (Mean Squared Error)**
* **PSNR (Peak Signal-to-Noise Ratio)**

---

### Example Results

| Method    | MSE      | PSNR (dB) |
| --------- | -------- | --------- |
| Classical | 0.458963 | 3.38      |
| Quantum   | 0.006279 | 22.02     |

---

### Observations

* Quantum similarity significantly improved reconstruction quality
* Better preservation of image structure
* Higher PSNR indicates better compression fidelity

---

## 📁 Results Folder

* `output_comparison.png` → visual comparison
* `metrics.txt` → numerical results

---

## ▶️ How to Run

Install dependencies:

```bash
pip install numpy opencv-python matplotlib qiskit qiskit-aer qiskit-ibm-runtime tqdm
```

Run:

```bash
python main.py
```

---

## ⚠️ Limitations

* Quantum simulation is computationally expensive
* Real hardware has:

  * Limited qubits
  * Noise
  * Queue delays
* Small image sizes required

---

## 🚀 Future Improvements

* Variational Quantum Circuits (VQC) for adaptive compression
* Hybrid quantum-classical optimization
* Larger image support
* Noise mitigation techniques
* Quantum autoencoders

---

## 🧠 Conclusion

This project demonstrates that quantum kernel methods can enhance fractal image compression by improving similarity detection. While current hardware limits scalability, the approach shows strong potential for future quantum advantage.


---
