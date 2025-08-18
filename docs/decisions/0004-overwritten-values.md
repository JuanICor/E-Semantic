# Resolve overwritten values problem

## Context and Problem Statement

Due to the way of storing uploaded information into the graph (by using a map that associated variables with their e-graph reference), and because the llvm file was being processed in a linear way, this lead to a problem where if a variable was being used in two different branches then which ever branch was read first, that one could modify the value being used in the second branch.

## Considered Options

* Keep current graph and look for new algorithms to create the value-graph.
* Analyze current graph using Abstract Interpretation.
* Analyze the program by it possible execution traces.

## Decision Outcome

Chosen option: "Analyze the program by it possible execution traces", because
keeping up with current graph has been leading to tons of blocker which had been patched with "clippers", which may lead to more issues in the long run.
Although Abstract Interpretation seemed to be the correct way to solve this problem, understanding how to implemented in the tool may have taken too much time, like for example we could have had to define a proper domain in which our values are located but the actual domain may be to big to actually do it. Further investigation is needed.
Calculating the traces of the program although expensive, is relative simple and quick to implement.

### Consequences

* Good, because easier to implement as we no longer have to deal with branches.
* Bad, because requieres a full redesign of the egraphs structure and rules.
