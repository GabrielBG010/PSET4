import numpy as np

def cosine_similarity(a,b):
    """calculate cosine similarity between two 1D numpy vectors a and b"""

    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
