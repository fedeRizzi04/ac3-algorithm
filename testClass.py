from ac3 import CspAc3Solver

class CspAc3Tester:

    def __init__(self):
        self.variables = set()
        self.domains = {}
        self.constraints = {}
        self.arcs = []

    def run_interactive_test(self):
        """Runs a complete interactive test of the CSP"""
        print("=== Interactive CSP AC-3 Test ===\n")

        try:
            self._input_variables()
            self._input_domains()
            self._input_constraints()
            self._solve_and_display()
        except Exception as e:
            print(f"\nError during execution: {e}")

    def _input_variables(self):
        """Input CSP variables"""
        print("1. Enter variables")
        var_input = input("Enter variables separated by commas (e.g., A,B,C): ")
        self.variables = {var.strip() for var in var_input.split(',')}
        print(f"Variables entered: {sorted(self.variables)}\n")

    def _input_domains(self):
        """Input domains for each variable"""
        print("2. Domain input")
        for var in sorted(self.variables):
            domain_input = input(f"Enter the domain for {var} (values separated by comma): ")
            try:
                # Try to convert to integers, otherwise keep as strings
                domain_values = []
                for val in domain_input.split(','):
                    val = val.strip()
                    try:
                        domain_values.append(int(val))
                    except ValueError:
                        domain_values.append(val)
                self.domains[var] = set(domain_values)
            except:
                self.domains[var] = {val.strip() for val in domain_input.split(',')}

        print("\nDomains entered:")
        for var, domain in self.domains.items():
            print(f"  {var}: {domain}")
        print()

    def _input_constraints(self):
        """Input constraints between variables"""
        print("3. Constraints input")
        print("IMPORTANT: You need to enter BOTH directions for ALL constraints!")
        print("Examples:")
        print("  - For A > B, you must enter both: A>B AND B<A")
        print("  - For A = B, you must enter both: A=B AND B=A")
        print("  - For |A-B|=2, you must enter both: |A-B|=2 AND |B-A|=2")
        print("\nSupported formats:")
        print("  - Equality: A=B, A==B (enter both directions!)")
        print("  - Inequality: A!=B, A<>B (enter both directions!)")
        print("  - Comparison: A<B, A>B, A<=B, A>=B (enter both directions!)")
        print("  - Absolute difference: |A-B|=2, |A-B|>1 (enter both directions!)")
        print("  - Custom: type 'custom' to enter lambda")

        while True:
            constraint_input = input("\nEnter constraint (or 'done' to finish): ").strip()

            if constraint_input.lower() == 'done':
                break

            if constraint_input.lower() == 'custom':
                self._input_custom_constraint()
                continue

            constraint_func = self._parse_constraint(constraint_input)
            if constraint_func:
                var1, var2, func = constraint_func
                self._add_unidirectional_constraint(var1, var2, func)

        self._generate_arcs()
        print(f"\nGenerated arcs: {len(self.arcs)}")
        print(f"Total constraints: {sum(len(c) for c in self.constraints.values())}")
        
        # Show constraint details for debugging
        print("\nConstraint details:")
        for arc, funcs in self.constraints.items():
            print(f"  Arc {arc}: {len(funcs)} constraint(s)")
        print()

    def _parse_constraint(self, constraint_str):
        """Automatic parsing of most common constraints"""
        constraint_str = constraint_str.replace(' ', '')

        # Pattern for constraint of equality/inequality
        import re

    def _parse_constraint(self, constraint_str):
        """Automatic parsing of constraints - returns unidirectional constraint only"""
        constraint_str = constraint_str.replace(' ', '')

        # Pattern for constraint of equality/inequality
        import re

        # |A-B|=n, |A-B|>n, etc. - Now unidirectional, user must enter both directions
        abs_pattern = r'\|([A-Za-z]+)-([A-Za-z]+)\|([<>=!]+)(\d+)'
        abs_match = re.match(abs_pattern, constraint_str)
        if abs_match:
            var1, var2, op, value = abs_match.groups()
            value = int(value)
            if var1 in self.variables and var2 in self.variables:
                if op == '=':
                    func = lambda x, y: abs(x - y) == value
                    return var1, var2, func
                elif op == '>':
                    func = lambda x, y: abs(x - y) > value
                    return var1, var2, func
                elif op == '<':
                    func = lambda x, y: abs(x - y) < value
                    return var1, var2, func
                elif op == '>=':
                    func = lambda x, y: abs(x - y) >= value
                    return var1, var2, func
                elif op == '<=':
                    func = lambda x, y: abs(x - y) <= value
                    return var1, var2, func

        # A op B pattern - All unidirectional now
        simple_pattern = r'([A-Za-z]+)([<>=!]+)([A-Za-z]+)'
        simple_match = re.match(simple_pattern, constraint_str)
        if simple_match:
            var1, op, var2 = simple_match.groups()
            if var1 in self.variables and var2 in self.variables:
                if op == '=' or op == '==':
                    func = lambda x, y: x == y
                    return var1, var2, func
                elif op == '!=' or op == '<>':
                    func = lambda x, y: x != y
                    return var1, var2, func
                elif op == '<':
                    func = lambda x, y: x < y  # Only A < B
                    return var1, var2, func
                elif op == '>':
                    func = lambda x, y: x > y  # Only A > B
                    return var1, var2, func
                elif op == '<=':
                    func = lambda x, y: x <= y  # Only A <= B
                    return var1, var2, func
                elif op == '>=':
                    func = lambda x, y: x >= y  # Only A >= B
                    return var1, var2, func

        print(f"Constraint format not recognized: {constraint_str}")
        return None

    def _input_custom_constraint(self):
        """Input of a custom constraint"""
        var1 = input("First variable: ").strip()
        var2 = input("Second variable: ").strip()

        if var1 not in self.variables or var2 not in self.variables:
            print("Invalid variables!")
            return

        print("Enter the lambda function (use 'x' for the first variable and 'y' for the second)")
        print("Example: x + y == 10, x != y, x % 2 == y % 2")

        lambda_str = input("lambda x, y: ")
        try:
            constraint_func = eval(f"lambda x, y: {lambda_str}")
            self._add_unidirectional_constraint(var1, var2, constraint_func)
            print(f"Unidirectional constraint added: {var1}, {var2} -> lambda x, y: {lambda_str}")
            print(f"Remember to add the reverse constraint {var2}, {var1} if needed!")
                
        except Exception as e:
            print(f"Error in lambda function: {e}")

    def _add_unidirectional_constraint(self, var1, var2, constraint_func):
        """Adds a unidirectional constraint for a single arc"""
        arc = (var1, var2)
        
        if arc not in self.constraints:
            self.constraints[arc] = []
        
        self.constraints[arc].append(constraint_func)

    def _add_constraint(self, var1, var2, constraint_func1, constraint_func2):
        """Adds a bidirectional constraint with proper reverse logic"""
        arc1 = (var1, var2)
        arc2 = (var2, var1)

        if arc1 not in self.constraints:
            self.constraints[arc1] = []
        if arc2 not in self.constraints:
            self.constraints[arc2] = []

        self.constraints[arc1].append(constraint_func1)
        self.constraints[arc2].append(constraint_func2)

    def _generate_arcs(self):
        """Generates the list of arcs from constraints"""
        self.arcs = list(self.constraints.keys())

    def _solve_and_display(self):
        """Solves the CSP and shows results"""
        print("4. CSP resolution with AC-3")
        print("Initial domains:")
        for var, domain in self.domains.items():
            print(f"  {var}: {domain}")

        try:
            solver = CspAc3Solver(self.arcs, self.domains.copy(), self.constraints)
            result_domains, has_solution = solver.solve()

            print("\n=== RESULTS ===")
            if has_solution:
                print("The CSP might have solutions!")
                print("\nDomains after AC-3:")
                for var, domain in result_domains.items():
                    print(f"  {var}: {domain}")
            else:
                print("✗ The CSP has no solutions!")
                print("\nDomains at failure:")
                for var, domain in result_domains.items():
                    status = "EMPTY" if not domain else str(domain)
                    print(f"  {var}: {status}")

        except Exception as e:
            print(f"\nError during solving: {e}")


def main():
    """Main function to start the test"""
    tester = CspAc3Tester()
    tester.run_interactive_test()


if __name__ == "__main__":
    main()