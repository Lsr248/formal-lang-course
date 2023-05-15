from typing import Dict, AbstractSet

from pyformlang.cfg import Variable, CFG, Terminal
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable],
        productions: Dict[Variable, Regex],
        start: Variable = Variable("S"),
    ):
        self.variables = variables
        self.start = start
        self.productions = productions


def create_ecfg_from_cfg(cfg: CFG):
    """Create an extended context-free grammar from the context-free grammar.
    Parameters
    ----------
    cfg: CFG
        Context-Free Grammar.
    Returns
    -------
    ecfg: ECFG
        The Extended context-free grammar.
    """
    productions = {}
    for _, prod in enumerate(cfg.productions):
        regex = Regex(
            " ".join([x.to_text() for x in prod.body] if len(prod.body) > 0 else "$")
        )
        productions[prod.head] = (
            productions[prod.head].union(regex) if prod.head in productions else regex
        )
    return ECFG(cfg.variables, productions, cfg.start_symbol)


def create_ecfg_from_text(text: str):
    """
    Create extended context-free grammar from a text.
    Parameters
    ----------
    text: str
        The text.
    Returns
    -------
    ecfg: ECFG
        The extended context-free grammar.
    """
    variables = set()
    terminals = set()
    productions = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        head_symbol, body_symbol = line.split("->")
        head = Variable(head_symbol.strip())
        variables.add(head)
        productions[head] = Regex(body_symbol)
    return ECFG(variables, productions)


def create_ecfg_from_file(file):
    """Read extended context-free grammar from a file.
    Parameters
    ----------
    file: name of file to read.
    Returns
    -------
    ecfg: ECFG
        The extended context-free grammar.
    """
    with open(file) as f:
        ecfg = create_ecfg_from_text(f.read())
    return ecfg
