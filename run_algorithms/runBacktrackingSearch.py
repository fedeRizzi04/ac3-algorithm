# python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csp import Csp
from runAc3 import CspAc3Runner


def printSolutions(solutions):
    if len(solutions) == 0:
        print("The CSP hasn't any solution")
        return

    print("The CSP has " + str(len(solutions)) + " solutions: ")
    counter = 0

    for sol in solutions:
        print(str(counter+1) + "):")
        for k, v in sol.items():
            print(str(k) + "=" + str(v))
        print("-----------------")
        counter += 1

def main(runAc3First=False):
    """Main function to optionally run AC-3 followed by Backtracking Search"""
    print("=== CSP Solver: Backtracking Search ===\n")

    tester = CspAc3Runner()
    tester.run_interactive_test(solve=runAc3First)

    print("="*30)
    print("Now it's time to run the Backtracking Search algorithm ... ")
    csp = tester.return_csp()

    if any(len(domain) == 0 for domain in csp._domains.values()):
        print("Cannot run Backtracking Search: One or more domains are empty. The CSP is unsatisfiable")
        return


    result = csp.runBacktrackingSearch()
    printSolutions(result)


if __name__ == "__main__":
    valid = False
    while not valid:
        ac3 = input("1 - run AC-3 first and then Backtracking Search on the CSP that you will insert \n2 - run directly Backtracking Search \n")
        try:
            ac3 = int(ac3)
            if ac3 in [1,2]:
                valid = True
            else:
                print("You need to insert 1 or 2")
        except ValueError:
            print("You need to insert a number (1 or 2)")
    main(runAc3First=(ac3==1))