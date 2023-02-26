import os

import pytest
import networkx as nx
import cfpq_data as cd

from project.graphUtils import *

graph = cd.graph_from_csv(cd.download("skos"))


def check_graphs(actual_graph, expected_graph):
    act_info = get_graph_info(actual_graph)
    exp_info = get_graph_info(actual_graph)
    return (
        act_info[0] == exp_info[0]
        and act_info[1] == exp_info[1]
        and act_info[2] == exp_info[2]
    )


def test_load_graph():
    assert check_graphs(graph, get_graph("skos"))


def test_save_graph():
    write_graph(graph, "skos")
    assert "skos" in os.listdir(".")
    os.remove("skos")


def test_get_info():
    info = get_graph_info(graph)
    assert info[0] == graph.number_of_nodes()
    assert info[1] == graph.number_of_edges()


def test_build_two_cycle_graph():
    labels = ("fst", "snd")
    actual_graph = generate_labeled_two_cycles_graph((10, 12), labels)
    expected_graph = cd.labeled_two_cycles_graph(10, 12, labels=labels)
    assert check_graphs(actual_graph, expected_graph)
