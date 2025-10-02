# Approaches used in the proyect

## Choosing a Parser

In the begining the first parser considered were PyCParser and Tree-Sitter, due to some inconvinences with both tools
and advantages brought by the LLVM IR, a hand made parser for LLVM was made.

## Program Representation within the E-Graph

The first approach was based on a kind of Value Dependence Graph in which side effects, brought by instructions like 'store' and 'load'
were represented in a literal way which caused further problems when trying to build the Graph.
As a result the next approach was based on the book written by Reynolds, in which a state is maintained to reflect the values of
each variable and reflect side effects with more consistency, this ended up being more complicated than it should and didn't really
solved the problems that surge with the previous approach while building the Graph.
As a third solution, we tried to use the traces of the program as a way of solving the problems that appeared when building the representation.
This might have been a possible solution but it didn't scale well in bigger programs with a lot of branches.
The fourth approach was using as the representation the Control Flow Graph of the program and use Abstract Interpretation within the Graph
to calculate the semantics of the program. This approach was way to complicated and it needed a pre-processing transformation that was not the
most feasable thing to do.
A paper was found that talked about doing Translation Validation over LLVM programs using E-graphs, based on this paper we tried to us as a Representation a kind of Value Dependece Graph based on the Monadic Gated SSA representation of the code. Unfortunatly Egg, the main tool used in the project to run E-graph, did not allow the insertion of loops within the E-graph. This ended up being an approach killer as the paper required
the introduction of loops in the graph to represent _mu_ nodes.
After finding discussions within egg's repository talking about the above issue, we saw that a lot of people were mentioning a program representation that works really well in Egg's E-graphs. Said representation is the Regionalized Value State Dependance Graph.
