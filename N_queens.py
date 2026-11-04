from solver import Solver
from csp import CSP
from constraint import Table, Different
from typing import List, Dict
import time

def solve_nqueens(n: int, algo: str, search_mode: str, ac_type: str = "AC1"):
    # Variables : une reine par colonne
    variables: List[str] = [f"q{i}" for i in range(n)]
    
    #  Domaines : chaque reine peut être sur une ligne de 1 à n
    domains: Dict[str, List[int]] = {
        var: list(range(1, n + 1)) for var in variables
    }

    csp = CSP(variables, domains)

    #  Ajout des contraintes
    for i in range(n):
        for j in range(i + 1, n):
            # Contrainte : Pas sur la même ligne
            csp.add_constraint(Different(f"q{i}", f"q{j}"))

            # Contrainte : Pas sur la même diagonale (via une Table)
            authorized_tuples = []
            for r1 in range(1, n + 1):
                for r2 in range(1, n + 1):
                    # Pas la même ligne
                    if r1 == r2:
                        continue
                    # Diagonale : |r1 - r2| != |i - j|
                    if abs(r1 - r2) != abs(i - j):
                        authorized_tuples.append([r1, r2])
            
            csp.add_constraint(Table([f"q{i}", f"q{j}"], authorized_tuples))

    #  Résolution
    solver = Solver()
    

    # k est fixé à 10 pour limiter la recherche
    solver.solve_all(csp, algo, ac_type, search_mode, 10)

if __name__ == "__main__":
    N_QUEENS = 7
    
    print("="*55)
    print(f" TEST DE PERFORMANCE : {N_QUEENS}-REINES ".center(55, '='))
    print("="*55)

    # Test 1 : Backtracking Classique (Séquentiel)
    # solver.solve_all(csp, "backtracking", "AC1", "seq", 10)
    solve_nqueens(N_QUEENS, "backtracking", "seq")

    # Test 2 : Backtracking + minDom (MRV)
    # solver.solve_all(csp, "backtracking", "AC1", "minDom", 10)
    solve_nqueens(N_QUEENS, "backtracking", "minDom")

    # Test 3 : Propagation AC3 + minDom
    # solver.solve_all(csp, "propagation", "AC3", "minDom", 10)
    solve_nqueens(N_QUEENS, "propagation", "minDom", ac_type="AC3")

    print("\n" + "="*55)