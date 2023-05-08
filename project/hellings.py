from typing import Set, Union

from networkx import MultiDiGraph, Graph, nx_pydot
from pyformlang.cfg import CFG, Variable
from project.cnfUtils import cfg_to_cnf


def reachability_problem(
    graph: Graph,
    query: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_var: Variable = "S",
) -> set:
    """Performs a context-free path querying in a graph by a context-free grammar.

    Parameters
    ----------
    graph: Graph
    query: CFG
    start_nodes: Set|None
    final_nodes: Set|None
    start_var: Variable |"S"

    Returns
    -------
    result: Set
        A set of pairs of nodes solving the reachability problem and corresponding to the
        conditions (starting and final nodes, starting symbol).
    """
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    if start_var is None:
        start_var = query.start_symbol

    ctc = hellings(graph, query)

    return {
        (start, final)
        for start, var, final in ctc
        if start in start_nodes and var == start_var and final in final_nodes
    }


def hellings(graph: Graph, cfg: CFG) -> list:
    """Function based on the Hellings algorithm that solves the reachability problem between all pairs of nodes
     for a given graph and a given context-free grammar.

    Parameters
    ----------
    graph: Graph
    cfg: CFG

    Returns
    -------
    result: List
        A list of pairs of nodes solving the reachability problem between all pairs of nodes.
    """

    cfg = cfg_to_cnf(cfg)
    term_productions, non_term_productions, eps_productions = set(), set(), set()
    for prod in cfg.productions:
        match len(prod.body):
            case 0:
                eps_productions.add(prod)
            case 1:
                term_productions.add(prod)
            case 2:
                non_term_productions.add(prod)

    result = []
    for (u, v, label) in graph.edges(data="label"):
        for prod in term_productions:
            if label == prod.body[0].value:
                result.append((u, prod.head, v))
    for n in graph.nodes:
        for prod in eps_productions:
            result.append((n, prod.head, n))
    m = result.copy()
    while m:
        (v, N, u) = m.pop(0)
        for (x, M, y) in result:
            if y == v:
                for prod in non_term_productions:
                    new_triple = (x, prod.head, u)
                    if (
                        prod.body[0] == M
                        and prod.body[1] == N
                        and new_triple not in result
                    ):
                        m.append(new_triple)
                        result.append(new_triple)
        for (x, M, y) in result:
            if x == u:
                for prod in non_term_productions:
                    new_triple = (v, prod.head, y)
                    if (
                        prod.body[0] == N
                        and prod.body[1] == M
                        and new_triple not in result
                    ):
                        m.append(new_triple)
                        result.append(new_triple)
    return result


def hellings(graphPath, cfgGile) -> list:
    """Function based on the Hellings algorithm that solves the reachability problem between all pairs of nodes
     for a given graph and a given context-free grammar.

    Parameters
    ----------
    graphPath: The path to file that contains graph in .dot format
    cfgGile: File that contains CFG

    Returns
    -------
    result: List
        A list of pairs of nodes solving the reachability problem between all pairs of nodes.
    """

    with open(cfgGile) as f:
        cfg = CFG.from_text(f.read())

    return hellings(nx_pydot.read_dot(graphPath), cfg)
