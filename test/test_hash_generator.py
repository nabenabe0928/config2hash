import itertools
import pytest
import unittest

from config2hash import HashGenerator


def test_error():
    search_space = {"x0": [0, 1], "x1": [0, 1, 2], "x2": [0, 1, 2, 3]}
    hg = HashGenerator(search_space)
    with pytest.raises(RuntimeError):
        for _ in range(60):
            hg.hash_set


def test_hash_generator():
    search_space = {"x0": [0, 1], "x1": [-1, 0, 1], "x2": [1, 10, 100, 1000]}
    hg = HashGenerator(search_space)
    hash_vals = []
    for vals in itertools.product(*[choices for choices in search_space.values()]):
        config = {hp_name: val for hp_name, val in zip(search_space.keys(), vals)}
        hash_val = hg.config2hash(config)
        hash_vals.append(hash_val)
        queried_config = hg.hash2config(hash_val)
        print(hash_val, config, queried_config)

        for key, val in config.items():
            assert queried_config[key] == val

    assert len(set(hash_vals)) == 2 * 3 * 4
    assert set(hash_vals) == hg.hash_set

    search_space["x2"] = [1, 10, 10, 1000]
    with pytest.raises(ValueError):
        hg = HashGenerator(search_space)


if __name__ == "__main__":
    unittest.main()
