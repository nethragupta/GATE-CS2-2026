
import numpy as np
import matplotlib.pyplot as plt
#if using termux
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

# gauss_pdf(x) = exp(-x^2/2)/sqrt(2 pi), the standard normal N(0, 1) PDF
from ncertprob.funcs import gauss_pdf

# The question's f(x) = exp(-x^2/18)/(3 sqrt(2 pi)) is N(0, 9), so sigma = 3.
# If Z ~ N(0, 1) has PDF g, then X = sigma Z has PDF g(x/sigma)/sigma.
sigma = 3.0
def f(x):
	return float(gauss_pdf(x/sigma))/sigma
# np.vectorize lets f work on a whole array of x values at once
vec_f = np.vectorize(f)

# Numerical PDF from the empirical CDF
maxrange = 50                    # number of x points
maxlim = 12.0                    # x runs from -12 to 12 (4 sigma each side)
x = np.linspace(-maxlim, maxlim, maxrange)
simlen = int(1e6)                # number of random samples
randvar = np.random.normal(0, sigma, simlen)     # 10^6 samples of N(0, 9)
# Empirical CDF: F(xi) ~ fraction of samples less than xi
err = np.array([np.mean(randvar < xi) for xi in x])
# PDF = derivative of the CDF: (change in F)/(change in x) between
# neighbouring points. np.diff gives those differences.
pdf = np.diff(err)/np.diff(x)
# Each slope belongs to the midpoint of its interval
xm = (x[:-1] + x[1:])/2

print("Sample mean     ~", randvar.mean(), "(theory 0)")
print("Sample variance ~", randvar.var(), "(theory 9)")
print("f(0) =", f(0), "= 1/(3 sqrt(2 pi)) =", 1/(3*np.sqrt(2*np.pi)))

fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
xx = np.linspace(-maxlim, maxlim, 400)            # many points for a smooth curve
ax.plot(xx, vec_f(xx), label=r'Theory $\mathcal{N}(0, 9)$')
ax.plot(xm, pdf, 'o', label='Numerical')          # dots from the simulation
# Mark mean and +/- sigma with line_gen, label them with label_pts
# Each dashed line goes from (xv, 0) up to the curve at (xv, f(xv))
for xv in [-sigma, 0.0, sigma]:
	x_l = line_gen(np.array([xv, 0.0]).reshape(-1, 1), np.array([xv, f(xv)]).reshape(-1, 1))
	ax.plot(x_l[0, :], x_l[1, :], 'k--', linewidth=1)    # 'k--' = black dashed
# Top ends of the three lines (row 0 = x, row 1 = y) and their labels
P = np.array([[-sigma, 0.0, sigma], [f(-sigma), f(0), f(sigma)]])
label_pts(P, [r'$-\sigma$', r'$\mu = 0$', r'$\sigma = 3$'])

ax.grid(True, linestyle='--', alpha=0.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$f(x)$')
ax.set_ylim(0, 0.155)            # just above the peak f(0) = 0.133
ax.legend()

#if using termux
plt.savefig(os.path.join(FIGS, 'gauss.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'gauss.pdf')])
#else
#plt.show()
