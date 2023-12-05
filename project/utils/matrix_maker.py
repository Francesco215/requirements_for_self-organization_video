import numpy as np

def small_world(N, K=4, beta=0.7):
    # Create a regular ring lattice
    G = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(1, K // 2 + 1):
            G[i, (i + j) % N] = 1
            G[i, (i - j) % N] = 1
    
    # Rewire edges with probability beta
    for i in range(N):
        for j in range(1, K // 2 + 1):
            if np.random.rand() < beta:
                G[i, (i + j) % N] = 0
                new_neighbor = np.random.choice(np.setdiff1d(np.arange(N), [i, (i + j) % N]))
                G[i, new_neighbor] = 1
    
    return G
import numpy as np

def big_diag(n, k):
    arr = np.zeros((n, n), dtype=int)
    
    for i in range(n):
        for j in range(n):
            if abs(i - j) < k or abs(i+n-j)<k:
                arr[i, j] = 1
    
    return arr
