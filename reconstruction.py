import numpy as np

def reconstruct(blocks):
    return np.array(blocks)

def merge_blocks(blocks, image_shape, block_size=4):
    h, w = image_shape
    img = np.zeros((h, w))

    idx = 0
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            img[i:i+block_size, j:j+block_size] = blocks[idx].reshape(block_size, block_size)
            idx += 1

    return img