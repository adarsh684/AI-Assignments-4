# CSP FUNCTIONS
def is_consistent(var, value, assignment, neighbors):
    for neighbor in neighbors.get(var, []):
        if assignment.get(neighbor) == value:
            return False
    return True


def select_unassigned_variable(variables, assignment, domain, neighbors):  # MRV heuristic
    unassigned = [v for v in variables if v not in assignment]

    return min(
        unassigned,
        key=lambda v: sum(
            1 for val in domain[v]
            if is_consistent(v, val, assignment, neighbors)
        )
    )


def backtrack(variables, domain, neighbors, assignment):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_variable(variables, assignment, domain, neighbors)

    for value in domain[var]:
        if is_consistent(var, value, assignment, neighbors):
            assignment[var] = value
            
            result = backtrack(variables, domain, neighbors, assignment)
            if result:
                return result

            del assignment[var]

    return None