import cfpq_data as cf
from networkx import drawing, MultiDiGraph
from collections import namedtuple


GraphInfo = namedtuple("GraphInfo", "nodes_num edges_num labels")


def get_graph(name):
    """
    Returns graph with a given name.
    :param name: Name of graph to find.
    :return: Existing graph with a given name from CFPQ_Data Dataset.
    """
    graph = cf.graph_from_csv(cf.dataset.download(name))

    return graph


def get_graph_info(graph: MultiDiGraph):
    """
    Returns basic info of a graph with a given name from CFPQ_Data Dataset.
    :param graph: graph to find
    :return: Namedtuple of number of nodes, number of edges, set of edges' labels.
    """
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {i[2]["label"] for i in graph.edges.data(default=True)},
    )


def get_graph_info_by_name(name):
    """
    Shows basic info of a graph with a given name from CFPQ_Data Dataset.
    :param name: Name of graph to find.
    :return: Namedtuple of number of nodes, number of edges, set of edges' labels.
    """
    graph = get_graph(name)
    return get_graph_info(graph)


def generate_labeled_two_cycles_graph(
    nodes_num,
    labels,
):
    """
    Returns a graph with two cycles with labeled edges.
    :param nodes_num: Numbers of nodes in two cycles.
    :param labels: Labels for edges in two cycles.
    :return: A graph with two cycles connected by one node.
    """

    return cf.labeled_two_cycles_graph(
        nodes_num[0],
        nodes_num[1],
        labels=labels,
    )


def write_graph(graph, path):
    """
    Writes the given graph into the file.
    :param graph: Graph to export.
    :param path: Path to dot file.
    """
    drawing.nx_pydot.write_dot(graph, path)


def build_and_save_two_cycle_graph(first_cycle, second_cycle, labels, path):
    """
    Builds and saves the created graph into the specified DOT file.
    :param first_cycle: Numbers of nodes in first cycle.
    :param second_cycle: Numbers of nodes in second cycle.
    :param labels: Labels for edges in two cycles.
    :param path: Path to dot file.
    :return: graph
    """
    graph = generate_labeled_two_cycles_graph((first_cycle, second_cycle), labels)
    write_graph(graph, path)
    return graph


def get_edges_by_label(graph: MultiDiGraph):
    """
    Returns a set of labeled edges.
    :param graph: Graph with labeled edges.
    :return: A set of triplets (node_from, label, node_to) describing all the unique edges of the graph.
    """
    return set(
        map(
            lambda edge: (edge[0], edge[2]["label"], edge[1])
            if "label" in edge[2].keys()
            else None,
            graph.edges.data(default=True),
        )
    )
