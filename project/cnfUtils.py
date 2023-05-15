from pyformlang.cfg import CFG


def cfg_from_file(path: str) -> CFG:
    with open(path, "r") as f:
        text = f.read()
    return CFG.from_text(text)
    # content = "".join(line for line in f)
    # return CFG.from_text(content)


def cfg_to_cnf(cfg: CFG) -> CFG:
    wcnf = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    epsilon_productions = wcnf._get_productions_with_only_single_terminals()
    epsilon_productions = wcnf._decompose_productions(epsilon_productions)

    return CFG(start_symbol=wcnf.start_symbol, productions=set(epsilon_productions))
