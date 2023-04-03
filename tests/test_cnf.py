from project.cnfUtils import *
import pytest

def test_wrong_file():
    path_not_exists = "tests/data/emp"
    path_not_txt = "tests/data/empty"

    with pytest.raises(OSError):
        cfg_from_file(path_not_exists)
    with pytest.raises(OSError):
        cfg_from_file(path_not_txt)

def test_empty_cfg():
    path_to_empty = "tests/data/empty.txt"
    cfg = cfg_from_file(path_to_empty)
    assert cfg.is_empty()
    assert cfg_to_cnf(cfg).is_empty()

def test_cfg():
    cfg = cfg_from_file("tests/data/cfg.txt")
    weak_cfg = cfg_to_cnf(cfg)
    words = ["", "b", "bb", "bbbbbbbbbbbbbbbbbbbbb"]
    for word in words:
        assert cfg.contains(word)
        assert weak_cfg.contains(word)
    not_words = ["a", "ba", "b "]
    for word in not_words:
        assert not cfg.contains(word)
        assert not weak_cfg.contains(word)