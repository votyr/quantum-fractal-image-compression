import numpy as np
import cv2

def load_image(path, size=(32, 32)):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, size)
    return img / 255.0  # normalize

def split_blocks(img, block_size=4):
    blocks = []
    h, w = img.shape

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = img[i:i+block_size, j:j+block_size]
            blocks.append(block.flatten())

    return np.array(blocks)

def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def split_range_domain(img, block_size=4):
    h, w = img.shape

    range_blocks = []
    domain_blocks = []

    # Range blocks = normal grid
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = img[i:i+block_size, j:j+block_size]
            range_blocks.append(block.flatten())

    # Domain blocks = shifted grid (important!)
    for i in range(0, h - block_size, block_size):
        for j in range(0, w - block_size, block_size):
            block = img[i:i+block_size, j:j+block_size]
            domain_blocks.append(block.flatten())

    return np.array(range_blocks), np.array(domain_blocks)

def transform_block(block, block_size=4):
    block = block.reshape(block_size, block_size)

    transforms = [
        block,
        np.rot90(block, 1),
        np.rot90(block, 2),
        np.rot90(block, 3),
        np.fliplr(block),
        np.flipud(block)
    ]

    return [t.flatten() for t in transforms]