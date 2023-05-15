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
    bm = bm_by_nfa(nfa)
    empty_bm = bm_by_nfa(NondeterministicFiniteAutomaton())

    intersection = nfa_by_bm(intersect(bm, empty_bm))

    assert intersection.is_empty()


def test_intersect():
    l_nfa = get_sampel_fa_other()
    r_nfa = get_sample_fa()
    expected = l_nfa.get_intersection(r_nfa)

    l_bm = bm_by_nfa(l_nfa)
    r_bm = bm_by_nfa(r_nfa)

    actual = nfa_by_bm(intersect(l_bm, r_bm))
    assert expected.is_equivalent_to(actual)
