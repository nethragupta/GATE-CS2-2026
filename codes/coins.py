
import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

# binomial_distribution(p, n, z) returns C(n,k) p^k (1-p)^(n-k) z^k for k = 0..n
from ncertprob.funcs import binomial_distribution

import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.line.funcs import line_gen        # points on the segment from A to B
from CoordGeo.plotting.funcs import label_pts   # writes a label above each point

def polymul2(A, B):
    # product of two polynomials in (z1^-1, z2^-1), stored as coefficient arrays
    # The product has degree (deg A + deg B) in each variable, so its array
    # has (rows A + rows B - 1) rows and (cols A + cols B - 1) columns
    C = np.zeros((A.shape[0] + B.shape[0] - 1, A.shape[1] + B.shape[1] - 1))
    for j in range(A.shape[0]):
        for k in range(A.shape[1]):
            # A[j,k] z1^-j z2^-k times all of B: B is added, scaled by A[j,k],
            # into C shifted down j rows and right k columns
            C[j:j + B.shape[0], k:k + B.shape[1]] += A[j, k] * B
    return C

# Z-transform of one toss, by which sums it adds to (Table of contributions)
both  = np.array([[0.5, 0.0], [0.0, 0.5]])   # toss 2:      1/2 + 1/2 z1^-1 z2^-1
only1 = np.array([[0.5], [0.5]])             # tosses 4, 6: 1/2 + 1/2 z1^-1
only2 = np.array([[0.5, 0.5]])               # tosses 1,3,5: 1/2 + 1/2 z2^-1

# M_{S1,S2}(z1, z2): product over all six independent tosses
# Start with toss 2, then multiply in tosses 4, 6 and 1, 3, 5 one at a time
M = both
for factor in [only1, only1, only2, only2, only2]:
    M = polymul2(M, factor)
print("Coefficients of M(z1, z2), rows = S1, columns = S2:")
# Every probability is a multiple of 1/64 (6 fair tosses), so print M x 64 as whole numbers
print(np.round(M * 64).astype(int), "/ 64")

# G(z1) = coefficient of z2^-2  ->  Pr(S1 = k, S2 = 2)
G = M[:, 2]                              # column 2 of the array: S2 = 2
print("G(z1) coefficients x 64:", np.round(G * 64).astype(int))
# Putting z1 = 1 adds up all the coefficients
pr_E2 = G.sum()                          # G(1)
pr_E1E2 = G[2:].sum()                    # S1 >= 2 (entries 2 and 3)
print("Pr(E2) =", pr_E2, ", Pr(E1 E2) =", pr_E1E2)
# Conditional probability: Pr(E1 | E2) = Pr(E1 and E2) / Pr(E2) = 0.5
print("Z-transform: Pr(E1 | E2) =", pr_E1E2 / pr_E2)

# Given E2, S1 is binomial(3, 1/2): check with the repo's function
pmf_theory = G / pr_E2
print("G/G(1) matches binomial_distribution(0.5, 3, 1):",
      np.allclose(pmf_theory, binomial_distribution(0.5, 3, 1)))

# Simulation: toss 6 coins, keep the trials where E2 happens
simlen = 200000
# Each row is one experiment of 6 tosses (column 0 = toss 1, ..., column 5 = toss 6)
t = np.random.randint(0, 2, size=(simlen, 6))       # 1 = head
# E2: exactly 2 heads among tosses 1, 2, 3, 5 (columns 0, 1, 2, 4)
E2 = t[:, [0, 1, 2, 4]].sum(axis=1) == 2
# Keep only the rows where E2 happened; K = heads among tosses 2, 4, 6
K = t[E2][:, [1, 3, 5]].sum(axis=1)
# Fraction of those rows with K = 0, 1, 2, 3
pmf_sim = np.array([np.mean(K == k) for k in range(4)])
print("Simulation : Pr(E1 | E2) ~", pmf_sim[2:].sum())

fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
k = np.arange(4)
# Light green band over K = 2, 3: the values where E1 happens
ax.axvspan(1.5, 3.5, color='green', alpha=0.1, label='$E_1$ ($K \\geq 2$)')
# Stems drawn with line_gen
for i in k:
    x_stem = line_gen(np.array([i, 0.0]).reshape(-1, 1),
                      np.array([i, pmf_theory[i]]).reshape(-1, 1))
    ax.plot(x_stem[0, :], x_stem[1, :], 'b-', linewidth=1.5)
ax.plot(k, pmf_theory, 'bo', label='Theory (joint Z-transform)')        # blue dots
ax.plot(k, pmf_sim, 'ro', fillstyle='none', markersize=10, label='Simulation')   # red rings
# Exact values with label_pts
P = np.block([[k.astype(float)], [pmf_theory]])
label_pts(P, ['1/8', '3/8', '3/8', '1/8'])

ax.set_xticks(k)
ax.set_ylim(0, 0.45)
ax.set_xlabel('$K$ (heads among tosses 2, 4, 6)')
ax.set_ylabel(r'$\Pr(K = k \mid E_2)$')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

#If using termux
plt.savefig('figs/coins.pdf')
subprocess.run(shlex.split("termux-open figs/coins.pdf"))
#else
#plt.show()
