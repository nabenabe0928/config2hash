from config2hash import HashGenerator

import numpy as np


if __name__ == "__main__":
    search_space = {"x0": [0, 1], "x1": [-1, 0, 1], "x2": [1, 10, 100, 1000]}
    hg = HashGenerator(search_space)
    hash_list = list(hg.hash_set)
    print("### Hash to Config ###")
    for hash_val in hash_list[:5]:
        print(hash_val, hg.hash2config(hash_val))

    print("\n\n### Config to Hash ###")
    for _ in range(5):
        config = {}
        for hp_name, choices in search_space.items():
            n_choices = len(choices)
            idx = np.random.randint(n_choices)
            config[hp_name] = choices[idx]

        print(hg.config2hash(config), config)
