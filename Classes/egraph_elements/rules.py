from __future__ import annotations
from typing import Iterable

from egglog import ruleset, unstable_combine_rulesets, Unit
from egglog.egraph import rewrite, rule, eq, union, set_, birewrite, delete
from egglog.builtins import (i64, String, Bool, Vec, Map, Set)

from .types import (Function, Trace, State, Instruction, Operand, Var,
                    is_declaration, eval_instructions, semantic_function)


@ruleset
def Function_rules(name: String, name2: String, Trs: Set[Trace]) -> Iterable:
    yield rule(Function(name, Set[Trace].empty())).then(
        is_declaration(Function(name, Set[Trace].empty())))

    yield rule(Function(name, Trs), Function(name2, Trs)).then(
        union(Function(name, Trs)).with_(Function(name2, Trs)))


@ruleset
def Trace_ruleset(Instrs: Vec[Instruction], Instrs2: Vec[Instruction],
                  state: State, state2: State, var: Var) -> Iterable:
    yield rule(Trace(Instrs, State(Map[Var, Operand].empty()))).then(
        union(State(Map[Var, Operand].empty())).with_(
            eval_instructions(Instrs, State(Map[Var, Operand].empty()),
                              i64(0))))

    yield rule(Trace(Instrs, state), Trace(Instrs2, state)).then(
        union(Trace(Instrs, state)).with_(Trace(Instrs2, state)))

    yield rule(Trace(Instrs, state),
               Instrs.contains(Instruction.ret(var))).then(
                   set_(Trace(Instrs, state).return_value()).to(state[var]))

    yield rewrite(Trace(Instrs, state)).to(
        Trace(Instrs2, state2),
        eq(Trace(Instrs, state).return_value()).to(
            Trace(Instrs2, state2).return_value()))


@ruleset
def State_ruleset(key: Var, value: Operand, relation: Map[Var, Operand],
                  state: State) -> Iterable:
    yield rewrite(State.empty()).to(State(Map[Var, Operand].empty()))

    yield rewrite(State(relation)[key]).to(relation[key],
                                           relation.contains(key))

    yield rule(State(relation).insert(Instruction(key, value))).then(
        union(State(relation).insert(Instruction(key, value))).with_(
            State(relation.insert(key, semantic_function(value, relation)))))

    yield rule(state.insert(Instruction(key, value))).then(
        set_(state.insert(Instruction(key, value)).contains(key)).to(Unit()))


@ruleset
def Integers_rules(x: i64, y: i64) -> Iterable:
    yield rewrite(Operand.integer(x) + Operand.integer(y)).to(
        Operand.integer(x + y))

    yield rewrite(Operand.integer(x) * Operand.integer(y)).to(
        Operand.integer(x * y))

    yield rewrite(Operand.integer(x) - Operand.integer(y)).to(
        Operand.integer(x - y))

    yield rewrite(Operand.integer(x) << Operand.integer(y)).to(
        Operand.integer(x << y))


@ruleset
def Boolean_rules(b: Bool, b1: Bool) -> Iterable:
    yield birewrite(Operand.boolean(b) | Operand.boolean(b1)).to(
        Operand.boolean(b1) | Operand.boolean(b))

    yield birewrite(Operand.boolean(b) & Operand.boolean(b1)).to(
        Operand.boolean(b1) & Operand.boolean(b))

    yield rewrite(Operand.boolean(b) | Operand.boolean(True)).to(
        Operand.boolean(True))

    yield rewrite(Operand.boolean(b) | Operand.boolean(Bool(False))).to(
        Operand.boolean(b))

    yield rewrite(Operand.boolean(b) & Operand.boolean(Bool(True))).to(
        Operand.boolean(b))

    yield rewrite(Operand.boolean(b) & Operand.boolean(Bool(False))).to(
        Operand.boolean(False))


@ruleset
def Evaluation_rules(state: State, Instrs: Vec[Instruction],
                     counter: i64) -> Iterable:

    yield rewrite(eval_instructions(Instrs, state, counter)).to(
        state,
        eq(Instrs.length() - 1).to(counter))

    yield rule(eval_instructions(Instrs, state, counter), (Instrs.length() - 1)
               > counter).then(
                   set_(eval_instructions(Instrs, state, counter)).to(
                       eval_instructions(Instrs, state.insert(Instrs[counter]),
                                         counter + 1)))


@ruleset
def Semantic_function_rules(relation: Map[Var, Operand], x: i64, b: Bool,
                            var: Var, O1: Operand, O2: Operand) -> Iterable:
    return [
        rewrite(semantic_function(Operand.integer(x),
                                  relation)).to(Operand.integer(x)),
        rewrite(semantic_function(Operand.boolean(b),
                                  relation)).to(Operand.boolean(b)),
        rewrite(semantic_function(Operand(var), relation)).to(relation[var]),
        rewrite(semantic_function(O1 + O2, relation)).to(
            semantic_function(O1, relation) + semantic_function(O2, relation)),
        rewrite(semantic_function(O1 - O2, relation)).to(
            semantic_function(O1, relation) - semantic_function(O2, relation)),
        rewrite(semantic_function(O1 * O2, relation)).to(
            semantic_function(O1, relation) * semantic_function(O2, relation)),
        rewrite(semantic_function(O1 << O2, relation)).
        to(semantic_function(O1, relation) << semantic_function(O2, relation)),
    ]


graph_ruleset = unstable_combine_rulesets(Semantic_function_rules,
                                          Evaluation_rules, Function_rules,
                                          Trace_ruleset, State_ruleset,
                                          Integers_rules, Boolean_rules)
