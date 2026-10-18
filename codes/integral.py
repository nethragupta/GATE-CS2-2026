
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

x = np.linspace(-1, 1, 2001)     # 2001 equally spaced points from -1 to 1
h = x[1] - x[0]                  # spacing between them (0.001)

def I(a):
    g = 3*x**2 - a*x + 1                    # the integrand at every point
    # Trapezoidal rule: h x (sum of all values - half of the two end values)
    return h*(g.sum() - (g[0] + g[-1])/2)   # trapezoidal rule

a_vals = np.linspace(-10, 10, 41)           # 41 values of a from -10 to 10
I_vals = np.array([I(a) for a in a_vals])   # I(a) for each of them
print("I(a) for a = -10, 0, 10:", I(-10), I(0), I(10))
# Largest distance from 4 over all a: should be tiny (rounding error only)
print("max |I(a) - 4| =", np.max(np.abs(I_vals - 4)))

fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
# Theory: the line I(a) = 4, drawn with line_gen from (-10, 4) to (10, 4)
x_line = line_gen(np.array([-10.0, 4.0]).reshape(-1, 1), np.array([10.0, 4.0]).reshape(-1, 1))
ax.plot(x_line[0, :], x_line[1, :], 'r--', label='Theory $I(a) = 4$')   # red dashed
ax.plot(a_vals, I_vals, 'o', label='Numerical $I(a)$')                   # dots
# Label three of the dots with their values (to 2 decimal places)
P = np.array([[-10.0, 0.0, 10.0], [I(-10), I(0), I(10)]])
label_pts(P, [f'{I(a):.2f}' for a in [-10, 0, 10]])

ax.set_ylim(0, 6)
ax.set_xlabel('$a$')
ax.set_ylabel('$I(a)$')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

#If using termux
plt.savefig(os.path.join(FIGS, 'integral.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'integral.pdf')])
#else
#plt.show()
