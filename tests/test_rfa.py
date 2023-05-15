from pyformlang.regular_expression import Regex
from project.automats import dfa_by_regex
from project.ecfgUtils import *
from project.rfaUtils import *


def test_rsm_from_ecfg():
    text = """
        S -> A B C
        A -> i
        B -> r
        C -> (a | S)
        """
    ecfg = create_ecfg_from_text(text)
    rsm = rfa_from_ecfg(ecfg)
    expected_productions = {
        Variable("S"): Regex("A B C"),
        Variable("A"): Regex("i"),
        Variable("B"): Regex("r"),
        Variable("C"): Regex("(a | S)"),
    }
    assert rsm.start == Variable("S")
    assert all(
        rsm.boxes[var].is_equivalent_to(expected_productions[var].to_epsilon_nfa())
        for var in expected_productions.keys()
    )


def test_minimize_rsm():
    text = """
        S -> A B C
        A -> i
        B -> r
        C -> (a | S)
        """
    ecfg = create_ecfg_from_text(text)
    rsm = rfa_from_ecfg(ecfg)
    assert all(
        minimize(rsm).boxes[var] == dfa_by_regex(ecfg.productions[var])
        for var in ecfg.productions.keys()
    )
