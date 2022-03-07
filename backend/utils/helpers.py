import itertools
import numpy as np
import pandas as pd


def get_connected_chunks(
    array: np.array,
    chunk_size: int = 25,
    hookups: int = 5,
) -> np.array:
    """
    Returns 2D array (n_chunks, chunk_size) with a part of linking elements
    among the chunks.

    :param array: 1D array of values needed to be splitted on chunks.
    :param chunk_size: The size of one single chunks while splitting.
    :param hookups: The number of values from one chunk to share with others.

    :return: 2D array of chunks.
    """
    chunk_size = min(chunk_size, array.shape[0])
    hookups = min(chunk_size, hookups)

    number_of_chunks = array.shape[0] // chunk_size
    chunks = np.array_split(array, number_of_chunks)

    proxies = sum(
        [
            np.random.choice(
                chunk, size=min(hookups, len(chunk)), replace=False
            ).tolist()
            for chunk in chunks
        ],
        [],
    )
    for idx1 in range(len(proxies)):
        index_search_from = min(idx1 + hookups, len(proxies) - 1)
        index_search_to = len(proxies)
        idx2 = np.random.randint(index_search_from, index_search_to)
        proxies[idx1], proxies[idx2] = proxies[idx2], proxies[idx1]

    proxies = np.array_split(proxies, number_of_chunks)

    result = [list(chk) + list(prx) for chk, prx in zip(chunks, proxies)]

    return result
