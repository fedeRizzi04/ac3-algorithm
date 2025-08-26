from collections import deque


class CspAc3Solver:

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
        for el in self._arcs:
            self._queue.append(el)

    def solve(self):
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
