# Analysis

## Semantic Program Alignment for Equivalence Checking - Berkeley Churchill

This paper was read with the objective of finding a procedure which could facilitate the implementation of Static Analysis using Abstract Interpretation.

The paper talks about a tool used to decide if two programs are semantically equivalent by aligning said programs into one.
At first the author metions previous tools that tried to align two separate programs into one by different methods, and mentions that previous tools always lacked a correct analysis for modern optimizations, majority of them being related with loops.
So the author gives a description of how the created tool works.
As a main input the tool takes the functions to compare and a suit of test cases, which are used to create a set of alignment predicates (or weak invariants) with must hold true in both functions.
Then for alignment predicate a trace alignment is calculated in both functions, which is used to construct a Program Alignment Automaton (PAA).
Finally the viability of the PAA is checked using the original test cases, and the PAA is used to learn an invariat which is used for check the proof obligations.

The main objective of this study was to know how the program alignment worked as it could be usefull in the context of doing Abstract Interpretation using a relations domain.
Although powerful this tool presented a lot of shortcomings when thinking how to introduce it into our program.
First of all, this tool is based on an already existing code which could take a lot of time to understand and try to implement by our selfs.
Secondly, when running the tool's test functions (found in its github repository) test cases based on short functions could take around 3 - 4 minutes. This could mean that said tool might not be the correct one to handle bigger functions, which our program will be used for.
Finally, our programs main objective is to decide whether a certain user pattern can be found within another source code, which means that we aren't necessarilly comparing two functions, and the pattern we will be working with do not contain a lot information about how the code works, this may complicate the process of creating the alignment predicates, which in consequence will make the programs alignments to be wrong.

## Evaluating Value-Graph Translation Validation for LLVM - Jean Baptiste Tristan

The paper talks about a validation tool called LLVM-MD, this tool is based on the LLVM optimizer with the difference that this tools certifies that the optimizations done are semantically sound.
The verification is done using Transalation Validation, which is a static analysis technique. This technique was first created as a way to validate that each process/tranformation done by a compiler did not changed the semantic value of the compiled program. Now a day this technique is used to validate that two programs are semantically equal.
Programs are represented as value-graphs (or Program Expression Graphs), this are graphs containing:

* Operator nodes, for example “plus”, “minus”, or any of our built-in nodes for representing conditionals and loops
* “Dataflow” edges that specify where operator nodes get their arguments from.

Some of the properties of this value-graphs are the following:

* They are _referentially transparent_, which means that the value of an expression depends only on the value of its constituent expressions.
* Thet are _complete_, which means that there is no need to maintain any additional representation such as a control flow graph (CFG).

Unlike previous works, LLVM-MD sustains that equality saturation is not needed for the translation validation, in particular for this case they are trying to see if the optimizations done by LLVM are sound, in other works it was mentioned that equality saturation is usefull to try to find all possible optimizations for a program.

LLVM-MD uses a Monadic Gated SSA to represent the analyzed programs, with the goal of making the assembly instructions _referentially transparent_. An import property of this is that it allows us to substitute sub-graphs with equivalent sub-graphs without worrying about computational effects.
Once the Monadic Gated SSA is computed the value graph is created by replacing each variable with its definition. Finally, a set of normalization rules are applied and maximize sharing until the value of the two functions merge into a single node, or we cannot perform any more normalization.

The paper shows some of the rules used to Normalize the value-graph. This rules can be separated into two different sets: General Simplification Rules and Optimization-specific Rules.
The general simplification rules reduce the number of graph nodes by removing unnecessary structure. We say general because these rules only depend on the graph representation, replacing graph structures with smaller, simpler graph structures.
The optimization-specific rules rewrite graphs in a way that mirrors the effects of specific optimizations. These rules do not always make the graph smaller or simpler, and one often needs to have specific optimizations in mind when adding them to the system.

The experiments shown in this paper show that the tool is not a 100% accurate, but it is available cover lots of different cases from different progams and it is also shown how each new rule improved accuracy of the tool.

* Not really applying equality saturation, as the are only checking for equality between programs.
* Rewrites are applied in order. Only generating one possible equivalent program.

## Equality Saturation: A new approach to Optimization - Ross Tate

This paper talks about a tool that improves compilers optimization stage, this tool aims to resolve the phase ordering problem and improve the profitability heuristics that the compilers use. The tool is based on equality analysis over an intermediate representation created by the authors.

The IR used by the tool is a Program Expression Graph (or PEG), which the authors argue is both _referencially transparent_ and _complete_, two properties that help simplify the analysis process.

Some of the benefits provided by this tool are:

* __Optimization Order does not matter__: As they only add new versions of the program with each rewrite and don't destroy previous versions any optimization can be applied in any order.
* __Global Profitability Heuristics__: By using Equality Saturation, they are effectively calculation all possible versions of the optimized program. By using Global Profitability Heuristics, they can select the best optimization for their use case. This is done using a Pseudo-Boolean Evaluator.
* __Translation Validation__: The authors argue that the tool can also be used to determine if two programs are equivalent.

At the end of the Paper the authors show their results in both Time and Space, using a benchmark which contains ~2500 methods, both results are really promising as in Time they get an average of 1.5 seconds, with their slowest process being the one that looks for the best optimization. And Space wise they also got really good results, as using a heap of only 200MB they were able to process all test cases.
