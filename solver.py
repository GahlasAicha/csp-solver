# fonctionnement d'un solveur CSP

from constraint import Constraint, Var, Value
from csp import CSP
from typing import Dict, List, Optional
import time

class Solver:
    def __init__(self):
        # 
        self.nbNodes = 0 # contiendra le nombre de noeuds créés dans l'arbre de recherche
        self.nbSolutions = 0 # contiendra le nombre de solutions trouvées
        self.solutions:dict[int, Dict[Var, Value]] = {} # contiendra les solutions trouvées
        self.nbFailures = 0 # contiendra le nombre d'échecs, ie. le nombre de fois que le domaine d'une variable `var` est vide (|D_{var}| = 0)
        self.starttime = 0 # contiendra le temps de résolution du problème

    #
    def check_if_solution(self, csp) -> bool: # TODO
        '''
        Vérifier si le CSP est satisfait et enregistrer la solution dans self.solutions
        Retourne True si solution et False sinon
        '''
        if csp.singleton() and not csp.check_unsat():
            sol = csp.solution()
            self.solutions[self.nbSolutions] = sol
            self.nbSolutions += 1
            return True
        return False


    def check_if_failure(self, csp) -> bool: # TODO
        '''
        Vérifier si le CSP ne peut être satisfait
        Retourne True si échec et False sinon
        '''
        # on verifie que le domaine de chaque variable n'est pas vide, sinon c'est un échec
        if csp.emptyDomain():
            self.nbFailures = self.nbFailures+1
            return True
        if csp.singleton() and csp.check_unsat():
            self.nbFailures = self.nbFailures+1
            return True
        return False
    #
    def select_unassigned_variable(self, csp, search:str="seq") -> Var: # TODO
        '''
        Retourner une variable dont le domaine n'est pas singleton
        '''
        unassigned_vars = [var for var in csp.variables if len(csp.domains[var]) > 1]
        if not unassigned_vars:
            return None
        if search == "minDom":
            return min(unassigned_vars, key=lambda var: len(csp.domains[var]))
       
        return csp.unassignedVar()

    # 
    def backtracking_search(self, csp, search:str="seq", k:float=float('inf')): # TODO
        '''
        Fonction qui réalise l'algorithme backtracking,
        lorsqu'on arrive à une solution on affiche la solution,
        puis continuer pour trouver toutes les solutions
        '''
        if self.nbSolutions >= k:
            return
        
        self.nbNodes += 1

        if self.check_if_solution(csp):
            return
        if self.check_if_failure(csp):
            return
        var = self.select_unassigned_variable(csp, search)
        if var is None:
            return
        values = list(csp.domains[var])
        for val in values:
            if self.nbSolutions >= k:break
            domains_copy = csp.domainsCopy()
            csp.domains[var] = [val]
            self.backtracking_search(csp, search, k) 
            csp.domains = domains_copy
    


    # 
    def forward_checking(self, csp, X): # TODO
        '''
        Forward checking du CSP avec la variable X qui vient d'être instanciée.
        Retourne False si un domaine devient vide, True sinon
        '''
        # pour chaque contrainte qui contient X, on revise les variables voisines de X
        for contrainte in csp.vcList[X]:
            for variable_voisine in contrainte.variables:
                # on ne revise pas la variable X elle-même
                if variable_voisine != X:
                    if contrainte.revise(variable_voisine, csp.domains):
                        if len(csp.domains[variable_voisine]) == 0:
                            return False
        return True
               
    # 
    # 
    # 
    def bt_forward(self, csp, search:str="seq", k:float=float('inf')): # TODO
        '''
        Fonction qui réalise l'algorithme backtracking avec forward checking
        lorsqu'on arrive à une solution on affiche la solution,
        puis continuer pour trouver toutes les solutions
        '''
        if self.nbSolutions >= k:
            return
        self.nbNodes = self.nbNodes+1 
        if self.check_if_solution(csp):
            return 
        if self.check_if_failure(csp):
            return
        var = self.select_unassigned_variable(csp, search) 
        if var is None:
            return
        values = list(csp.domains[var])
        for val in values:
            if self.nbSolutions >= k: break
            domains_copy = csp.domainsCopy()
            csp.domains[var] = [val]
            if self.forward_checking(csp, var):
                self.bt_forward(csp,  search, k)
            else:
                self.nbFailures += 1
                
            csp.domains = domains_copy

    # 
    # 
    # 
    # 
    def bt_propagation(self, csp, choixAC, search:str="seq", k:float='inf'): # TODO
        '''
        Fonction qui réalise l'algorithme backtracking avec propagation de contraintes.
        La propagation est effectuée par `choixAC` (AC-1 ou AC3)
        lorsqu'on arrive à une solution on affiche la solution
        puis continuer pour trouver toutes les solutions
        '''
        if self.nbSolutions >= k:
            return
        self.nbNodes += 1

        if self.check_if_solution(csp):
            return
        
        if self.check_if_failure(csp):
            return
        
        var = self.select_unassigned_variable(csp, search)
        if var is None:
            return
        values = list(csp.domains[var])
        for val in values:
            if self.nbSolutions >= k: break
            domains_copy = csp.domainsCopy()
            csp.domains[var] = [val]
            success = True
            if choixAC == "AC1":
                success = self.propagate_AC1(csp)
            elif choixAC == "AC3":
                success = self.propagate_AC3(csp)
            else:
                raise ValueError("choixAC doit être AC1 ou AC3")
            if success:
                self.bt_propagation(csp, choixAC, search, k)
            else:
                self.nbFailures += 1
            csp.domains = domains_copy

        

    # 
    def propagate_AC1(self, csp): # TODO
        '''
        le CSP a seulement des contraintes binaires
        '''
        while True :
            revised = False
            for contraint in csp.ctrList:
                for var in contraint.variables:
                    if contraint.revise(var, csp.domains):
                        if len(csp.domains[var]) == 0:
                            return False
                        revised = True
            if not revised:
                break
        return True
        
    
    # 
    def propagate_AC3(self, csp): # TODO
        '''
        le CSP a seulement des contraintes binaires
        '''
        queue = []
        for contraint in csp.ctrList:
            vars = contraint.variables 
            if len(vars) == 2:
                queue.append((contraint, vars[0], vars[1]))
                queue.append((contraint, vars[1], vars[0]))

                while len(queue) > 0:
                    contraint, var1, var2 = queue.pop(0)
                    if contraint.revise(var1, csp.domains):
                        if len(csp.domains[var1]) == 0:
                            return False
                        for contraint2 in csp.vcList[var1]:
                            if contraint2 != contraint:
                                vars2 = contraint2.variables
                                if len(vars2) == 2:
                                     # On ajoute l'arc pointant vers var1
                                     voisin = vars2[0] if vars2[1] == var1 else vars2[1]
                                     queue.append((contraint2, voisin, var1))
        return True

    #
    def solve_all(self, csp:CSP, algo:str="backtracking", choixAC:str="AC1", search:str="seq",k=float('inf')): # TODO
        '''
        Fonction qui réalise la résolution du problème en choisissant l'algorithme et la méthode de propagation
        '''
        self.nbNodes = 0
        self.nbSolutions = 0
        self.nbFailures = 0
        self.solutions = {}
        self.starttime = time.perf_counter()
        print(f"\n Lancement : {algo.upper()} (Mode: {search} ,Max solutions: {k})")
        if algo == "propagation": print(f" Filtrage initial : {choixAC}")
        if algo == "backtracking":
            self.backtracking_search(csp, search, k)
        elif algo == "forward" or algo == "bt_forward":
            self.bt_forward(csp, search, k)
        elif algo == "propagation":
            if choixAC not in ["AC1", "AC3"]:
                raise ValueError("choixAC doit être AC1 ou AC3")
            
            if choixAC == "AC1":
                self.propagate_AC1(csp)
            elif choixAC == "AC3":
                self.propagate_AC3(csp)
            # on lance la recherche avec propagation 
            self.bt_propagation(csp, choixAC, search, k)
        else:
            raise ValueError("algo doit être backtracking, forward ou propagation")
        self.print_statistics()



    def print_statistics(self):
        '''Afficher les statistiques de la résolution du problème'''
        execution_time = time.perf_counter() - self.starttime
        print("Statistiques de la résolution")
        print("-" * 30)
        print(f"Nombre de noeuds créés : {self.nbNodes}")
        print(f"Nombre de solutions trouvées : {self.nbSolutions}")
        print(f"Nombre d'échecs : {self.nbFailures}")
        print(f"temps de résolution : {execution_time*1000:.6f} ms")
        print("="*30 + "\n")

        if self.nbSolutions > 0:
            print("Solutions trouvées :")
            for i, sol in self.solutions.items():
                print(f"Solution {i+1} : {sol}")
        else:
            print("Aucune solution trouvée.")
        