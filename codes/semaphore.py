
# step(state) returns every state reachable by running ONE line of ONE process.
def step(state):
    pcs, A, B, X, out = state
    nxt = []
    for p in range(3):
        pc = pcs[p]
        # new = pcs with process p moved on to its next line
        # (tuples cannot be changed, so copy to a list, change, convert back)
        new = list(pcs); new[p] = pc + 1; new = tuple(new)
        # process is blocked and adds nothing.
        if pc == 0 and A == 1:   nxt.append((new, 0, B, X, out))
        elif pc == 1:            nxt.append((new, A, B, X, out + '*'))     # Print(*)
        elif pc == 2:            nxt.append((new, A, B, X + 1, out))       # X = X + 1
        # If X == 2, print $ and set B = 1; otherwise do nothing
        elif pc == 3:            nxt.append((new, A, 1, X, out + '$') if X == 2 else (new, A, B, X, out))
        elif pc == 4:            nxt.append((new, 1, B, X, out))           # Signal(A): A = 1
        elif pc == 5 and B == 1: nxt.append((new, A, 0, X, out))           # Wait(B), blocks if B = 0
        elif pc == 6:            nxt.append((new, A, B, X, out + '#'))     # Print(#)
        elif pc == 7:            nxt.append((new, A, 1, X, out))           # Signal(B): B = 1
        # pc == 8: this process has finished, nothing to add
    return nxt

# Start: all processes at line 0, A = 1, B = 0, X = 0, nothing printed.
# stack = states still to explore; seen = states already explored (so no
# state is explored twice); outputs = final printed texts.
outputs, seen, stack = set(), set(), [((0, 0, 0), 1, 0, 0, '')]
while stack:
    s = stack.pop()
    if s in seen:
        continue
    seen.add(s)
    nxt = step(s)
    if not nxt:
        # No process can move: all have finished (or are stuck), so record the output
        outputs.add(s[4])
    stack += nxt                 # explore all the next states later

print("All possible outputs:", sorted(outputs))
# Check each option from the question against the list
for label, pat in [('i)', '**$*###'), ('ii)', '**$#*##'), ('iii)', '**$##*#'), ('iv)', '***$###')]:
    print(f"{label:5s} {pat}: {'possible' if pat in outputs else 'not possible'}")
