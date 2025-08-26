import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csp import Csp
from runAc3 import CspAc3Runner

def main(runAc3First=False):
    """Main function to run AC-3 followed by Min-Conflicts"""
    
    print("=== CSP Solver: Min-Conflicts ===\n")
    
    tester = CspAc3Runner()
    
    # first run AC-3 interactively if the user wants it
    tester.run_interactive_test(solve=runAc3First)
    
    print("="*30)
    print("Now it's time to run the Min-Conflicts algorithm ... ")
    # get CSP instance with domains updated by AC-3
    csp = tester.return_csp()
    
    # check if all domains have at least one element after AC-3
    if any(len(domain) == 0 for domain in csp._domains.values()):
        print("Cannot run Min-Conflicts: One or more domains are empty. The CSP is unsatisfiable")
        return
    
    # get max steps for Min-Conflicts
    valid = False
    while not valid:
        try:
            max_steps = int(input("Enter the max steps that Min-Conflicts can do trying to solve the CSP (e.g. 100000)"))
            if max_steps > 0:
                valid = True
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    
    
    # running Min-Conflicts
    assignment, validSol, steps = csp.runMinConflicts(max_steps)
    
    if validSol:
        print("Here's a possible solution for the CSP:")
        for var, value in assignment.items():
            print(f"{var} ==> {value}")
        print(f"This solution tooks {steps} steps to Min-Conflicts to find")
    else:
        print("Min-Conflicts couldn't find a solution within the given steps.")

if __name__ == "__main__":
    valid = False
    while not valid:
        ac3 = input("1 - run AC-3 first and then Min-Conflicts on the CSP that you will insert \n2 - run directly Min-Conflicts \n")
        try:
            ac3 = int(ac3)
            if ac3 in [1,2]:
                valid = True
            else:
                print("You need to insert 1 or 2")
        except ValueError:
            print("You need to insert a number (1 or 2)")
    main(runAc3First=(ac3==1))