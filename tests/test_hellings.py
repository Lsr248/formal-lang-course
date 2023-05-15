from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.hellings import reachability_problem, hellings


def check_cfpq(algo_res, cfpq_res):
    expected_hellings = {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (2, Variable("B"), 3),
        (3, Variable("B"), 2),
        (1, Variable("S"), 3),
        (1, Variable("Q"), 2),
        (0, Variable("S"), 2),
        (0, Variable("Q"), 3),
        (2, Variable("S"), 3),
        (2, Variable("Q"), 2),
        (1, Variable("S"), 2),
        (1, Variable("Q"), 3),
        (0, Variable("S"), 3),
        (0, Variable("Q"), 2),
        (2, Variable("S"), 2),
        (2, Variable("Q"), 3),
    }
    expected_cfpq = {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)}
    assert algo_res == expected_hellings
    assert cfpq_res == expected_cfpq


def test_cfpq_hellings():
    text = """
        S -> A B
        S -> A Q
        Q -> S B
        A -> a
        B -> b
        """
    cfg = CFG.from_text(text)
    graph = MultiDiGraph()
    graph.add_nodes_from(range(0, 3))
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "a"}),
            (2, 0, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (3, 2, {"label": "b"}),
        ]
    )
    check_cfpq(
        algo_res=set(hellings(graph, cfg)),
        cfpq_res=reachability_problem(graph, cfg, start_var=Variable("S")),
    )
