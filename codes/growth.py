import math                      
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

# 200 values of n spread evenly on a log scale, from 10^1 to 10^8
# (logspace(1, 8, ...) means 10**1 ... 10**8)
n = np.logspace(1, 8, 200)

# The four functions, evaluated at every n
f_log = np.log2(n)               # log2(n)
f_cube = n**(1/3)                # cube root of n
f_pow = 2**np.log2(n)            # 2^(log2 n), which is just n
# log2(n!): n! itself is far too large to compute for n = 10^8, so use
# lgamma(k+1) = ln(k!) (natural log of k factorial, computed directly),
# then divide by ln(2) to change it to base 2
f_fact = np.array([math.lgamma(k + 1) for k in n]) / math.log(2)

# Print the four values at a few sizes of n to compare them as numbers
for k in [1e2, 1e4, 1e6, 1e8]:
    # {k:>9.0e}: k in scientific notation, right-aligned in 9 characters
    # {...:6.1f}: a number with 1 decimal place, 6 characters wide
    print(f"n = {k:>9.0e}: log n = {math.log2(k):6.1f}, n^(1/3) = {k**(1/3):8.1f}, "
          f"2^log n = {k:10.0f}, log n! = {math.lgamma(k+1)/math.log(2):12.0f}")
# The values grow in the order log n < n^(1/3) < n < log(n!) for large n

# Plot all four on log-log axes: both axes are logarithmic, so values from
# about 3 to 10^9 fit on one graph and each function appears as a smooth curve
fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
ax.loglog(n, f_log, label=r'$\log(n)$')             # r'...$...$' = LaTeX label
ax.loglog(n, f_cube, label=r'$n^{1/3}$')
ax.loglog(n, f_pow, label=r'$2^{\log(n)} = n$')
ax.loglog(n, f_fact, label=r'$\log(n!)$')
ax.set_xlabel('$n$')
ax.set_ylabel('value')
ax.legend()                                         # box naming each curve
# Grid lines at major (10, 100, ...) and minor (20, 30, ...) ticks
ax.grid(True, which='both', linestyle='--', alpha=0.4)

#If using termux
plt.savefig(os.path.join(FIGS, 'growth.pdf'))                      
subprocess.run(['termux-open', os.path.join(FIGS, 'growth.pdf')])   
#else
#plt.show()                                         