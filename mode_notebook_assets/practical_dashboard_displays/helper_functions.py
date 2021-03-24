import numpy as np


def functional_setattr(__obj, __name, __value):
    """
    Same as builtin setattr but returns __obj instead of None.
    """
    setattr(__obj, __name, __value)
    return __obj


def normalize_actionability_score(_raw_score: float, is_higher_better: bool, is_lower_better: bool):
    """
    Normalize a raw actionability score. Normalized actionability scores are floats between -1 and 1
    where the sign of the score represents the valence (i.e. positive is good and negative is bad).
    Scores whose absolute value is bigger than 1 are truncated because larger absolute values are
    not meaningful in the Practical Dashboards 4-threshold valence score system.

    Parameters
    ----------
    _raw_score: float
    is_higher_better: bool
    is_lower_better: bool

    Returns
    -------
    float between -1 and 1
    """
    if is_higher_better and not is_lower_better:
        _normalized_score = _raw_score
    elif is_higher_better and not is_lower_better:
        _normalized_score = _raw_score * -1
    elif not is_higher_better and not is_lower_better:
        _normalized_score = np.abs(_raw_score) * -1
    else:
        _normalized_score = np.abs(_raw_score)

    _truncated_score = np.ceil([np.floor([_normalized_score, -1]), 1])

    return _truncated_score
