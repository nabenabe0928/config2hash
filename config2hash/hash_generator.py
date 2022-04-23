from typing import Any, Dict, List


class HashGenerator:
    """
    The class exclusively for converting a config to an integer
    given a search space.
    Args:
        search_space (Dict[str, List[Any]]):
            A search space that we are interested in.
            e.g.
            ```python
            search_space = "sphere": {
                "x0": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
                "x1": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
            }
            ```
    """

    def __init__(self, search_space: Dict[str, List[Any]]):
        """
        Attributes:
            hp_to_index (Dict[str, Dict[str, int]]):
                The mapping from a choice to an index in each dimension.
            base_list (List[int]):
                The base numbers used to generate a hash value for each config.
            n_max_choices (int):
                The maximum number of choices in search space.
        """
        n_choices = [len(choices) for choices in search_space.values()]
        self._n_max_choices = max(n_choices)
        self._hp_to_index = {
            hp_name: {c: idx for idx, c in enumerate(choices)} for hp_name, choices in search_space.items()
        }
        self._search_space = search_space
        dim = len(search_space)
        self._base_list = [self._n_max_choices**d for d in range(dim)]

    def config2hash(self, config: Dict[str, Any]) -> int:
        """
        A method that maps from config to a hash value.

        Args:
            config (Dict[str, ParamType]):
                A configuration of the objective function.

        Returns:
            hash_val (int):
                A hash value of the given config.
        """
        hash_val = 0
        for dim, (hp_name, map2index) in enumerate(self._hp_to_index.items()):
            idx = map2index[config[hp_name]]
            base = self._base_list[dim]
            hash_val += base * idx
        return hash_val

    def hash2config(self, hash_val: int) -> Dict[str, Any]:
        """
        A method that maps a hash value to config.

        Args:
            hash_val (int):
                A hash value of the given config.

        Returns:
            config (Dict[str, ParamType]):
                A configuration of the objective function.
        """
        config = {}
        for dim, (hp_name, choices) in enumerate(self._search_space.items()):
            idx = hash_val % self._n_max_choices
            config[hp_name] = choices[idx]
            hash_val //= self._n_max_choices

        return config
