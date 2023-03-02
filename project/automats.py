from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton, State
from pyformlang.regular_expression import Regex

from project.graphUtils import *



def dfa_by_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    return regex.to_epsilon_nfa().minimize()


def nfa_by_graph(
    graph: MultiDiGraph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:

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
