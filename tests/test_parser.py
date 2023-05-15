import filecmp
import os

import pytest

from project.gql.parser import *


@pytest.mark.parametrize(
    "inp, data",
    [
        ("x = 5; /*comment*/", True),
        ("/*comment*/ x = 5;", True),
        ("x /*comment*/ = 5;", True),
        ("x = 5 ; /*comment", False),
        ("x = 5; //comment", False),
        ("x = 5; /*комментарий*/", True),
    ],
)
def test_comment(inp, data):
    assert accept(inp) == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("(expr)*", True),
        ("(union (expr1, expr2))*", True),
        ("(expr1, expr2)*", False),
        ("()*", False),
    ],
)
def test_star(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("union (expr1, expr2)", True),
        ('union (union ("a", 1), "A")', True),
        ("union (expr)", False),
        ("union (expr1, expr2, expr3)", False),
    ],
)
def test_union(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("concat (expr1, expr2)", True),
        ('concat (concat ("a", 1), "A")', True),
        ("concat (expr)", False),
        ("concat (expr1, expr2, expr3)", False),
    ],
)
def test_concat(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("intersect (expr1, expr2)", True),
        ('intersect (intersect ("a", 1), "A")', True),
        ("intersect (expr)", False),
        ("intersect (expr1, expr2, expr3)", False),
    ],
)
def test_intersect(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("filter (fun (var) {1}, expr)", True),
        ("filter (fun () {}, expr )", False),
        ("filter (fun (var) {1})", False),
        ("filter (fun (var) {1}, expr1, expr2", False),
    ],
)
def test_filter(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("map (fun (var) {1}, expr)", True),
        ("map (fun () {}, expr )", False),
        ("map (fun (var) {1})", False),
    ],
)
def test_map(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("get_edges (var)", True),
        ("get_edges (.not_var)", False),
        ("get_edges var", False),
        ("get_edges (var", False),
        ('{(0, "label1", 1), (1, "label2", 2)}', True),
        ("{(111)}", False),
        ("set()", True),
    ],
)
def test_edges(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("get_labels (var)", True),
        ("get_labels (.not_var)", False),
        ("get_labels var", False),
        ("get_labels (var", False),
        ('{"label1", "label2"}', True),
        ("{lab1}", True),
        ("{true}", False),
        ("set()", True),
    ],
)
def test_labels(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("get_start (var)", True),
        ("get_start (.not_var)", False),
        ("get_start var", False),
        ("get_start (var", False),
        ("get_final (graph)", True),
        ("get_reachable (graph)", True),
        ("get_vertices (graph)", True),
        ('{(0, "label", 1)}', True),
        ('{(0, "label", "ss")}', False),
        ("set()", True),
    ],
)
def test_vertices(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("0", True),
        ("1234567890", True),
        ("(1)", True),
        ("-1", True),
        ('"string"', True),
        ("true", True),
        ("(l", False),
        ("truer", False),
        ("0111", False),
    ],
)
def test_value(inp, data):
    assert accept("x = " + inp + ";") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("i_am_variable", True),
        ("_me_too", True),
        ("iAmVariable1234", True),
        ("p/a/t/h.dot", True),
        ("111", False),
        ("/ccc", False),
    ],
)
def test_variable(inp, data):
    assert accept(inp + "= 1; ") == data


@pytest.mark.parametrize(
    "inp, data",
    [
        ("print expr;", True),
        ("print (expr);", True),
        ("print expr", False),
        ("print .not_expr;", False),
    ],
)
def test_print(inp, data):
    assert accept(inp) == data


@pytest.mark.parametrize(
    "inp, data",
    [
        (
            """
        graph = load_graph("p/a/t/h");
        vertices = get_final(graph);
        graph_upd = set_start(get_vertices(graph), graph);
        print vertices;
        print get_labels(graph_upd);
        """,
            True,
        ),
        (
            """
        graph = load_graph("p/a/t/h/2");
        edges = get_edges(graph);
        graph_upd = set_final(get_start(graph), graph);
        print get_final(graph_upd);
        print edges;
        """,
            True,
        ),
        (
            """
        a = union ("A", "a");
        b_a = (union ("b", a))*;
        print concat (a, b_a);
        """,
            True,
        ),
    ],
)
def test_prog(inp, data):
    assert accept(inp) == data


def test1_write_dot():
    text = """a = 5;"""
    save_as_dot(text, "tests/data/temp1_task14.dot")
    assert filecmp.cmp(
        "tests/data/temp1_task14.dot", "tests/data/expected1_task14.dot", shallow=False
    )
    os.remove("tests/data/temp1_task14.dot")


def test2_write_dot():
    text = """
        a = union ("A", "a");
        b_a = (union ("b", a))*;
        print concat (a, b_a);
        """
    save_as_dot(text, "tests/data/temp2_task14.dot")
    assert filecmp.cmp(
        "tests/data/temp2_task14.dot", "tests/data/expected2_task14.dot", shallow=False
    )
    os.remove("tests/data/temp2_task14.dot")
