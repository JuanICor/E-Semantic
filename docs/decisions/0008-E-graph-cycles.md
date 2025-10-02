# How to represent loop iterable values in the E-graph

## Context and Problem Statement

When uploading converting the CGF to the e-graph representation (a VDG) a problem occurd as egg, the tool used to represent E-graphs, does not allow the insertion of cycles.
In our inicial approach the representation was based on the one given in the paper [Evaluating Value-Graph Translation Validation for LLVM](https://dl.acm.org/doi/10.1145/1993498.1993533).
The main difference is that said approach was implemented on a in-house tool that allowed the modification of existing nodes thus facilitating the introduction of cycles in the e-graph.

## Decision Drivers

* Cleanest approach
* Least error prone
* Complexity

## Considered Options

* Introduce a temporary node
* Use a fix-point combinator like node
* Use a RVSDG representation

## Decision Outcome

Chosen option: "{title of option 1}", because
{justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

<!-- This is an optional element. Feel free to remove. -->
## Validation

{describe how the implementation of/compliance with the ADR is validated. E.g., by a review or an ArchUnit test}

<!-- This is an optional element. Feel free to remove. -->
## Pros and Cons of the Options

### {title of option 1}

<!-- This is an optional element. Feel free to remove. -->
{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
<!-- use "neutral" if the given argument weights neither for good nor bad -->
* Neutral, because {argument c}
* Bad, because {argument d}
* … <!-- numbers of pros and cons can vary -->

### {title of other option}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
* Neutral, because {argument c}
* Bad, because {argument d}
* …

## More Information

In the official egg github there was a conversation on how to introduce cycles to the e-graph <https://github.com/egraphs-good/egg/discussions/106>,
in said conversation both ideas of introducing a temporary node and using a RVSDG were mentioned, being the accepted answer the one that mentioned the RVSDGs.
Also in the latest _Zulip_ conversation seems like that approach is the one that is still being used.
