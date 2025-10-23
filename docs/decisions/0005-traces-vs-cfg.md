# What to use: Function Traces vs Function CFG

## Context and Problem Statement

As a first approach it was decided to calculate the different execution traces of a function and upload these information in the E-graph.
Given by the exponencial complexity of calculating all the differnts path of a graph, it was debated whether we should use the whole CFG in the E-graph
or just stick the execution traces route.

## Decision Drivers

* Time Complexity of Problem.
* Perfomance impact of the approach.
* How easy is to solve in E-graph.
* Code Modification

## Considered Options

* Keep Execution Traces as is.
* Use CFG to analize program.

## Decision Outcome

Chosen option: Use CFG to analize program, because there is too much difference in the time complexity between uploading all of the execution traces and uploading only the CFG, to have some context calculating all of the traces could have a complexity of 2^(number of branches) while only uploading the CFG has a complexity of (number of nodes). Besides the way the traces were solved in the E-graph was similar to a possible approach to solve the E-graph with a CFG. Also uploading the CFG is relatively simple with existing code used to calculate traces (instead of using a DFS with a queue we will use traditional BFS).

### Consequences

* Good, because reduces time complexity significatly.
* Bad, because requires a new approach to solving the problem.
* Bad, because requires code refactoring.
