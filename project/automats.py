from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex

from project.graphUtils import *


def dfa_by_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Builds DFA by a regular expression.
    :param regex: Regular expression.
    :return: Minimal DFA built on given regular expression.
    """
    return regex.to_epsilon_nfa().minimize()


def nfa_by_graph(
    graph: MultiDiGraph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    """
    Builds NFA by a graph.
    :param graph: Graph to transform to NFA.
    :param start_states: Start states in NFA. If None, then every node in NFA is the starting.
    :param final_states: Final states in NFA. If None, then every node in NFA is the final.
    :return: NFA built on given graph.
    """

    nfa = NondeterministicFiniteAutomaton()

    nfa.add_transitions(get_edges_by_label(graph))
    all_nodes = set(graph)

    if not start_states:
        start_states = all_nodes
    if not final_states:
        final_states = all_nodes

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa
