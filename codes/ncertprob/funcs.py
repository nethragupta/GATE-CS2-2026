# Functions from github.com/gadepall/ncert-probability, importable the same
# way as matgeo's CoordGeo:
#
#   from ncertprob.funcs import binomial_distribution, dice_roll
#
# The repo has no library of its own: its functions live inside one-off
# scripts in numbered folders (e.g. exemplar/12/13/3/6/codes/main.py).
# Importing those scripts directly runs the whole script, and some of them
# load data files or save plots to folders that do not exist here.
#
# So each function below is read from its original file in the cloned repo
# and only that function (with the file's imports) is executed. The code
# that runs is the repo's own, unchanged. A function is loaded the first
# time it is imported, so only the repo files you actually use must exist.
#
# The cloned repo is expected at codes/ncert-probability, i.e. next to
# the ncertprob/ folder. Change REPO below if yours is somewhere else.

import ast
import os

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'ncert-probability')

# name: (file in the repo, extra globals the function relies on)
SOURCES = {
    # C(n,k) p^k (1-p)^(n-k) z^k for k = 0..n
    'binomial_distribution': ('exemplar/12/13/3/6/codes/main.py', {}),
    # number of heads in num_tosses fair coin tosses
    'simulate_experiment':   ('exemplar/12/13/3/6/codes/main.py', {}),
    # n rolls of a fair die
    'dice_roll':             ('exemplar/12/13/3/13/codes/ncert.py', {}),
    # True if n is prime
    'is_prime':              ('ncert/10/13/1/25/codes/ncertassign.py', {}),
    # PMF of a fair die, array of `size` values 1/6 (that file sets prob = 1/6)
    'generate_pmf':          ('exemplar/10/13/3/19/codes/main.py', {'prob': 1/6}),
    # standard normal PDF
    'gauss_pdf':             ('codes/clt/pdf_plot.py', {}),
}

__all__ = list(SOURCES)


def load_func(path, name, **env):
    """Return function `name` defined in the script at `path`, without
    running the rest of the script. `env` sets globals it relies on."""
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    keep = [node for node in tree.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
            or (isinstance(node, ast.FunctionDef) and node.name == name)]
    if not any(isinstance(n, ast.FunctionDef) for n in keep):
        raise NameError(f"{name} not found in {path}")
    scope = dict(env)
    for node in keep:
        try:
            exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), scope)
        except ImportError:
            pass          # skip imports the function does not need
    return scope[name]


def __getattr__(name):
    # Called on `from ncertprob.funcs import name`: load it from the repo
    if name not in SOURCES:
        raise AttributeError(f"ncertprob.funcs has no function {name!r}")
    rel, env = SOURCES[name]
    path = os.path.normpath(os.path.join(REPO, rel))
    if not os.path.exists(path):
        raise ImportError(f"{name} needs {path}; clone ncert-probability "
                          f"next to the codes/ folder or edit REPO in {__file__}")
    func = load_func(path, name, **env)
    globals()[name] = func        # cache it
    return func
