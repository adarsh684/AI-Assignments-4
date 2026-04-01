from csp import backtrack

STATES = ['WA', 'NT', 'SA', 'Queensland', 'NSW', 'V', 'T']
COLORS = ['Red', 'Green', 'Blue']

CONSTRAINTS = [
    ('WA', 'NT'), ('WA', 'SA'),
    ('NT', 'SA'), ('NT', 'Queensland'),
    ('SA', 'Queensland'), ('SA', 'NSW'), ('SA', 'V'),
    ('Queensland', 'NSW'),
    ('NSW', 'V')
]

def build_neighbors():
    neighbors = {s: set() for s in STATES}
    for a, b in CONSTRAINTS:
        neighbors[a].add(b)
        neighbors[b].add(a)
    return neighbors

NEIGHBORS = build_neighbors()

def solve():
    domain = {s: COLORS for s in STATES}
    solution = backtrack(STATES, domain, NEIGHBORS, {})

    if solution:
        print("Solution Found:\n")
        for state in STATES:
            print(f"{state:12s} → {solution[state]}")
    else:
        print("No solution found.")

    return solution


if __name__ == "__main__":
    solve()
