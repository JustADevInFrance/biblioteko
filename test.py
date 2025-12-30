from typing import List, Tuple, Optional

#!/usr/bin/env python3
# GitHub Copilot
# Illustrative example contrasting a polynomial 2-SAT solver (in P)
# with a brute-force 3-SAT solver (NP-style exponential).
# Save as /C:/Users/tomme/Desktop/PJE/biblioteko/test.py


# Utilities for literal <-> index mapping
# Literals are integers: k (means variable k true), -k (means variable k false)
# Variables are 1..n. Internally each variable has two nodes:
# index = 2*(k-1) + (0 for true, 1 for false). Negation flips lowest bit (^1).
def lit_to_index(lit: int) -> int:
    v = abs(lit) - 1
    return 2 * v + (0 if lit > 0 else 1)

def neg_index(idx: int) -> int:
    return idx ^ 1

# 2-SAT solver using implication graph + Kosaraju SCC (linear time O(n+m))
def solve_2sat(n: int, clauses: List[Tuple[int, int]]) -> Tuple[bool, Optional[List[bool]]]:
    N = 2 * n
    g = [[] for _ in range(N)]
    gr = [[] for _ in range(N)]
    def add_imp(u: int, v: int):
        g[u].append(v)
        gr[v].append(u)
    # For each clause (a OR b), add (~a -> b) and (~b -> a)
    for a, b in clauses:
        add_imp(lit_to_index(-a), lit_to_index(b))
        add_imp(lit_to_index(-b), lit_to_index(a))
    # Kosaraju: order by finish time on g
    seen = [False] * N
    order = []
    def dfs1(u: int):
        seen[u] = True
        for w in g[u]:
            if not seen[w]:
                dfs1(w)
        order.append(u)
    for i in range(N):
        if not seen[i]:
            dfs1(i)
    comp = [-1] * N
    cid = 0
    def dfs2(u: int, cid: int):
        comp[u] = cid
        for w in gr[u]:
            if comp[w] == -1:
                dfs2(w, cid)
    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cid)
            cid += 1
    # Check contradictions: variable and its negation in same component -> unsat
    for var in range(n):
        if comp[2*var] == comp[2*var + 1]:
            return False, None
    # Build assignment: variable is true if component(var_true) > component(var_false)
    # (components are in reverse topological order)
    assignment = [False] * n
    for var in range(n):
        assignment[var] = comp[2*var] > comp[2*var + 1]
    return True, assignment

# Brute-force 3-SAT solver (exponential time). Clauses are tuples of 3 literals.
def solve_3sat_bruteforce(n: int, clauses: List[Tuple[int, int, int]]) -> Tuple[bool, Optional[List[bool]]]:
    if n >= 25:
        # avoid huge search in examples
        raise ValueError("n too large for brute-force demo")
    for mask in range(1 << n):
        assign = [(mask >> i) & 1 == 1 for i in range(n)]
        ok = True
        for a, b, c in clauses:
            def lit_val(lit: int) -> bool:
                return assign[abs(lit) - 1] if lit > 0 else not assign[abs(lit) - 1]
            if not (lit_val(a) or lit_val(b) or lit_val(c)):
                ok = False
                break
        if ok:
            return True, assign
    return False, None

# Example usages
if __name__ == "__main__":
    # 2-SAT examples
    # Variables: 1,2,3
    # Clauses are pairs (a OR b)
    clauses_sat = [(1, 2), (-1, 3), (-3, 2)]  # satisfiable
    clauses_unsat = [(1, 2), (-1, 2), (1, -2), (-1, -2)]  # forces contradiction on var1/var2 combination -> unsat

    sat, assign = solve_2sat(3, clauses_sat)
    print("2-SAT example (satisfiable):", sat, "assignment:", assign)
    sat2, assign2 = solve_2sat(2, clauses_unsat)
    print("2-SAT example (unsatisfiable):", sat2)

    # 3-SAT examples (small n because brute force)
    # Variables: 1..4
    clauses3 = [(1, 2, 3), (-1, -2, 4), (-3, -4, 2)]
    sat3, assign3 = solve_3sat_bruteforce(4, clauses3)
    print("3-SAT brute-force result:", sat3, "assignment:", assign3)

    # Note:
    # - 2-SAT is solvable in polynomial time (example above uses linear-time SCC algorithm).
    # - 3-SAT is NP-complete; the brute-force solver above is exponential in n.
    # This script demonstrates the practical difference: certain SAT fragments (2-SAT) are in P,
    # while general SAT (3-SAT) requires exponential search unless P=NP (unknown).