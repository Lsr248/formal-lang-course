# from project.task2 import create_minimal_dfa_for_regex
from project.automats import dfa_by_regex
from project.cnfUtils import cfg_from_file
from project.ecfgUtils import *

expected = ECFG(
    variables={Variable("S"), Variable("A")},
    productions={Variable("S"): Regex("A"), Variable("A"): Regex("(((S.S)|$)|b)")},
)


def test_ecfg_from_cfg1():
    path = "tests/data/cfg.txt"
    cfg = cfg_from_file(path)
    actual = create_ecfg_from_cfg(cfg)
    assert actual.variables == expected.variables
    assert actual.start == expected.start
    assert all(
        dfa_by_regex(actual.productions[var]).is_equivalent_to(
            dfa_by_regex(expected.productions[var])
        )
        for var in expected.productions.keys()
    )


def test_ecfg1_from_text():
    text = """
        S -> A
        A -> (b | $ | S S)
        """
    actual = create_ecfg_from_text(text)
    assert actual.variables == expected.variables
    assert actual.start == expected.start
    assert all(
        dfa_by_regex(actual.productions[var]).is_equivalent_to(
            dfa_by_regex(expected.productions[var])
        )
        for var in expected.productions.keys()
    )
