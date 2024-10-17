# Tree-Sitter or Clang

## Context and Problem Statement

Althought tree_sitter is a powerfull tool for parsing, it brings some limitation when trying to look for the semantic value of a desired expression.That's why it was considered use SSA to construct the e-graph.

<!-- This is an optional element. Feel free to remove. -->
## Decision Drivers

* Semantic Analysis of certain expressions
* Advantages of the format
* The representation of the expressions in each form

## Considered Options

* Tree-Sitter
* CLang - LLVM

## Decision Outcome

Chosen option: "CLang - LLVM", because

* Working over SSA, makes it more efficient to determine the value of expression.
* Makes certain cases easier to analize.
* Does not represent the code as a Tree, what simplifies the translation to e-graphs expressions.
