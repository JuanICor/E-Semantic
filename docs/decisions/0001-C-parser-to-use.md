# Library for parsing

## Context and Problem Statement

Which library provides the best tools for parsing C code?
Which library enables a quick search through the code we are parsing?

## Decision Drivers

* How easy it is to use.
* Previous experience with the library.
* Ease of use with mypy.

## Considered Options

* PyCParcer
* Tree_Sitter

## Decision Outcome

Chosen option: "Tree_Sitter", because

* It's easy to use, gives the user full access to the AST.
* Provides a power query mechanism, which allows for a easy search over the AST.
* Already compatible with mypy
