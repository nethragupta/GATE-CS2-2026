
import numpy as np
import numpy.linalg as LA       

# Random number generator with seed 0, so the same matrix comes out every run
rng = np.random.default_rng(0)
M = rng.standard_normal((4, 4))         # a random 4x4 matrix
if LA.det(M) < 0:
    M[0, :] = -M[0, :]                  # make det(M) positive
# Multiplying M by c multiplies det by c^4, so c = (3/det M)^(1/4) gives det = 3.
# (det(M) must be positive for this fourth root to be a real number.)
A = M * (3 / LA.det(M))**(1/4)          # scale so that det(A) = 3
print("det(A)  =", round(LA.det(A), 6))                       
print("det(2A) =", round(LA.det(2*A), 6), "= 2^4 x 3 =", 2**4 * 3)   
