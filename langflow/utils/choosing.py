import numpy as np
import pandas as pd
from typing import Tuple


def generate_phrase_pair(pairs: pd.DataFrame) -> Tuple[str, str]:
    """
    Choose pair of phrases randomly
    """
    f, s = pairs[np.random.choice(len(pairs))]
    return f.lower().capitalize(), s.lower().capitalize()
