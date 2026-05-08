USE_HARDWARE = False

from utils import load_image, split_range_domain
from classical import find_best_matches
from quantum_kernel import find_best_matches_quantum
from reconstruction import reconstruct, merge_blocks
import matplotlib.pyplot as plt
import numpy as np
from quantum_kernel import quantum_similarity

# Metrics
def mse(a, b):
    return np.mean((a - b) ** 2)

def psnr(a, b):
    m = mse(a, b)
    if m == 0:
        return 100
    return 20 * np.log10(1.0 / np.sqrt(m))

# Load image
img = load_image("images/test4.jpeg", size=(32,32))

# Split
range_blocks, domain_blocks = split_range_domain(img)

# Classical
matches_classical = find_best_matches(range_blocks, domain_blocks)
img_classical = merge_blocks(reconstruct(matches_classical), img.shape)

# Quantum
matches_quantum = find_best_matches_quantum(
    range_blocks,
    domain_blocks,
    use_hardware=USE_HARDWARE
)
img_quantum = merge_blocks(reconstruct(matches_quantum), img.shape)

# Metrics
mse_c = mse(img, img_classical)
psnr_c = psnr(img, img_classical)

mse_q = mse(img, img_quantum)
psnr_q = psnr(img, img_quantum)

import os
os.makedirs("results", exist_ok=True)

# Plot
plt.figure(figsize=(12,5))

plt.subplot(1,3,1)
plt.title("Original")
plt.imshow(img, cmap='gray')

plt.subplot(1,3,2)
plt.title(f"Classical\nPSNR: {psnr_c:.2f}")
plt.imshow(img_classical, cmap='gray')

plt.subplot(1,3,3)
plt.title(f"Quantum\nPSNR: {psnr_q:.2f}")
plt.imshow(img_quantum, cmap='gray')

output_path = "results/output_comparison.png"
plt.savefig(output_path)
print(f"Saved image to {output_path}")

plt.show()

with open("results/metrics.txt", "w") as f:
    f.write("=== Results ===\n")
    f.write(f"Classical MSE: {mse_c:.6f}\n")
    f.write(f"Classical PSNR: {psnr_c:.2f}\n")
    f.write(f"Quantum MSE: {mse_q:.6f}\n")
    f.write(f"Quantum PSNR: {psnr_q:.2f}\n")

print("Saved metrics to results/metrics.txt")

if USE_HARDWARE:
    print("\n=== IBM Hardware Test ===")

    a = range_blocks[0][:4]
    b = domain_blocks[0][:4]

    sim = quantum_similarity(a, b, use_hardware=False)
    print(f"Simulator similarity: {sim:.4f}")

    hw = quantum_similarity(a, b, use_hardware=True)
    print(f"Hardware similarity: {hw:.4f}")