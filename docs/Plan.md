# SAME Rules Thesis Plan

## Research Questions

- What other tools are useful for this type of analysis?
- What are the advantages of using egglogs python binding?
- How to compare two .c files semantically using Egraphs?
- Can we indicate if the semantics of a piece of code can be found inside a .c file?
- What kind of sintaxis works best when writing patterns?

## Itinerary

### May / June

- Compare two .c files with the first version of the tool.
- Adapt tool to pass most Test Cases.

### July

- Finish adapting Test Cases.
- Start writing Patterns used for tool.
- Create comparable code from the Patterns.

### August

- Find Patterns in Code.
- Start writing paper.

### September

- First Draft.

## Timeline

```mermaid
    gantt
        dateFormat DD-MMM-YY
        axisFormat %b %d, %Y
        todayMarker off
        Initializer: dummy, 14-May-25, 3m
        section Match Whole Files
            Readapt Tool: redo, 21-May-25, 14d
            Pass Test Cases : pass_tests, 28-May-25, 30d
        section Match with Patterns
            Write Patterns Sintax : pattern1, after pass_tests, 7d
            Write Code from Patterns : pattern2, after pattern1, 14d
            Match Patterns with code : pattern3, 17-Jul-25, 14d
        section Writing
            First Draft : write1, 29-Jul-25, 21d
```
