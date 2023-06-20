from pyformlang.finite_automaton import State

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol

from project.regular_queries import *


def get_sample_fa():
    states = [State(0), State(1)]
    fa = NondeterministicFiniteAutomaton()
    fa.add_start_state(states[0])
    fa.add_final_state(states[1])
    fa.add_transitions(
        [
            (states[0], Symbol("a"), states[0]),
            (states[1], Symbol("b"), states[0]),
            (states[0], Symbol("a"), states[1]),
        ]
    )
    return fa


def get_sampel_fa_other():
    states = [State(0), State(1), State(2), State(3)]
    fa = NondeterministicFiniteAutomaton()
    fa.add_start_state(states[2])
    fa.add_start_state(states[3])
    fa.add_final_state(states[0])
    fa.add_final_state(states[1])
    fa.add_transitions(
        [
            (states[0], Symbol("a"), states[2]),
            (states[1], Symbol("a"), states[0]),
            (states[3], Symbol("a"), states[0]),
            (states[0], Symbol("b"), states[0]),
            (states[2], Symbol("b"), states[2]),
        ]
    )
    return fa


def test_intersect_with_empty():
    nfa = get_sample_fa()
    bm = BoolDecomposition(nfa)
    empty_bm = BoolDecomposition(NondeterministicFiniteAutomaton())

    intersection = BoolDecomposition.intersect_automata(bm, empty_bm)

    assert not intersection.start_states
    assert not intersection.final_states
    assert not intersection.state_to_index
    assert not intersection.bool_matrix
    assert intersection.all_states == 0


def test_intersect():
    l_nfa = get_sampel_fa_other()
    r_nfa = get_sample_fa()
    expected = l_nfa.get_intersection(r_nfa)

    l_bm = BoolDecomposition(l_nfa)
    r_bm = BoolDecomposition(r_nfa)

    actual = BoolDecomposition.intersect_automata(l_bm, r_bm)
    assert expected.final_states  == actual.final_states
