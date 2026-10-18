import numpy as np                              # arrays
import matplotlib.pyplot as plt                 # plotting
from sympy import symbols, expand, Rational     # exact (symbolic) algebra
#If using termux
import subprocess                               # runs termux-open at the end
import shlex                                    # splits that command into words
#end if

# binomial_distribution(p, n, z) returns the list
#   C(n,k) p^k (1-p)^(n-k) z^k   for k = 0, 1, ..., n
from ncertprob.funcs import binomial_distribution

# Tell Python where to find CoordGeo:
#   ROOT = this codes/ folder (CoordGeo, cprog, ncert-probability live here)
#   sys.path is the list of folders Python searches when importing.
# CoordGeo itself is added too, because its files import each other
# by short names (e.g. "from line.funcs import *").
import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.line.funcs import line_gen        # points on the segment from A to B
from CoordGeo.plotting.funcs import label_pts   # writes a label above each point

# Initialize figure
# fig = the whole picture, ax = the plotting area inside it
# layout='constrained' keeps labels and legend from being cut off
fig, ax = plt.subplots(figsize=(9, 6), layout='constrained')

# Parameters
n = 4                # number of days
k = 3                # required number of cloudy days
p = Rational(1, 2)   # Pr(cloudy); Rational keeps it as the exact fraction 1/2
q = 1 - p            # Pr(sunny)

# 1. Z-transform  M_X(z) = q + p z^{-1},  M_Y(z) = M_X(z)^n
#    X = 1 if a day is cloudy, else 0 (a Bernoulli random variable).
#    Y = X_1 + ... + X_n = number of cloudy days. The days are independent,
#    so the Z-transform of Y is the product of the n Z-transforms.
z = symbols('z')                 # make z a symbol, not a number
M_X = q + p * z**-1
M_Y = expand(M_X**n)             # multiply out (q + p z^-1)^4
# Pr(Y = i) is the coefficient of z^{-i} in M_Y(z).
# coeff(z, -i) picks that coefficient; float() turns 1/4 into 0.25.
pmf_z = np.array([float(M_Y.coeff(z, -i)) for i in range(n + 1)])
print("M_Y(z) =", M_Y)
print(f"Z-transform     : Pr(Y = {k}) = {M_Y.coeff(z, -k)}")   # 1/4

# 2. Closed-form binomial PMF (z = 1 gives the PMF values)
#    With z = 1 the factor z^k is 1, so the list is just C(n,k) p^k q^(n-k)
pmf_formula = binomial_distribution(float(p), n, 1)
print(f"Binomial formula: Pr(Y = {k}) = {pmf_formula[k]}")    # 0.25, the same answer

# 3. Plot the PMF
y = np.arange(n + 1)             # the possible values 0, 1, 2, 3, 4
# Stems drawn with line_gen from (i, 0) to (i, p_Y(i))
# line_gen needs each point as a 2x1 column vector, hence reshape(-1, 1).
# It returns a 2 x 10 array: row 0 = x values, row 1 = y values.
for i in range(n + 1):
    x_stem = line_gen(np.array([y[i], 0.0]).reshape(-1, 1),
                      np.array([y[i], pmf_z[i]]).reshape(-1, 1))
    ax.plot(x_stem[0, :], x_stem[1, :], 'b-', linewidth=1.5)   # 'b-' = blue line
ax.plot(y, pmf_z, 'bo', label='Z-transform')                   # 'bo' = blue dots on top

# Label each stem with its exact probability using label_pts
# P is a 2 x 5 array: first row the x values, second row the y values
P = np.block([[y.astype(float)], [pmf_z]])
label_pts(P, [str(M_Y.coeff(z, -i)) for i in range(n + 1)])   # labels 1/16, 1/4, ...

# Highlight the answer with a big green star
ax.plot(k, pmf_z[k], 'g*', markersize=15, label=r'$p_Y(3) = 1/4$ (Option A)')

# Formatting plot area
ax.set_xticks(y)                 # ticks only at 0, 1, 2, 3, 4
ax.set_ylim(0, 0.45)             # room above the tallest stem for its label
ax.grid(True, linestyle='--', alpha=0.5)   # dashed, half-transparent grid

# Remove the outer plot box (spines)
for spine in ax.spines.values():
    spine.set_visible(False)

# Axis labels (text between $...$ is written as maths)
ax.set_xlabel('Y (number of cloudy days)')
ax.set_ylabel(r'$p_Y(k)$')

# Legend placed just outside the top right corner of the plot
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., frameon=True)

#If using termux
plt.savefig('figs/pmf.pdf')                                # save the figure for the book
subprocess.run(shlex.split("termux-open figs/pmf.pdf"))    # open it on Android

#else
#plt.show()                                                # on a PC: open in a window
