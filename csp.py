from collections import deque
import random
from collections import defaultdict

class Csp:

    # arcs : list of tuples (Xi, Xj) of variables in the CSP sharing at least one binary constraint (if a constraint involves 2 variables, for example A > B, then in this list must appear (A, B) and (B, A). The graph must be directed )
    # domains: dict where a variable is linked to its domain (a set of values). In this dict there is a key for each variable of the CSP (even if the variable does not share a binary constraint)
    # constraints: dict where the key is a tuple (Xi, Xj) and the value is a list of constraints (lambda function with 2 parameters and a condition on these two)
    def __init__(self, arcs : list, domains : dict, constraints : dict):
        self._arcs = arcs
        # check if the domains at least contain one element (if not the CSP has no solutions)
        for value in domains.values():
            if not value: # empty set
                raise ValueError('The domains of the variables must contain at least one value. The given CSP has no solutions')
        self._domains = domains
        self._constraints = constraints
        self._queue = deque()
        
            
            
    '''
    ----------------------------------
    AC-3 Algorithm part
    '''

    def runAc3(self):
        
        self._queue.clear() # clear the deque, maybe some algorithm has inserted something in
        # popolating the queue with all the arcs (variables that shares at least one binary constraint)
        for el in self._arcs:
            self._queue.append(el)
            
        while self._queue:
            (Xi, Xj) = self._queue.popleft()
            updated = self.updateDomain((Xi, Xj))
            if updated:
                if not self._domains[Xi]:
                    return self._domains.copy(), False # returns the domains (the user can se that the domain of Xi is empty) and a flag to inform that there are no solutions
                self.recheckArcs(Xi)
        return self._domains, True


    def updateDomain(self, arc):
        """
        For an arc (Xi, Xj) this function check if Xi is arc-consistent with Xj. For each constraint between Xi and Xj it will be checked
        if every value in the domain of Xi has a value in the domain of Xj that together satisfies the constraint. If this does not happen then
        the value will be removed from Xi domain, causing a re-check of arc-consistency between (Xk, Xi), where Xk is a variable that shares a binary constraint
        with Xi
        """     
        updatedDomainXi = False
        (Xi, Xj) = arc

        # values to remove because there are no corrispondence for some constraint
        valrem : set = set()

        for constraint in self._constraints[arc]:
            for vi in self._domains[Xi]:
                foundValue = False
                for vj in self._domains[Xj]:
                        if constraint(vi, vj):
                            foundValue = True
                            break
                if not foundValue:
                    valrem.add(vi)

        if valrem:
            updatedDomainXi = True

        for value in valrem:
            self._domains[Xi].discard(value)

        return updatedDomainXi

    def recheckArcs(self, var_updated):
        """
        If a domain of a variable has been changed, then we have to check the consistency between
        all the variables that shares a constraint with the variable that has changed domain
        """

        # converting the queue in a set to have the belonging test efficient
        queue_set = set(self._queue)
        for (Xi, Xj) in self._arcs:
            if Xj == var_updated and (Xi, Xj) not in queue_set:
                self._queue.append((Xi, Xj))
                queue_set.add((Xi, Xj)) # to avoid duplicates (Xi, Xj) in self._arcs

    def _printDomains(self):
        """
        This method is intended to return the solution of AC-3 well-printed, human like. So for each variable is indicated the corresponding domain after the process.
        That method should be called by the programmer of this class because if this function were called after an object instantiation the domains would be the initial ones (not the solution domains)
        """
        for var, domain in self._domains.items():
            print(str(var) + ": {", end="")
            for value in domain:
                print(str(value) + ", ", end="")
            print("")

    '''
    ------------------------------------------
    '''
    
    '''
    ------------------------------------------
    Min conflicts part
    '''
    
    def runMinConflicts(self, maxsteps):
        """
        Given a CSP and maximum number of step to compute, this method tries to solve the CSP using Min-Conflicts. 
        This method return an assignment, a boolean value that states if the assignment is valid for the CSP and the step of computation that Min-Conflict 
        took to return the assignment (wether valid or invalid)
        """
        # generating a complete and random assignment
        assignment = {}
        
        for var, domain in self._domains.items():
            assignment[var] = random.choice(list(domain)) # choosing 1 random element in the set (domain)
        
        # starting with min-conflicts
        i = 0
        while i < maxsteps:
            # check if the assignment satisfies the constraints
            if self.check_assignment(assignment):
                return assignment, True, i
            
            # choosing a random variable that violates at least one constraint
            var = self.get_conflicted_variable(assignment)
            # the value to choose is the value that minimize the conflicts in the current assignment
            value = self.get_random_value(var, assignment)
            assignment[var] = value
            i += 1
            
        return assignment, False, maxsteps
    
    def check_assignment(self, assignment):
        
        # for each arc (Xi, Xj) (binary constraint), I'll check if the assignment satisfies the constraints between Xi and Xj
        for (Xi, Xj) in self._arcs:
            for constraint in self._constraints[(Xi, Xj)]:
                if not constraint(assignment[Xi], assignment[Xj]):
                    return False
        return True
    
    def get_conflicted_variable(self, assignment):
        """
        This methods select a random variable that violates at least one constraint of this CSP. 
        """
        conflicted_vars = set() 
        
        for (Xi, Xj) in self._arcs:
            
            if Xi in conflicted_vars:
                continue
            
            for constraint in self._constraints[(Xi, Xj)]:
                if not constraint(assignment[Xi], assignment[Xj]):
                    conflicted_vars.add(Xi)
                    break
        if not conflicted_vars:
            return None # this does never happen in the algorithm because if none variable has at least 1 conflict, the assigned previously checked would have been returned as a solution
        return random.choice(list(conflicted_vars))
    
    def get_random_value(self, var, assignment):
        """ 
        This method selects the value for var that minimizes the conflicts with the other assigned variables.
        Directly modifies assignment[var] during computation, which is safe in this context.
        """
        conflicts_per_value = {}
        for value in self._domains[var]:
            counter = 0
            assignment[var] = value
            for (Xi, Xj) in self._arcs:
                if Xi == var or Xj == var:
                    for constraint in self._constraints[(Xi, Xj)]:
                        if not constraint(assignment[Xi], assignment[Xj]):
                            counter += 1
            conflicts_per_value[value] = counter
        
        # returns the value that minimize the conflicts
        min_conflicts = min(conflicts_per_value.values())
        best_values = [ v for v, c in conflicts_per_value.items() if c == min_conflicts]
        # if there are multiple best values will be chosen one of these randomically
        return random.choice(best_values)
        

    '''
    ----------------------
    Backtracking search part
    '''            
    
    def runBacktrackingSearch(self): 
        pass
    
    
    def degreeHeuristic(self, assignment):
        """ 
        This method returns an unassigned variable following the degree heuristic. This heuristic choose to assign a value to the variable involved in 
        the greatest number of constraints among other unassigned variables.
        Assigned must be a dict where each key is a variable of the CSP and the value is the assigned value for the variable, or False is the variable is unassigned
        """
        num_constraints = {}

        unassigned = [v for v in assignment if assignment[v] == False]

        if not unassigned:
            return None

        for v in unassigned:
            num_constraints[v] = 0
            for (Xi, Xj) in self._arcs:
                if Xi == v and Xj in unassigned:
                    num_constraints[Xi] += len(self._constraints[(Xi, Xj)])
        max_degree = max(num_constraints.values())
        bests = [v for v, deg in num_constraints.items() if deg == max_degree]
        return random.choice(bests)


    def lcsHeuristic(self, assignment, var):
        """
        This method returns the value to be assigned to the variable var (the parameter one) in the current step of the backtracking search. The value the least constraining value, so the value that does not permit
        the minimum number of assignment to other unassigned variables in the CSP
        """
        unassigned = [v for v in assignment if assignment[v] == False]
        unassigned_neighbors = [Xj for (Xi, Xj) in self._arcs if Xi == var and Xj in unassigned]
        num_constraint_for_values = defaultdict(int)

        for value in self._domains[var]:
            for Xj in unassigned_neighbors:
                for constraint in self._constraints[(var, Xj)]:
                    num_constraint_for_values[value] += sum([1 for value2 in self._domains[Xj] if not constraint(value, value2)])

        min_constraints = min(num_constraint_for_values.values())
        bests = [v for v, c in num_constraint_for_values.items() if c == min_constraints]
        return random.choice(bests)
    
    

        
