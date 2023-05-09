from typing import Set, Union

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
from scipy.sparse import dok_matrix

from project.graphUtils import get_graph
from project.cnfUtils import cfg_to_cnf

def cfpq_matrix(
    graph: Union[MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_states: Set = None,
    final_states: Set = None,
    start_symbol: Variable = Variable("S"),
):
    """Performs a context-free path querying in a graph by a context-free grammar using boolean matrices.

    Parameters
    ----------
    graph: MultiDiGraph | str
    cfg: CFG | str
    start_states: Set[int]
    final_states: Set[int]
    start_symbol: Variable

    Returns
    -------
    result: Set[Tuple]
        A set of pairs of nodes solving the reachability problem and corresponding to the
        conditions (starting and final nodes, starting symbol).
    """
    if isinstance(graph, str):
        graph = get_graph(graph)
    if isinstance(cfg, str):
        cfg = CFG.from_text(cfg)
    if start_states is None:
        start_states = graph.nodes
    if final_states is None:
        final_states = graph.nodes
    return {
        (i, j)
        for (i, var, j) in matrix_algorithm(graph, cfg)
        if i in start_states and j in final_states and var == start_symbol
    }


def matrix_algorithm(graph: MultiDiGraph, cfg: CFG):
    """Function based on the Matrix algorithm that solves the reachability problem between all pairs of nodes
         for a given graph and a given context-free grammar.

    Parameters
    ----------
    graph: MultiDiGraph
    cfg: CFG

    Returns
    -------
    result: Set[Tuple]
        A set of pairs of nodes solving the reachability problem between all pairs of nodes.
    """
    cfg = cfg_to_cnf(cfg)
    term_productions, non_term_productions, eps_productions = set(), set(), set()
    for prod in cfg.productions:
        if len(prod.body) == 1:
            term_productions.add(prod)
        elif len(prod.body) == 2:
            non_term_productions.add(prod)
        else:
            eps_productions.add(prod)
    n = graph.number_of_nodes()
    var_to_mtx = {}
    for var in cfg.variables:
        var_to_mtx[var] = dok_matrix((n, n), dtype=bool)
    for (u, v, label) in graph.edges(data="label"):
        for prod in term_productions:
            if label == prod.body[0].value:
                var_to_mtx[prod.head][u, v] = True
    for i in graph.nodes:
        for prod in eps_productions:
            var_to_mtx[prod.head][i, i] = True
    while True:
        changed = False
        for prod in non_term_productions:
            prev_nonzero = var_to_mtx[prod.head].count_nonzero()
            var_to_mtx[prod.head] += var_to_mtx[prod.body[0]] @ var_to_mtx[prod.body[1]]
            if not changed:
                changed = prev_nonzero != var_to_mtx[prod.head].count_nonzero()
        if not changed:
            break
    res = set()
    for (var, mtx) in var_to_mtx.items():
        for (i, j) in zip(*mtx.nonzero()):
            res.add((i, var, j))
    return res