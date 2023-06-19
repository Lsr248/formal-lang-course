from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfpqUtils import matrix_algorithm, cfpq_matrix
from test_hellings import check_cfpq


def test_cfpq_matrix():
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
        algo_res=matrix_algorithm(graph, cfg),
        cfpq_res=cfpq_matrix(graph, cfg, start_symbol=Variable("S")),
    )