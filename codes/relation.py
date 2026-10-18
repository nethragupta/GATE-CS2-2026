
import math
import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if

A = range(1, 11)                 # the numbers 1 to 10
# M is the 10x10 relation matrix: M[x-1][y-1] = 1 if (x, y) is in R.
# math.isqrt(n) is the integer part of sqrt(n); n is a perfect square
# exactly when isqrt(n)^2 == n.
M = np.array([[1 if math.isqrt(x*y)**2 == x*y else 0 for y in A] for x in A])
# R as a set of pairs, read off from M
R = {(x, y) for x in A for y in A if M[x-1][y-1]}

# all(...) is True only if the condition holds in every case
reflexive = all((x, x) in R for x in A)                  # (x, x) in R for every x
symmetric = all((y, x) in R for (x, y) in R)             # (x, y) in R => (y, x) in R
# (x, y) and (y, z) in R => (x, z) in R; here w must equal y to chain the pairs
transitive = all((x, z) in R for (x, y) in R for (w, z) in R if y == w)
# (x, y) and (y, x) both in R => x = y
antisymmetric = all(x == y for (x, y) in R if (y, x) in R)
# Expected: True, True, True, False (option i, ii, iii)
print("Reflexive    :", reflexive)
print("Symmetric    :", symmetric)
print("Transitive   :", transitive)
print("Antisymmetric:", antisymmetric)

fig, ax = plt.subplots(figsize=(6, 6), layout='constrained')
# imshow draws M as a grid of coloured squares: 1 = dark blue, 0 = white.
# origin='lower' puts x = 1 at the bottom; extent places square (x, y)
# centred on the whole numbers 1 to 10.
ax.imshow(M, cmap='Blues', origin='lower', extent=(0.5, 10.5, 0.5, 10.5))
ax.set_xticks(list(A)); ax.set_yticks(list(A))
ax.set_xlabel('$y$'); ax.set_ylabel('$x$')
ax.set_title(r'$(x, y) \in R$ (shaded)')
ax.grid(True, linestyle='--', alpha=0.3)

#If using termux
plt.savefig('figs/relation.pdf')
subprocess.run(shlex.split("termux-open figs/relation.pdf"))
#else
#plt.show()
