from pyformlang.finite_automaton import State
from project.graphUtils import *
from project.automats import *
from networkx import MultiDiGraph
from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import lil_matrix, kron
from typing import Set, Dict


class BoolDecomposition:
    """Class in which the nfa decomposes. The indexes of the start and final states, the Boolean adjacency
    matrix for each symbol, the mapping to each index state and the total number of states are stored.
    """

    start_states: Set[State]
    final_states: Set[State]
    bool_matrix: Dict
    state_to_index: Dict[State, int]
    all_states: int
    mtx_type_for_construction = lil_matrix

    def __init__(self, nfa: EpsilonNFA = None, mtx_type_for_construction=lil_matrix):
        if nfa is None:
            self.start_states = set()
            self.final_states = set()
            self.bool_matrix = {}
            self.state_to_index = {}
            self.index_to_state = {}
            self.all_states = 0
        else:
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.all_states = len(nfa.states)
            self.state_to_index = {
                state: index for (index, state) in enumerate(nfa.states)
            }
            self.index_to_state = {
                index: state for index, state in enumerate(nfa.states)
            }
            self.bool_matrix = self.create_bool_matrix_from_nfa(nfa)
        self.mtx_type_for_construction = mtx_type_for_construction

    def create_bool_matrix_from_nfa(self, nfa: EpsilonNFA):
        bool_matrix = {}
        for src_st, label_trg_st in nfa.to_dict().items():
            for label, trg_st in label_trg_st.items():
                if not isinstance(trg_st, set):
                    trg_st = {trg_st}
                for st in trg_st:
                    if label not in bool_matrix:
                        bool_matrix[label] = self.mtx_type_for_construction(
                            (self.all_states, self.all_states), dtype=bool
                        )
                    f = self.state_to_index.get(src_st)
                    s = self.state_to_index.get(st)
                    bool_matrix[label][f, s] = True
        return bool_matrix

    def intersect_automata(
        self, second_automaton: "BoolDecomposition"
    ) -> "BoolDecomposition":
        """Gets the intersection of self automaton with the second one.

        Parameters
        ----------
        second_automaton : BoolDecomposition
            Decomposed second automaton for intersection.

        Returns
        -------
        bool_decomposition : BoolDecomposition
            The decomposed automaton resulting from the intersection of automata.
        """
        bool_decomposition = BoolDecomposition()
        labels = self.bool_matrix.keys() & second_automaton.bool_matrix.keys()
        for label in labels:
            bool_decomposition.bool_matrix[label] = kron(
                self.bool_matrix[label], second_automaton.bool_matrix[label]
            )
        for (f_st, f_idx) in self.state_to_index.items():
            for (s_st, s_idx) in second_automaton.state_to_index.items():
                new_state_idx = f_idx * second_automaton.all_states + s_idx
                bool_decomposition.state_to_index[State(new_state_idx)] = new_state_idx
                if f_st in self.start_states and s_st in second_automaton.start_states:
                    bool_decomposition.start_states.add(new_state_idx)
                if f_st in self.final_states and s_st in second_automaton.final_states:
                    bool_decomposition.final_states.add(new_state_idx)
        bool_decomposition.all_states = self.all_states * second_automaton.all_states
        return bool_decomposition

    def get_transitive_closure(self):
        transitive_closure = sum(self.bool_matrix.values())
        prev = None
        curr = transitive_closure.nnz
        while prev != curr:
            transitive_closure += transitive_closure @ transitive_closure
            prev = curr
            curr = transitive_closure.nnz
        return transitive_closure


def regular_path_querying(
    graph: MultiDiGraph,
    regex: Regex,
    start_states: Set[int] = None,
    final_states: Set[int] = None,
) -> Set:
    """Perform a regular query to the graph.

    Parameters
    ----------
    graph: MultiDiGraph
    regex: PythonRegex
    start_states: Set[int]
    final_states: Set[int]
    """
    graph_bool_decomposition = BoolDecomposition(
        nfa_by_graph(graph, start_states, final_states)
    )
    regex_bool_decomposition = BoolDecomposition(dfa_by_regex(regex))
    intersection = graph_bool_decomposition.intersect_automata(regex_bool_decomposition)
    transitive_closure = intersection.get_transitive_closure()
    result = set()
    s_st, f_st = transitive_closure.nonzero()
    for i, j in zip(s_st, f_st):
        if i in intersection.start_states and j in intersection.final_states:
            result.add(
                (
                    State(i // regex_bool_decomposition.all_states),
                    State(j // regex_bool_decomposition.all_states),
                )
            )
    return result


def regular_path_querying_for_interpreter(graph: EpsilonNFA) -> Set:
    graph_bool_decomposition = BoolDecomposition(graph)
    transitive_closure = graph_bool_decomposition.get_transitive_closure()
    result = set()
    s_st, f_st = transitive_closure.nonzero()
    for i, j in zip(s_st, f_st):
        if (
            i in graph_bool_decomposition.start_states
            and j in graph_bool_decomposition.final_states
        ):
            result.add(State(j))
    return result
