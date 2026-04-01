from csp import is_consistent, select_unassigned_variable

def crypt_constraint(assignment):
    def val(x):
        return assignment.get(x)

    letters = ['T','W','O','F','U','R']

    # all-different
    assigned_vals = [val(l) for l in letters if val(l) is not None]
    if len(assigned_vals) != len(set(assigned_vals)):
        return False

    # leading zero
    if val('T') == 0 or val('F') == 0:
        return False

    # column constraints
    if all(val(x) is not None for x in ['O','R','C1']):
        if val('O') + val('O') != val('R') + 10*val('C1'):
            return False

    if all(val(x) is not None for x in ['W','U','C1','C2']):
        if val('W') + val('W') + val('C1') != val('U') + 10*val('C2'):
            return False

    if all(val(x) is not None for x in ['T','O','C2','C3']):
        if val('T') + val('T') + val('C2') != val('O') + 10*val('C3'):
            return False

    if val('C3') is not None and val('F') is not None:
        if val('C3') != val('F'):
            return False

    return True

def backtrack(variables, domain, neighbors, assignment):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_variable(variables, assignment, domain, neighbors)

    for value in domain[var]:
        if is_consistent(var, value, assignment, neighbors):
            assignment[var] = value
            if crypt_constraint(assignment):
                result = backtrack(variables, domain, neighbors, assignment)
                if result:
                    return result

            del assignment[var]

    return None

variables = ['T','W','O','F','U','R','C1','C2','C3']

domain = {v: list(range(10)) for v in variables}

domain['C1'] = [0,1]
domain['C2'] = [0,1]
domain['C3'] = [0,1]

letters = ['T','W','O','F','U','R']
neighbors = {v: [] for v in variables}

for v in letters:
    neighbors[v] = [u for u in letters if u != v]

solution = backtrack(variables, domain, neighbors, {})
if solution:
    T, W, O = solution['T'], solution['W'], solution['O']
    F, U, R = solution['F'], solution['U'], solution['R']

    two = 100*T + 10*W + O
    four = 1000*F + 100*O + 10*U + R

    print("Cryptarithmetic CSP ")
    print("Problem: TWO + TWO = FOUR\n")

    print("Letter Assignments:")
    print(f" T = {T}, W = {W}, O = {O}, F = {F}, U = {U}, R = {R}\n")

    print("Verification:")
    print(f" {two} + {two} = {four} ")
else:
    print("No solution found")