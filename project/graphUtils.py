import cfpq_data as cf
from networkx import drawing, MultiDiGraph


def get_graph(name):
    graph = cf.graph_from_csv(cf.dataset.download(name))

    return graph


def get_graph_info(graph: MultiDiGraph):
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {i[2]["label"] for i in graph.edges.data(default=True)},
    )


def get_graph_info_by_name(name):
    graph = get_graph(name)
    return get_graph_info(graph)


def generate_labeled_two_cycles_graph(
    nodes_num,
    labels,
):

    return cf.labeled_two_cycles_graph(
        nodes_num[0],
        nodes_num[1],
        labels=labels,
    )


def write_graph(graph, path):
    drawing.nx_pydot.write_dot(graph, path)


def build_and_save_two_cycle_graph(first_cycle, second_cycle, labels, path):
    graph = generate_labeled_two_cycles_graph(first_cycle, second_cycle, labels)
    write_graph(graph, path)
    return graph
