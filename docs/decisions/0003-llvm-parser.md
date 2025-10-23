# Tools used to parse LLVM files

## Context and Problem Statement

Given that we are now working an LLVM IR of the code, we need different parsing tools for such files.

## Decision Drivers

* Ease of use.
* Previous experience with the parsers.
* Readability of the tools Grammar.
* How easy is to integrate into the project.

## Considered Options

* A combination of Parsimonious and llvmlite
* TatSu
* Lark(1)

## Decision Outcome

Chosen option: "TatSu", because

* TatSu grammar is easy to define and powerful as it lets one give shape to the output from it.
* TatSu allows one to define whitespaces, which the parser will ignore. As contrast to Parsimonios, in which one needs to input each space character manually, creating a really bloated grammar and difficult to understand.
* Had access to people who had already worked with TatSu and Parsimonious.
* TatSu doesn't require the use of visitors, simplifying the integration process.
