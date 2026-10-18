
# A recurrence is Theta(n) when T(n)/n stays between two constants,
# so the plot shows T(n)/n: flat lines are Theta(n), rising lines are not.
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

N = 2**12                        # largest n = 4096
# One array per recurrence; T[n] will hold T(n). Index 0 is unused.
TA = np.zeros(N + 1); TB = np.zeros(N + 1); TC = np.zeros(N + 1); TD = np.zeros(N + 1)
TA[1] = TB[1] = TC[1] = TD[1] = 1    # base case T(1) = 1 for all four
# Fill each table from small n upwards, so the values on the right-hand
# side are always already known. n//2 is integer division (n/2 rounded down).
for n in range(2, N + 1):
    TA[n] = TA[n-1] + 1          # T(n) = T(n-1) + 1
    TD[n] = TD[n-1] + n          # T(n) = T(n-1) + n
    TB[n] = 2*TB[n//2] + 1       # T(n) = 2T(n/2) + 1
    TC[n] = 2*TC[n//2] + n       # T(n) = 2T(n/2) + n

# Compare at powers of 2 (2, 4, ..., 4096), where n/2 is exact
n = 2**np.arange(1, 13)
# name: (table, closed form from the Z-transform)
closed = {'i)':   (TA, n),
          'ii)':  (TB, 2*n - 1),
          'iii)': (TC, n*(np.log2(n) + 1)),
          'iv)':  (TD, n*(n + 1)/2)}
for name, (T, formula) in closed.items():
    ok = np.allclose(T[n], formula)          # True if they agree at every n
    # T(n)/n at the largest n: about 1 and 2 for i), ii); large for iii), iv)
    print(f"{name:5s} matches Z-transform closed form: {ok},  T(n)/n at n = 2^12: {T[N]/N:8.2f}")

fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
# semilogx with base=2: the x axis is logarithmic, so 2, 4, 8, ... are evenly spaced.
# 'o-', 's-', '^-', 'd-' = circle, square, triangle, diamond markers joined by lines.
ax.semilogx(n, TA[n]/n, 'o-', base=2, label=r'i) $T(n-1)+1$')
ax.semilogx(n, TB[n]/n, 's-', base=2, label=r'ii) $2T(n/2)+1$')
ax.semilogx(n, TC[n]/n, '^-', base=2, label=r'iii) $2T(n/2)+n$')
ax.semilogx(n, TD[n]/n, 'd-', base=2, label=r'iv) $T(n-1)+n$')
ax.set_yscale('log')             # y axis logarithmic too, since iv) grows to about 2000
ax.set_xlabel('$n$')
ax.set_ylabel('$T(n)/n$')
ax.legend()
ax.grid(True, which='both', linestyle='--', alpha=0.4)

#If using termux
plt.savefig(os.path.join(FIGS, 'recurrence.pdf'))
subprocess.run(['termux-open', os.path.join(FIGS, 'recurrence.pdf')])
#else
#plt.show()
