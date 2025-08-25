# AC-3 Algorithm Implementation

An implementation of the AC-3 (Arc Consistency 3) algorithm for solving Constraint Satisfaction Problems (CSPs) in Python.

## Overview

This project provides:
- **`ac3.py`**: Core AC-3 algorithm implementation
- **`testClass.py`**: Interactive testing interface for CSP problems 

The AC-3 algorithm enforces arc consistency by removing values from variable domains that cannot be part of any solution, helping to solve or simplify CSPs.

## Files Description

### `ac3.py`
Contains the `CspAc3Solver` class that implements the AC-3 algorithm.

### `testClass.py`
Provides the `CspAc3Tester` class with an interactive interface to:
- Define variables and their domains
- Add constraints between variables
- Solve the CSP using AC-3
- Display results

## Usage

### Running the Interactive Tester

```bash
python3 testClass.py
```

### Example Session

Here's a complete example of solving a simple CSP:

```
=== Interactive CSP AC-3 Test ===

1. Enter variables
Enter variables separated by commas (e.g., A,B,C): a,b,c

2. Domain input
Enter the domain for a (values separated by comma): 1,2,3
Enter the domain for b (values separated by comma): 1,2,3
Enter the domain for c (values separated by comma): 1,2,3

3. Constraints input
IMPORTANT: You need to enter BOTH directions for ALL constraints!
Examples:
  - For A > B, you must enter both: A>B AND B<A
  - For A = B, you must enter both: A=B AND B=A
  - For |A-B|=2, you must enter both: |A-B|=2 AND |B-A|=2

Enter constraint (or 'done' to finish): a>b
Enter constraint (or 'done' to finish): b<a
Enter constraint (or 'done' to finish): b>c
Enter constraint (or 'done' to finish): c<b
Enter constraint (or 'done' to finish): done

4. CSP resolution with AC-3
Initial domains:
  a: {1, 2, 3}
  b: {1, 2, 3}
  c: {1, 2, 3}

=== RESULTS ===
The CSP has solutions!

Domains after AC-3:
  a: {3}
  b: {2}
  c: {1}
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

### Bidirectional Constraints
**All constraints must be entered in both directions manually.** This design choice ensures explicit control over the CSP definition (AC-3 works with a directed graph representation of the CSP).

Examples:
- For `A > B`, you must enter both `A>B` AND `B<A`
- For `A = B`, you must enter both `A=B` AND `B=A`
- For `|A-B|=2`, you must enter both `|A-B|=2` AND `|B-A|=2`

### Variable Names
- Variables can be uppercase or lowercase letters
- Multi-character variable names are supported (e.g., `var1`, `abc`)

### Domain Values
- Domains can contain integers or strings
- Values are automatically converted to integers when possible
- Mixed domains (integers and strings) are supported

## Algorithm Details

The AC-3 algorithm works by:

1. **Initialization**: All arcs (Xi, Xj) are added to a queue
2. **Processing**: For each arc, values that don't satisfy constraints are removed
3. **Propagation**: When a domain changes, related arcs are re-queued
4. **Termination**: Process continues until no more changes occur

## Requirements

- Python 3.x



