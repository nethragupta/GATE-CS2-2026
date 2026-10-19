import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

# Save figures in the repo's figs/ folder no matter where the script is run from
import os
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figs')
os.makedirs(FIGS, exist_ok=True)

import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.line.funcs import line_gen        # points on the segment from A to B
from CoordGeo.plotting.funcs import label_pts   # writes a label above each point

def f(r):
    # 100 r moves the second decimal digit to the units place
    # round(..., 9) removes tiny floating-point errors before the floor.
    d2 = int(np.floor(round(100*r, 9))) % 10      # second digit after the point
    return 1 if d2 in (2, 3, 6, 7) else 0

# f is constant on [k/100, (k+1)/100); compare neighbouring intervals
# (k + 0.5)/100 is the middle of piece k, safely inside it
vals = [f((k + 0.5)/100) for k in range(100)]
# A jump at k/100 happens when piece k differs from piece k-1
jumps = [k for k in range(1, 100) if vals[k] != vals[k-1]]
print("Number of discontinuities:", len(jumps))         # expected 40
print("First few:", [k/100 for k in jumps[:8]])         # 0.02, 0.04, 0.06, 0.08, ...

fig, ax = plt.subplots(figsize=(9, 4), layout='constrained')
K = 30                                   # show the first 30 intervals
for k in range(K):
    # horizontal piece of f on [k/100, (k+1)/100)
    x_h = line_gen(np.array([k/100, vals[k]]).reshape(-1, 1),
                   np.array([(k + 1)/100, vals[k]]).reshape(-1, 1))
    ax.plot(x_h[0, :], x_h[1, :], 'b-', linewidth=2)
J = [k for k in jumps if k < K]          # the jumps inside the part shown
for k in J:
    # vertical dotted line at each jump
    x_v = line_gen(np.array([k/100, 0.0]).reshape(-1, 1), np.array([k/100, 1.0]).reshape(-1, 1))
    ax.plot(x_v[0, :], x_v[1, :], 'r:', linewidth=1)       # 'r:' = red dotted
# Label the top of each dotted line with its r value
P = np.array([[k/100 for k in J], [1.0]*len(J)])
label_pts(P, [f'{k/100:.2f}' for k in J])

ax.set_xlim(0, K/100)
ax.set_ylim(-0.2, 1.35)
ax.set_yticks([0, 1])                    # f only takes the values 0 and 1
ax.set_xlabel('$r$ (first 30 of 100 intervals shown; jumps labelled)')
ax.set_ylabel('$f(r)$')
ax.grid(True, linestyle='--', alpha=0.5)

#If using termux
plt.savefig(os.path.join(FIGS, 'digit.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'digit.pdf')])
#else
#plt.show()
