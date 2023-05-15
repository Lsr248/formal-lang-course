from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from project.graphUtils import *
from itertools import product
from scipy.sparse import kron, dok_array, csr_array, bmat
from pyformlang import finite_automaton as fa

BinaryMatrix = namedtuple("BinaryMatrix", "states matrix")
"""
Namedtuple specifying a binary matrix for some automaton.
"""

StateInfo = namedtuple("StateInfo", "value is_start is_final")


def intersect_nfa(
    nfa1: NondeterministicFiniteAutomaton, nfa2: NondeterministicFiniteAutomaton
) -> NondeterministicFiniteAutomaton:
    bm1 = bm_by_nfa(nfa1)
    bm2 = bm_by_nfa(nfa2)
    intersection = intersect(bm1, bm2)

    return nfa_by_bm(intersection)


def bm_by_nfa(nfa: NondeterministicFiniteAutomaton) -> BinaryMatrix:
    """
    Builds binary matrix by NFA.
    :param nfa: NFA to transform.
    :return: Binary matrix.
    """
    states = list(
        {
            StateInfo(st.value, st in nfa.start_states, st in nfa.final_states)
            for st in nfa.states
        }
    )

    transitions = nfa.to_dict()
    matrix = {}
    for n_from in transitions:
        for symbol, ns_to in transitions[n_from].items():
            tmp = matrix.setdefault(
                symbol.value, dok_array((len(states), len(states)), dtype=bool)
            )
            start_index = next(i for i, s in enumerate(states) if s.value == n_from)
            for n_to in ns_to if isinstance(ns_to, set) else {ns_to}:
                end_index = next(i for i, s in enumerate(states) if s.value == n_to)
                tmp[start_index, end_index] = True

    for key in matrix:
        matrix[key] = matrix[key].tocsr()

    return BinaryMatrix(states, matrix)


def nfa_by_bm(bm: BinaryMatrix) -> NondeterministicFiniteAutomaton:
    """
    Builds NFA by binary matrix.
    :param bm: Binary matrix to transform.
    :return: NFA.
    """
    nfa = NondeterministicFiniteAutomaton()

    for label in bm.matrix.keys():
        arr = bm.matrix[label].toarray()
        for i in range(len(arr)):
            for j in range(len(arr)):
                if arr[i][j]:
                    nfa.add_transition(
                        State(bm.states[i].value),
                        label,
                        State(bm.states[j].value),
                    )

    for st in bm.states:
        if st.is_start:
            nfa.add_start_state(State(st.value))
        if st.is_final:
            nfa.add_final_state(State(st.value))

    return nfa


def intersect(bm_l: BinaryMatrix, bm_r: BinaryMatrix) -> BinaryMatrix:
    """
    Computes intersection of two binary matrices.
    :param bm_l: Left-hand side binary matrix.
    :param bm_r: Right-hand side binary matrix.
    :return: Intersection of two binary matrices.
    """
    states = [
        StateInfo(
            (st1.value, st2.value),
            st1.is_start and st2.is_start,
            st1.is_final and st2.is_final,
        )
        for st1, st2 in product(bm_l.states, bm_r.states)
    ]

    matrix = {}
    n = len(states)
    for symbol in set(bm_l.matrix.keys()).union(set(bm_r.matrix.keys())):
        if symbol in bm_l.matrix and symbol in bm_r.matrix:
            matrix[symbol] = csr_array(
                kron(bm_l.matrix[symbol], bm_r.matrix[symbol], format="csr")
            )
        else:
            matrix[symbol] = csr_array((n, n), dtype=bool)

    return BinaryMatrix(states, matrix)
