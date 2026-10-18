
import numpy as np
import numpy.linalg as LA        # eigenvalues
import sympy                     # exact row reduction (rref)
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.matrix.funcs import polyvalm
from CoordGeo.line.funcs import line_gen        
from CoordGeo.plotting.funcs import label_pts   
# Row reduction R2 <- a R2 - 16 R1 turns [A | c] = [[a, 1, b], [16, a, 24]] into
#   [[a, 1, b], [0, a^2 - 16, 24 a - 16 b]]
# Infinitely many solutions need this second row to be zero.

# Step 1: a^2 - 16 = 0. This is f(-a), where f is the characteristic
# polynomial of N = [[0, 1], [16, 0]]  (5.1.1.1)
N = np.array([[0, 1], [16, 0]])
f = np.poly(N)                                    
print("Characteristic polynomial of N:", f)        # [1, 0, -16]  ->  l^2 - 16
print("Cayley-Hamilton, f(N) =\n", polyvalm(f, N)) # zero matrix (5.1.2.1)
# The eigenvalues of N are the roots of f(l) = 0: l = 4, -4.
# np.real drops the zero imaginary part numpy may return.
lam = np.real(LA.eigvals(N))                       # roots of f(l) = 0
# a = -l for each root, sorted, rounded to whole numbers: a = 4, -4
a_vals = [int(round(v)) for v in sorted(-lam, reverse=True)]   # a = -l
print("a =", a_vals)

fig, ax = plt.subplots(figsize=(8, 6), layout='constrained')
pts, names = [], []              # points to label and their labels
# For each value of a (blue line for a = 4, red line for a = -4)
for a, col in zip(a_vals, ['b', 'r']):
    A = np.array([[a, 1], [16, a]])
    # Step 2: the last entry of the reduced second row is E[1,:] @ c = 0,
    # with E = [[1, 0], [-16, a]] and c = (b, 24):  -16 b + 24 a = 0
    E = np.array([[1, 0], [-16, a]])
    # -16 b + a x 24 = 0  ->  b = -(a x 24) / (-16) = 3a/2   (// = integer division)
    b = -E[1, 1]*24 // E[1, 0]
    c = np.array([b, 24]).reshape(-1, 1)
    Aug = np.block([A, c])                       # augmented matrix [A | c]
    print(f"\na = {a}, b = {b}, ab = {a*b}")
    print("E [A | c] =\n", E @ Aug)              # @ = matrix product; second row is all 0

    # R = reduced row echelon form, piv = the pivot columns. Only column 0
    # is a pivot, so there is one equation in two unknowns: infinitely many solutions.
    R, piv = sympy.Matrix(Aug).rref()
    print("rref([A | c]) =", R.tolist(), " pivots:", piv)
    # Zero second row -> y is free: x = R[0,2] - R[0,1] y   (as in 5.10.1.16)
    x0 = np.array([float(R[0, 2]), 0.0]).reshape(-1, 1)    # y = 0
    m = np.array([-float(R[0, 1]), 1.0]).reshape(-1, 1)    # direction
    # The solutions are x0 + t m for every t: a line. Draw it for t from -3 to 3.
    x_l = line_gen(x0 - 3*m, x0 + 3*m)
    ax.plot(x_l[0, :], x_l[1, :], col + '-', linewidth=2,
            label=fr'$a = {a},\ b = {b}$')
    pts.append(x0); names.append(f'({x0[0,0]:g}, 0)')   # remember the point (x0, 0)

# Both solution lines pass through (3/2, 0); label it once
P = np.block(pts)                # put the saved column vectors side by side
ax.plot(P[0, :], P[1, :], 'ko')
label_pts(P[:, [0]], names[:1])
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

#If using termux
plt.savefig('figs/lines.pdf')
subprocess.run(shlex.split("termux-open figs/lines.pdf"))
#else
#plt.show()
