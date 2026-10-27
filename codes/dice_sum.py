
# Theory: the PMF of S = X1 + X2 is the convolution of the two die PMFs,
# p_X(n) = sum_k p_X1(n-k) p_X2(k)  (formula 1.1.6).
import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

# Save figures in the repo's figs/ folder no matter where the script is run from
# (figs/ sits next to this codes/ folder)
import os
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figs')
os.makedirs(FIGS, exist_ok=True)


import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.line.funcs import line_gen        # points on the segment from A to B
from CoordGeo.plotting.funcs import label_pts   # writes a label above each point

# dice_roll(n)     : n random rolls of a fair die (numbers 1 to 6)
# is_prime(n)      : True if n is a prime number
# generate_pmf(6)  : array of 6 values, each 1/6 (PMF of one die)
from ncertprob.funcs import dice_roll, is_prime, generate_pmf

# Theory: p_S = p_X * p_X (convolution), defined on k = 2, ..., 12
pmf_X = generate_pmf(6)              # [1/6, 1/6, 1/6, 1/6, 1/6, 1/6] for faces 1..6
# np.convolve multiplies the two PMFs as polynomials: the result has
# 11 values, for S = 2, 3, ..., 12 (e.g. Pr(S = 7) = 6/36)
panal = np.convolve(pmf_X, pmf_X)
n = np.arange(2, 13)                 # the possible sums 2, ..., 12

# Simulation: roll two dice simlen times and add them
simlen = 100000
S = dice_roll(simlen) + dice_roll(simlen)
# S == k is True/False for each roll; the mean of that gives the
# fraction of rolls with sum k, an estimate of Pr(S = k)
psim = np.array([np.mean(S == k) for k in n])

primes = [int(k) for k in n if is_prime(k)]   # 2, 3, 5, 7, 11
idx = [k - 2 for k in primes]                 # positions in panal (sum 2 is index 0)
print("Prime sums:", primes)
# Add up the probabilities of the prime sums: (1+2+4+6+2)/36 = 15/36
print("Theory    : Pr(S prime) =", panal[idx].sum(), "= 15/36")
print("Simulation: Pr(S prime) ~", psim[idx].sum())

fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
# Stems drawn with line_gen from (k, 0) to (k, p_S(k))
# zip pairs each sum k with its probability p
for k, p in zip(n, panal):
    x_stem = line_gen(np.array([k, 0.0]).reshape(-1, 1), np.array([k, p]).reshape(-1, 1))
    ax.plot(x_stem[0, :], x_stem[1, :], 'b-', linewidth=1.5)
ax.plot(n, panal, 'bo', label='Analysis')                           # blue dots: theory
ax.plot(n, psim, 'ro', fillstyle='none', markersize=10, label='Simulation')   # red rings
ax.plot(primes, panal[idx], 'g*', markersize=14, label='Prime sums')          # green stars
# Label the prime sums with their probabilities, e.g. 6/36
P = np.block([[np.array(primes, dtype=float)], [panal[idx]]])
label_pts(P, [f'{round(p*36)}/36' for p in panal[idx]])

ax.set_xticks(n)
ax.set_ylim(0, 0.2)
ax.set_xlabel('$k$')
ax.set_ylabel('$p_S(k)$')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

#If using termux
plt.savefig(os.path.join(FIGS, 'dice_sum.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'dice_sum.pdf')])
#else
#plt.show()
