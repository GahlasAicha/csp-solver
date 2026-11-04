from solver import Solver
from csp import  CSP
from constraint import *
from typing import Dict, List, Optional

if __name__ == "__main__":
    variables: List[str] = ["A", "B","C", "D", "E", "F"]
    domains: Dict[str, List[int]] = {}
    for var in variables:
        domains[var] = [1, 2, 3, 4, 5]
    csp = CSP(variables, domains)
    csp.add_constraint(Superior("B", "A"))
    csp.add_constraint(Superior("D", "A"))
    csp.add_constraint(Superior("E", "A"))
    csp.add_constraint(Superior("C", "B"))
    csp.add_constraint(Superior("D", "B"))
    csp.add_constraint(Superior("E", "B"))
    csp.add_constraint(Superior("D", "C"))
    csp.add_constraint(Superior("C", "F"))
    csp.add_constraint(Superior("E", "D"))
    csp.add_constraint(Superior("E", "F"))
    #csp.add_constraint(Superior("A", "E"))
    
    solver = Solver()
    #
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.backtracking_search(csp)
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.nbNodes = 0
    #solver.bt_forward(csp,None)
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.nbNodes = 0
    #solver.bt_propagation(csp,"AC1")
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.nbNodes = 0
    #solver.bt_propagation(csp,"AC3")
    #print("Number of nodes: ",solver.nbNodes)
   # print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.nbNodes = 0  
    #solver.solve_all(csp, "forward", "AC3")
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
   # print("===========================================\n\n")
    #

    solver.nbNodes = 0
    solver.solve_all(csp, "backtracking", None)
    print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #
    solver.nbNodes = 0
    solver.solve_all(csp, "forward", None)
    print("Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    solver.nbNodes = 0
    solver.solve_all(csp, "propagation", "AC3")
    print("Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    solver.nbNodes = 0
    solver.solve_all(csp, "propagation", "AC1")
    print("Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")  
