# Decisions made during the implementation of the GSA Transform Algorithm

## Context and Problem Statement

The GSA Transform Algorithm is the main algorithm used to convert the SSA representation to a GSA representation, which should facilitate the analysis done in the egraph.
The Algorithm some what complex and may be missing some edge cases.

## Decision Drivers

* How easy is to implement
* Time needed to implement
* Number of concepts needed to implement it

## Considered Options

* Tu-Padua Algorithm
* Replace existing phi nodes with the GSA nodes.

## Decision Outcome

Chosen option: "Replace existing phi nodes", because
this one is way easier to implement and understand, we also make use of the phi nodes placed by mem2reg. The implemented version is quite simple as it doesn't cover complex cases where a phi node may have more than 2 incoming values depending on the structure of the CFG, we also consider only cases where loops have only one exit block.

## Pros and Cons of the Options

### Tu-Padua Algorithm

* Good, because is a robust algorithm which covers various cases
* Good, because can be used to place the phi nodes without the need of calling mem2reg
* Neutral, because as the implemented algorithm it does not cover all cases, needs to be refactor to include cases like handling multiple incoming values for phi nodes.
* Bad, because is very theory heavy. Although it has been proven to work (and even mem2reg applies it), it requiers many graph traversal concepts.
