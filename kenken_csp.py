from cspbase import *
import itertools
import numpy as np
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    domain = []

    for n in range(1, kenken_grid[0][0] + 1):
        domain.append(n)

    cons = []
    vars = initialize_vars(domain)

    for row in range(len(domain)):
        for col in range(len(domain)):
            cons.extend(binary_not_equal_row(vars, row, col))
            cons.extend(binary_not_equal_col(vars, row, col))

    csp = CSP("binary_ne_grid")

    for v in vars:
        for j in v:
            csp.add_var(j)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars

def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)

    vars = initialize_vars(domain)

    cons = []
    cons.extend(n_ary_all_different(vars, len(domain)))

    csp = CSP("nary_ad_grid")

    for v in vars:
        for j in v:
            csp.add_var(j)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars

def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)

    vars = initialize_vars(domain)

    cons = []

    # Modified code from nqueens problem in test.py
    for cage in range(len(kenken_grid)):
        # Forced value to a cell
        if len(kenken_grid[cage]) == 2:
            i = int(str(kenken_grid[cage][0])[0]) - 1
            j = int(str(kenken_grid[cage][0])[1]) - 1
            vars[i][j] = Variable('V{}{}'.format(i, j), [kenken_grid[cage][1]])
        # larger cage
        elif len(kenken_grid[cage]) > 2:
            # number of variables in the current cage
            num_vars = len(kenken_grid[cage]) - 2

            cage_values = []
            cage_values_domain = []
            satisfying_tuples = []

            # Get vars in cage
            for cell in range(num_vars):
                cell_i = int(str(kenken_grid[cage][cell])[0]) - 1
                cell_j = int(str(kenken_grid[cage][cell])[1]) - 1

                cage_values.append(vars[cell_i][cell_j])
                cage_values_domain.append(vars[cell_i][cell_j].domain())

            con = Constraint("C(C{})".format(cage), cage_values)

            for cells in itertools.product(*cage_values_domain):
                # Generate all the operations for kenken
                # Addition and multiplication values do not need to check for permutations
                if kenken_grid[cage][-1] == 0:
                    actual = 0
                    for var in cells:
                        actual += var
                    if actual == kenken_grid[cage][-2]:
                        satisfying_tuples.append(cells)
                elif kenken_grid[cage][-1] == 3:
                    total = 1
                    for var in cells:
                        total *= var
                    if total == kenken_grid[cage][-2]:
                        satisfying_tuples.append(cells)
                # Check permutation values for subtract and division
                elif kenken_grid[cage][-1] == 1:
                    # Get all possible orderings of the cells
                    for order in itertools.permutations(cells):
                        actual = order[0]
                        for var in range(1, len(order)):
                            actual -= order[var]
                        # if this permutation is correct, add it to satisfying tuples
                        if actual == kenken_grid[cage][-2]:
                            satisfying_tuples.append(cells)
                elif kenken_grid[cage][-1] == 2:
                    # Get all possible orderings of cells
                    for order in itertools.permutations(cells):
                        actual = order[0]
                        for var in range(1, len(order)):
                            actual //= order[var]
                        # if this permutation is correct, add it to satisfying tuples
                        if actual == kenken_grid[cage][-2]:
                            satisfying_tuples.append(cells)

            con.add_satisfying_tuples(satisfying_tuples)
            cons.append(con)

    for row in range(len(domain)):
        for col in range(len(domain)):
            cons.extend(binary_not_equal_row(vars, row, col))
            cons.extend(binary_not_equal_col(vars, row, col))

    csp = CSP("kenken_grid")

    for v in vars:
        for j in v:
            csp.add_var(j)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars

#### HELPER FUNCTIONS ####

def initialize_vars(domain):
    variables = []
    for row in domain:
        curr = []
        for col in domain:
            curr.append(Variable('V{}{}'.format(row, col), domain))
        variables.append(curr)
    return variables

def n_ary_all_different(vars, n):

    constraints = []
    x = 0
    # loop through all rows and cols and collect list of them
    for i in range(n):
        satisfying_tuples = []
        row = []
        col = []
        for j in range(n):
            row.append(vars[i][j])
            col.append(vars[j][i])
        # add to constraint
        con_row = Constraint("C(V{}{}{})".format(i, j, x), row)
        con_col = Constraint("C(V{}{}{})".format(j, i, x), col)

        x += 1

        for tup in itertools.product(vars[i], repeat=n):
            sat = True
            for x in range(n):
                for j in range(n):
                    if x != j:
                        if tup[x] == tup[j]:
                            sat = False
            if sat:
                satisfying_tuples.append(tup)

        con_row.add_satisfying_tuples(satisfying_tuples)
        con_col.add_satisfying_tuples(satisfying_tuples)
        constraints.append(con_row)
        constraints.append(con_col)

    return constraints


def binary_not_equal_row(vars, row, col):
    constraints = []
    # FORMAT COPIED FROM NQUEENS IN TEST.PY
    for i in range(len(vars[row])):
        satisfying_tuples = []
        # compare with only values occurring after, since values occurring before is already compared
        if i <= col:
            continue
        curr = vars[row][col]
        next = vars[row][i]
        con = Constraint("C(V{}{}{}{})".format(row, col, row, i), [curr, next])

        for tup in itertools.product(curr.domain(), next.domain()):
            # For each tuple, ensure that they are not equal
            if tup[0] != tup[1]:
                satisfying_tuples.append(tup)

        con.add_satisfying_tuples(satisfying_tuples)
        constraints.append(con)

    return constraints

def binary_not_equal_col(vars, row, col):
    constraints = []
    # FORMAT COPIED FROM NQUEENS IN TEST.PY
    for i in range(len(vars[col])):
        satisfying_tuples = []
        # compare with only values occurring after, since values occurring before is already compared
        if i <= row:
            continue
        curr = vars[row][col]
        next = vars[i][col]
        con = Constraint("C(V{}{}{}{})".format(row, col, i, col), [curr, next])

        # For each tuple, ensure that they are not equal
        for tup in itertools.product(curr.domain(), next.domain()):
            # For each tuple, ensure that they are not equal
            if tup[0] != tup[1]:
                satisfying_tuples.append(tup)

        con.add_satisfying_tuples(satisfying_tuples)
        constraints.append(con)

    return constraints
