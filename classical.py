import numpy as np
from utils import transform_block, normalize_vector

def classical_similarity(a, b):
    return np.dot(a, b)

def find_best_matches(range_blocks, domain_blocks):
    matches = []

    for r in range_blocks:
        r = normalize_vector(r)

        best_block = None
        best_score = -1

        for d in domain_blocks:
            transformed = transform_block(d)

            for t in transformed:
                t = normalize_vector(t)
                score = classical_similarity(r, t)

                if score > best_score:
                    best_score = score
                    best_block = t

        matches.append(best_block)

    return matches