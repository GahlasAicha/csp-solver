from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar

#Var = 'str'
Var = TypeVar('str') # type pour variable
#Value = 'int'
Value = TypeVar('int') # type pour domaine

# 
class Constraint(ABC):
    '''Classe pour les contraintes'''
    # constructeur initie les variables
    def __init__(self, variables: List[Var]) -> None:
        '''
        Crée une contrainte avec les variables

        Parameters
        ----------
        variables : List[Var]
        '''
        #
        self.variables = variables
        '''liste des variables de la contrainte'''
        #

    # fonctions à redéfinir pour chaque contrainte
    @abstractmethod
    def unsat(self, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Tester si les domaines sont en conflit dans la contrainte
        Retourner True s'il y a un conflit (la contrainte est donc unsatisfaisable) et False sinon
        '''
        ...

    # fonctions à redéfinir pour chaque contrainte
    @abstractmethod
    def checkSupport(self, var: Var, value: Value, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Tester si la valeur `value` de la variable `var` a un support et
        retourner True si oui et False sinon
        '''
        ...
        
    # 
    def revise(self, revisedVar, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Enlever les valeurs sans support de la variable `revisedVar` et
        retourner True si ces valeurs existent
        '''
        listRem = []
        for val in domains[revisedVar]:
            if self.checkSupport(revisedVar, val, domains) == False:
                listRem.append(val)
        for val in listRem:
            domains[revisedVar].remove(val)
        if len(listRem)==0:
            return False
        return True

# 
class Different(Constraint):
    '''Contrainte v1 != v2'''
    def __init__(self, v1, v2) -> None:
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2

    def unsat(self, domains: Dict[str, List[int]]) -> bool: 
       for val1 in domains[self.v1]:
           for val2 in domains[self.v2]:
               if val1 != val2:
                   return False
       return True
       
    def checkSupport(self, var, value, domains) -> bool: # Tester si une valeur  𝑣𝑎𝑙𝑢𝑒∈𝐷𝑣𝑎𝑟 a un support
        if var == self.v1:
            for val2 in domains[self.v2]: 
                if value != val2: 
                    return True
        else:
            for val1 in domains[self.v1]: # var == self.v2 
                if value != val1: 
                    return True
        return False

# 
class Superior(Constraint):
    '''Contrainte v1 > v2'''
    def __init__(self, v1: str, v2:str):
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2
    
    def unsat(self, domains: Dict[str, List[int]]) -> bool: 
        for val1 in domains[self.v1]:
            for val2 in domains[self.v2]:
                if val1 > val2: 
                    return False
        return True

    
    def checkSupport(self, var, value, domains) -> bool: # TODO
        if var == self.v1:
            for val2 in domains[self.v2]: 
                if value > val2: 
                    return True # value a u support dans le domaine de v2
        else: # var == self.v2
            for val1 in domains[self.v1]: 
                if value < val1: 
                    return True # value a u support dans le domaine de v1
        return False # value n'a pas de support dans le domaine de l'autre variable
class SumSup(Constraint):
    '''Contrainte v1 + v2 > a'''
    def __init__(self, v1: str, v2:str, a:int):
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2
        self.a = a
    
    def unsat(self, domains: Dict[str, List[int]]) -> bool: # TODO
        for val1 in domains[self.v1]:
            for  val2 in domains[self.v2]:
                if val1 + val2 > self.a: 
                    return False
        return True
    
    def checkSupport(self, var, value, domains) -> bool: # TODO
        if var == self.v1:
            for val2 in domains [self.v2]: 
                if value + val2 > self.a: 
                    return True 
        else: # var == self.v2
            for val1 in domains[self.v1]: 
                if value + val1 > self.a: 
                    return True
        return False
    

class Table(Constraint):
    '''Contrainte définie en extension (la table liste les tuples satisfaisant la contrainte)'''
    def __init__(self, varList, tupleTable):
        super().__init__(varList)
        self.table = tupleTable
        
    def unsat(self, domains: Dict[str, List[int]]) -> bool: # TODO
        for t in self.table :
            compatible = True
            for i, var in enumerate (self.variables):
                if t[i] not in domains[var]:
                    compatible=False
                    break
            if compatible:
                return False
        return True


    
        
    def checkSupport(self, var, value, domains) -> bool: # TODO
        varIndex = self.variables.index(var)
        for t in self.table:
            if t[varIndex] == value: # si la valeur est dans la table
                compatible = True
                for i, var_name in enumerate(self.variables):
                    if i != varIndex and t[i] not in domains[var_name]: # si les autres valeurs du tuple ne sont pas dans les domaines
                        compatible = False
                        break
                if compatible:
                    return True # la valeur a un support dans la table
        return False # la valeur n'a pas de support dans la table
