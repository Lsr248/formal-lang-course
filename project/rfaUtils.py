from typing import Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from project.ecfgUtils import ECFG
from scipy.sparse import dok_matrix
import numpy

class RFA:
    """
    Class for representing Recursive finite automaton.
    """

    def __init__(self, start: Variable, boxes: Dict[Variable, DeterministicFiniteAutomaton]):
        self.start = start
        self.boxes = boxes


def rfa_from_ecfg(ecfg: ECFG):
    """Create a RFA from the Extended Context-Free Grammar.
    Parameters
    ----------
    ecfg: ECFG
        Extended Context-Free Grammar.
    Returns
    -------
    RFA: RFA
        The equivalent recursive state machine.
    """
    boxes = {}
    for k, v in ecfg.productions.items():
        boxes[k] = v.to_epsilon_nfa().minimize()
    return RFA(start=ecfg.start, boxes=boxes)

def toAdjacencyMatrix(self):
    """
    Convert recursive finite automaton to a adjacency matrix.
    """
    states = set()
    for var, dfa in self.dfas.items():
        for x in dfa.states:
            states.add((var, x))
    state_idx = {k: i for i, k in enumerate(states)}
    result = {}
    for var, dfa in self.dfas.items():
        for fro, symb, to in dfa:
            mat = result.setdefault(
                symb, dok_matrix((len(state_idx), len(state_idx)), dtypeb= numpy.bool_)
            )
            mat[state_idx[(var, fro)], state_idx[(var, to)]] = True
    return result, state_idx


def minimize(rfa:RFA):
    """Minimize the current Recursive finite automaton.
    Returns
    RFA: RFA
        The minimal RFA.
    """
    # for box in self.boxes :
    #     box.dfa = box.dfa.minimize()
    # return self
    res = RFA(start=rfa.start, boxes={})
    for v, nfa in rfa.boxes.items():
        res.boxes[v] = nfa.minimize()
    return res
