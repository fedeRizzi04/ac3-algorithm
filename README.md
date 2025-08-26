# CSP Solver: AC-3 and Min-Conflicts Implementation

A Python implementation of two popular algorithms for solving Constraint Satisfaction Problems (CSPs): AC-3 (Arc Consistency 3) and Min-Conflicts.

## Overview

This project provides:
- **`csp.py`**: Core CSP class with both AC-3 and Min-Conflicts algorithms
- **`run_algorithms/runAc3.py`**: Interactive interface for AC-3 algorithm testing
- **`run_algorithms/runMinConflicts.py`**: Combined AC-3 + Min-Conflicts solver

The AC-3 algorithm enforces arc consistency by removing inconsistent values from variable domains, while Min-Conflicts uses local search to find complete solutions by iteratively fixing constraint violations.

## Files Description

### `csp.py`
Contains the main `Csp` class that implements both:
- **AC-3 Algorithm**: Domain reduction through arc consistency
- **Min-Conflicts Algorithm**: Local search for complete solutions

### `run_algorithms/runAc3.py`
Provides the `CspAc3Runner` class with an interactive interface to:
- Define variables and their domains
- Add constraints between variables
- Solve the CSP using AC-3
- Display reduced domains

### `run_algorithms/runMinConflicts.py`
Provides flexible CSP solving with two options:
1. **AC-3 + Min-Conflicts**: First runs AC-3 to reduce domains, then applies Min-Conflicts
2. **Min-Conflicts only**: Runs Min-Conflicts directly on original domains

The user can choose which approach to use at runtime.

## Usage

### Running AC-3 Only

```bash
cd run_algorithms
python3 runAc3.py
```

This will run the AC-3 algorithm to reduce variable domains based on constraints.

### Running Min-Conflicts (with choice of approach)

```bash
cd run_algorithms
python3 runMinConflicts.py
```

When you run this, you'll be prompted to choose:
- **Option 1**: Run AC-3 first, then Min-Conflicts on reduced domains
- **Option 2**: Run Min-Conflicts directly on original domains

**Option 1** is recommended for complex CSPs as AC-3 can significantly reduce the search space.
**Option 2** follows the standard Min-Conflicts approach and may be better for some problems where domain reduction could eliminate useful values.

### Using Input Files

You can automate input using text files:

```bash
python3 runMinConflicts.py < input_file.txt
```

Example input file format:
```
1
a,b,c,d
1,3,4
1,3,4
1,2,3
1,2,3
a!=b
b!=a
a>d
d<a
done
100000
```

The first line specifies the choice:
- `1` for AC-3 + Min-Conflicts
- `2` for Min-Conflicts only

### Example Session

Here's a complete example showing the choice between approaches:

```
1 - run AC-3 first and then Min-Conflicts on the CSP that you will insert 
2 - run directly Min-Conflicts 
1

=== Interactive CSP AC-3 Test ===

1. Enter variables
Enter variables separated by commas (e.g., A,B,C): a,b,c

2. Domain input
Enter the domain for a (values separated by comma): 1,2,3
Enter the domain for b (values separated by comma): 1,2,3
Enter the domain for c (values separated by comma): 1,2,3

3. Constraints input
Enter constraint (or 'done' to finish): a>b
Enter constraint (or 'done' to finish): b<a
Enter constraint (or 'done' to finish): b>c
Enter constraint (or 'done' to finish): c<b
Enter constraint (or 'done' to finish): done

4. CSP resolution with AC-3
=== RESULTS ===
The CSP might have solutions!

Domains after AC-3:
  a: {3}
  b: {2}
  c: {1}

==============================
Now it's time to run the Min-Conflicts algorithm...
Enter the max steps: 100000

Here's a possible solution for the CSP:
a ==> 3
b ==> 2
c ==> 1
Min-Conflicts took 2 steps to find this solution 
```

## Constraint Formats

The system supports several constraint formats:

### Comparison Constraints
- **Equality**: `A=B`, `A==B`
- **Inequality**: `A!=B`, `A<>B`
- **Ordering**: `A<B`, `A>B`, `A<=B`, `A>=B`

### Absolute Value Constraints
- **Exact difference**: `|A-B|=2`
- **Minimum difference**: `|A-B|>1`
- **Maximum difference**: `|A-B|<3`
- **Range**: `|A-B|>=1`, `|A-B|<=4`

### Custom Lambda Constraints
Type `custom` to enter custom lambda functions:
```
First variable: a
Second variable: b
lambda x, y: (x + y) % 2 == 0
```

## Important Notes

## Requirements

- Python 3.x

## Important Notes

### Node Consistency (Preprocessing Required)
**Node consistency must be enforced manually as a preprocessing step.** Before running the algorithms, you must remove any values from variable domains that violate unary constraints (constraints involving only one variable).

Examples of unary constraints:
- `X > 5`: Remove all values ≤ 5 from X's domain
- `Y % 2 == 0`: Keep only even values in Y's domain
- `Z != 3`: Remove value 3 from Z's domain

**The algorithms in this project only handle binary constraints (between two variables). Unary constraints must be resolved by manually filtering domains before defining the CSP. Other types of constraint must be turned into binary ones**

### Bidirectional Constraints
**All constraints must be entered in both directions manually.** This design choice ensures explicit control over the CSP definition (AC-3 works with a directed graph representation of the CSP).

Examples:
- For `A > B`, you must enter both `A>B` AND `B<A`
- For `A = B`, you must enter both `A=B` AND `B=A`
- For `|A-B|=2`, you must enter both `|A-B|=2` AND `|B-A|=2`

### Variable Names
- Variables can be uppercase or lowercase letters (e.g., A, b)
- Multi-character variable names are supported (e.g., `var1`, `abc`)

### Domain Values
- Domains can contain integers or strings
- Values are automatically converted to integers when possible
- Mixed domains (integers and strings) are supported



