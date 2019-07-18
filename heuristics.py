'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''
import operator
import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    # store a list of seen constraints
    seen = dict()

    # check all constraints to see which has the longest list of unassigned vars
    for con in csp.get_all_cons():
        # list of variables that the constraint is over
        for var in con.get_scope():
            if var not in seen:
                seen[var] = con.get_n_unasgn()
            else:
                seen[var] += con.get_n_unasgn()

    # find the max in the dict
    if seen:
        return max(seen, key=seen.get)
    else:
        return None

def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    # Initialize to a negative value
    min_domain = None
    min_var = None

    # Loop through unassigned values
    for var in csp.get_all_unasgn_vars():
        # first iteration of loop
        if not min_domain:
            min_domain = var.cur_domain_size()
            min_var = var

        # there is a value smaller than current min
        if var.cur_domain_size() < min_domain:
            min_domain = var.cur_domain_size()
            min_var = var

    return min_var

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    result = dict()
    for value in var.cur_domain():
        var.assign(value)
        # store number of non valid tuples
        num = 0
        for con in csp.get_cons_with_var(var):
            for variable in con.get_unasgn_vars():
                # count number of values in current domain
                for val in variable.cur_domain():
                    # if no supporting tuple, it is more constraining
                    if not con.has_support(variable, val):
                        num += 1
        var.unassign()
        result[value] = num

    if result:
        # Sort from least constraining to most constraining
        return sorted(result, key=result.get, reverse=False)
    else:
        return None
