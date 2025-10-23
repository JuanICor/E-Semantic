# Semantic Analysis tecnique

## Context and Problem Statement

To match functions within the E-graph one needs to define a set of rules that will be executed, there are multiple approaches that can be used.
As Egglog is considered a programming language there are consideration of using already defined algorithms used in Static Analysis.

## Considered Options

* Abstract Interpretation in a symbolic domain
* Abstract Interpretation in a relations domain
* Semantic Equivalent Rewrites

## Decision Outcome

Chosen option: "Semantic Equivalent Rewrites", because
{justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

## Pros and Cons of the Options

### Abstract Interpretation

* Good, because it's got a strong mathematical background.
* Good, because simplifies some parts of the implemantation.
* Good, because can cover more cases without so many rules.
* Bad, because complexity is fairly high
* Bad, because requires some code transformations which are really expensive.

### Semantic Rewrites

* Good, because easy to implement.
* Good, because it's easy to create rules for said analysis.
* Good, because easy to extend later on.
* Neutral, because requires some not so complex algorithms.
* Bad, because can not be as exhaustive.
* Bad, because requires much more rules to cover all test cases.
