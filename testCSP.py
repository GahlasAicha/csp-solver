from solver import Solver
from csp import  CSP
from constraint import *
from typing import Dict, List, Optional

if __name__ == "__main__":
    variables: List[str] = ["x", "y","z"]
    domains: Dict[str, List[int]] = {}
    for var in variables:
        domains[var] = [1, 2, 3]
    csp = CSP(variables, domains)
    csp.add_constraint(Different("x", "y"))
    csp.add_constraint(Superior("x", "z"))

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
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #solver.nbNodes = 0
    #solver.solve_all(csp, "backtracking", None)
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")
    #print("===========================================\n\n")
    #
    #solver.nbNodes = 0
    #solver.solve_all(csp, "forward", None)
    #print("Number of nodes: ",solver.nbNodes)
   # print("\n\n===========================================")
    #solver.nbNodes = 0
    #solver.solve_all(csp, "propagation", "AC3")
   # print("Number of nodes: ",solver.nbNodes)
   # print("\n\n===========================================")
    #solver.nbNodes = 0
   # solver.solve_all(csp, "propagation", "AC1")
    #print("Number of nodes: ",solver.nbNodes)
    #print("\n\n===========================================")


    ## test avec k  
    print("\n" + " TEST DE k PROGRESSIF ".center(40, '='))
    
    valeurs_k = [1, 3, 10] 

    for k_test in valeurs_k:
        solver.nbNodes = 0 # On réinitialise pour chaque test
        solver.nbSolutions = 0
        solver.solutions = {}
        
        print(f"\n>>> Test avec k = {k_test} :")
        solver.solve_all(csp, "backtracking", search="seq", k=k_test)
        
        print(f"  - Solutions trouvées : {solver.nbSolutions}")
        print(f"  - Noeuds explorés    : {solver.nbNodes}")
        
        # Vérification logique
        if solver.nbSolutions > k_test:
            print("  [ERREUR] : Le solveur n'a pas respecté la limite k !")
        elif solver.nbSolutions == k_test:
            print(f"  [OK] : Limite k={k_test} atteinte exactement.")
        else:
            print(f"  [INFO] : Toutes les solutions ({solver.nbSolutions}) ont été trouvées avant d'atteindre k={k_test}.")

    print("\n" + "="*40)

    print("\n" + " TEST HEURISTIQUE minDom ".center(40, '='))
    
    #  On repart de domaines neufs pour éviter les effets de bord
    new_domains = {var: [1, 2, 3] for var in variables}
    csp_minDom = CSP(variables, new_domains)
    csp_minDom.add_constraint(Different("x", "y"))
    csp_minDom.add_constraint(Superior("x", "z"))

    #  On réinitialise le solver
    solver.nbNodes = 0
    solver.nbSolutions = 0
    solver.solutions = {}

    #  On lance avec search="minDom"
    solver.solve_all(csp_minDom, algo="backtracking", search="minDom")

    print(f"  - Solutions trouvées : {solver.nbSolutions}")
    print(f"  - Noeuds explorés     : {solver.nbNodes}")
    print("\n" + "="*40)