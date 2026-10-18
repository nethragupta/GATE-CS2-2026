# Jaccard coefficient of two edge sets S, T = |S intersect T| / |S union T|.
# It is 0 when the two trees share no edge, which is the smallest possible value.
import itertools                 # combinations of edges
import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'CoordGeo'))

from CoordGeo.line.funcs import line_gen        # points on the segment from A to B
from CoordGeo.conics.funcs import circ_gen      # points on a circle
from CoordGeo.plotting.funcs import label_pts   # writes a label above each point

n = 5                                            # K5: 5 vertices, numbered 0 to 4
# Every pair of vertices is an edge: (0,1), (0,2), ..., (3,4), 10 edges
edges = list(itertools.combinations(range(n), 2))

# A set of n-1 = 4 edges is a spanning tree if it has no cycle.
# Union-find: parent[u] links each vertex towards the root of its group.
# Adding an edge whose two ends already have the same root closes a cycle.
def is_tree(es):
    parent = list(range(n))                      # each vertex starts as its own group
    def find(u):
        while parent[u] != u:                    # follow the links to the root
            u = parent[u]
        return u
    for u, v in es:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False                         # cycle found: not a tree
        parent[ru] = rv                          # join the two groups
    return True

# Try every choice of 4 edges out of 10 and keep the trees
trees = [set(t) for t in itertools.combinations(edges, n - 1) if is_tree(t)]
# & = common edges, | = all edges of either tree; take the smallest ratio
jac = min(len(s & t) / len(s | t) for s, t in itertools.combinations(trees, 2))
print("Spanning trees of K5:", len(trees))       # 5^(5-2) = 125 (Cayley's formula)
print("Minimum Jaccard coefficient:", jac)       

# One example of two trees with no common edge
T1 = [(0, 1), (1, 2), (2, 3), (3, 4)]
T2 = [(0, 2), (2, 4), (1, 4), (1, 3)]
print("T1 and T2 share", len(set(T1) & set(T2)), "edges")

# Vertices on the unit circle, evenly spaced, vertex 0 at the top (angle 90 degrees)
theta = np.pi/2 + 2*np.pi*np.arange(n)/n
# V is 2 x 5: column i is the point (cos theta_i, sin theta_i)
V = np.vstack((np.cos(theta), np.sin(theta)))

fig, ax = plt.subplots(figsize=(6, 6), layout='constrained')
x_circ = circ_gen(np.zeros((2, 1)), 1)           # circle with centre (0, 0), radius 1
ax.plot(x_circ[0, :], x_circ[1, :], ':', color='lightgray')
# All 10 edges of K5 in light grey. V[:, [u]] is column u kept as a 2x1 vector.
for (u, v) in edges:
    x_e = line_gen(V[:, [u]], V[:, [v]])
    ax.plot(x_e[0, :], x_e[1, :], '-', color='lightgray', linewidth=1)
# T1 in thick blue. Only the first edge gets a legend label, so it appears once.
for k, (u, v) in enumerate(T1):
    x_e = line_gen(V[:, [u]], V[:, [v]])
    ax.plot(x_e[0, :], x_e[1, :], 'b-', linewidth=3, label='$T_1$' if k == 0 else None)
# T2 in thick red dashes
for k, (u, v) in enumerate(T2):
    x_e = line_gen(V[:, [u]], V[:, [v]])
    ax.plot(x_e[0, :], x_e[1, :], 'r--', linewidth=3, label='$T_2$' if k == 0 else None)
ax.plot(V[0, :], V[1, :], 'ko', markersize=8)    # the vertices as black dots
label_pts(V, [str(i) for i in range(n)])         # number them 0 to 4
ax.set_aspect('equal')                           # same scale on both axes, so the circle is round
ax.axis('off')                                   # hide the axes
ax.legend(loc='lower right')

#If using termux
plt.savefig('figs/spanning.pdf')
subprocess.run(shlex.split("termux-open figs/spanning.pdf"))
#else
#plt.show()
