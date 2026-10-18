
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

# Keys from the question, inserted in this order, with h(k) = k mod 9
keys = [5, 28, 19, 15, 26, 33, 12, 17, 10]
m = 9                                # number of slots in the table
# One empty list per slot; each list is that slot's chain
table = [[] for _ in range(m)]
for k in keys:
    table[k % m].append(k)          # chaining: append to the slot's list

# Print each slot and its chain, e.g. "1 -> 28 -> 19 -> 10".
# enumerate gives (slot number, chain); map(str, chain) turns the keys
# into text, and ' -> '.join puts arrows between them.
for slot, chain in enumerate(table):
    print(slot, '->', ' -> '.join(map(str, chain)))
print("Longest chain:", max(len(c) for c in table))     # expected 3

# Draw slot s at (0, -s) and its chain to the right: (1, -s), (2, -s), ...
# (minus sign so slot 0 is at the top and the slots go downwards)
fig, ax = plt.subplots(figsize=(8, 6), layout='constrained')
for s, chain in enumerate(table):
    Slot = np.array([0.0, -s]).reshape(-1, 1)           # slot position as a column vector
    ax.plot(0, -s, 'ks', markersize=14, fillstyle='none')   # 'ks' = black square (the slot)
    prev = Slot                                         # the last thing drawn in this row
    for j, key in enumerate(chain):
        Node = np.array([j + 1.0, -s]).reshape(-1, 1)   # j-th key goes at x = j + 1
        x_link = line_gen(prev, Node)          # link in the chain
        ax.plot(x_link[0, :], x_link[1, :], 'b-')
        ax.plot(Node[0, 0], Node[1, 0], 'bo', markersize=8)   # blue dot for the key
        prev = Node                                     # next link starts from here
    # Points of this row: x = 0, 1, ..., len(chain); y = -s for all of them.
    # Label the slot with its number and each node with its key.
    pts = np.block([[np.arange(len(chain) + 1, dtype=float)], [-s*np.ones(len(chain) + 1)]])
    label_pts(pts, [str(s)] + [str(key) for key in chain])

ax.set_xlim(-0.6, 3.8)
ax.set_ylim(-m + 0.3, 0.8)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['slot', '1st', '2nd', '3rd'])      # names instead of numbers
ax.set_yticks([])                                       # no ticks on the y axis
ax.set_title('Chains after inserting all keys (longest = 3, slot 1)')
for spine in ax.spines.values():                        # remove the box around the plot
    spine.set_visible(False)

#If using termux
plt.savefig(os.path.join(FIGS, 'hash.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'hash.pdf')])
#else
#plt.show()
