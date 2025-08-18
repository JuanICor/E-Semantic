# SAME Rules Thesis Plan 2.0

## Research Questions

- What other tools are useful for this type of analysis?
- What are the advantages of using egglogs python binding?
- How to compare two .c files semantically using Egraphs?
- Can we indicate if the semantics of a piece of code can be found inside a .c file?
- What kind of sintaxis works best when writing patterns?

## Itinerary

### May / June

- Find all of the programs traces.
- Compare traces using E-graphs.
- Pass Test Cases using new model.

### July

- Start writing Patterns used for tool.
- Create comparable code from the Patterns.
- Find Patterns in Code.
- Start writing paper.

### August

- First Draft.

## Timeline

```mermaid
    gantt
        dateFormat DD-MMM-YY
        axisFormat %b %d, %Y
        todayMarker off
        Initializer: dummy, 17-May-25, 3m
        section Traces
            Find Traces: traces1, 19-May-25, 7d
            Compare Traces: traces2, 24-May-25, 7d
            Pass Test Cases : pass_tests, 30-May-25, 21d
        section Match with Patterns
            Patterns Sintax : pattern1, after pass_tests, 10d
            Code from Pattern : pattern2, after pattern1, 7d
            Match Patterns with code : pattern3, after pattern2, 14d
        section Writing
            First Draft : write1, 22-Jul-25, 21d
```
