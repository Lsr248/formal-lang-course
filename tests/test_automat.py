import pytest
import pyformlang.regular_expression as re
import pyformlang.finite_automaton as fa
import networkx as nx
import cfpq_data as cd

from project.automats import *


def test_regex_to_dfa():
    dfa = dfa_by_regex(re.Regex("a|b|c"))
    assert dfa.accepts([fa.Symbol("a")])
    assert dfa.accepts([fa.Symbol("c")])
    assert not dfa.accepts([fa.Symbol("42")])
    assert dfa.is_deterministic()



def test_graph_to_nfa():
    graph = cd.labeled_two_cycles_graph(5, 5, labels=("A", "B"))
    actual_nfa = nfa_by_graph(graph, {0}, {3, 2})

    expected = fa.NondeterministicFiniteAutomaton()
    expected.add_start_state(fa.State(0))
    expected.add_final_state(fa.State(3))
    expected.add_final_state(fa.State(2))
    for fr, to, label in graph.edges(data="label"):
        expected.add_transition(fa.State(fr), fa.Symbol(label), fa.State(to))

    assert actual_nfa.is_equivalent_to(expected)


def test_empty_graph_to_nfa():
    nfa = nfa_by_graph(nx.MultiDiGraph())
    assert nfa.is_empty()