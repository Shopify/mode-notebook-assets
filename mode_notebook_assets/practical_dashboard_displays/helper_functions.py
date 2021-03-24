import numpy as np


def functional_setattr(__obj, __name, __value):
    """
    Same as builtin setattr but returns __obj instead of None.
    """
    setattr(__obj, __name, __value)
    return __obj


def normalize_valence_score(_raw_score: float, is_higher_better: bool, is_lower_better: bool) -> float:
    """
    Normalize a raw valence score. Normalized valence scores are floats between -1 and 1
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

    _truncated_score = min(max(_normalized_score, -1), 1)

    return _truncated_score


def map_score_to_string(valence_score: float, labels: list = None) -> str:
    """
    Maps an valence score (float greater than or equal to -1
    and less than or equal to 1) to a label.

    Can also be used for mapping descriptions or adjectives.

    Parameters
    ----------
    valence_score: An valence score
    labels: A list of labels, length must equal 5

    Returns
    -------
    A label string
    """
    if labels is None:
        _labels = [
            'Unusually Bad',
            'Worse than Normal',
            'In a Normal Range',
            'Better than Normal',
            'Unusually Good',
        ]
    else:
        _labels = labels

    assert len(_labels) == 5, 'Mapping valence scores to labels requires 5 labels.'

    if valence_score <= -1:
        return _labels[0]
    elif valence_score < 0:
        return _labels[1]
    elif valence_score >= 1:
        return _labels[4]
    elif valence_score > 0:
        return _labels[3]
    else:
        return _labels[2]


def map_sign_to_string(x: float, labels: list = None):
    """
    Maps a sign to a string. If negative, first label;
    if zero, second label; if positive, third label.

    Parameters
    ----------
    x: A number
    labels: A list of labels, length must equal 3

    Returns
    -------
    A label string
    """
    if labels is None:
        _labels = [
            'Lower than',
            'Within the range of',
            'Higher than',
        ]
    else:
        _labels = labels

    assert len(_labels) == 3, 'Mapping signs to strings requires 3 labels.'

    if x < 0:
        return _labels[0]
    elif x > 0:
        return _labels[2]
    else:
        return _labels[1]
