def map_actionability_score_to_color(x: float, is_valence_ambiguous=False, is_higher_good=True, is_lower_good=False,
                                     good_palette=None, bad_palette=None, ambiguous_palette=None):
    _good_palette = list(good_palette or px.colors.sequential.Greens[3:-2])
    _bad_palette = list(bad_palette or px.colors.sequential.Reds[3:-2])
    _ambiguous_palette = list(ambiguous_palette or ['rgb(255,174,66)'])

    if x == 0:
        return 'rgb(0,0,0)'
    elif is_valence_ambiguous:
        return _ambiguous_palette[
            int(min(np.floor(np.abs(x) * (len(_ambiguous_palette) - 1)), len(_ambiguous_palette) - 1))]
    else:
        _is_good = (is_higher_good and x > 0) or (is_lower_good and x < 0)
        if _is_good:
            return _good_palette[int(min(np.floor(np.abs(x) * (len(_good_palette) - 1)), len(_good_palette) - 1))]
        else:
            return _bad_palette[int(min(np.floor(np.abs(x) * (len(_bad_palette) - 1)), len(_bad_palette) - 1))]


def map_actionability_score_to_description(x: float, is_valence_ambiguous=False, is_higher_good=True,
                                           is_lower_good=False):
    if x == 0:
        return 'Within a Normal Range'
    elif is_valence_ambiguous:
        return 'Ambiguous'
    else:
        _is_good = (is_higher_good and x > 0) or (is_lower_good and x < 0)
        if _is_good:
            if np.abs(x) > 1:
                return 'Extraordinary'
            else:
                return 'Actionably Good'
        else:
            if np.abs(x) > 1:
                return 'Crisis'
            else:
                return 'Actionably Bad'


def map_threshold_labels_to_name_by_configuration(label: str, is_higher_good=True, is_lower_good=False):
    is_high = 'high' in label
    is_low = 'low' in label
    is_l1 = 'l1' in label
    is_l2 = 'l2' in label

    if is_high and is_l2:
        return 'Extraordinary' if is_higher_good else 'Crisis'
    elif is_high and is_l1:
        return 'Actionably Good' if is_higher_good else 'Actionably Bad'
    elif is_low and is_l1:
        return 'Actionably Good' if is_lower_good else 'Actionably Bad'
    elif is_low and is_l2:
        return 'Extraordinary' if is_lower_good else 'Crisis'
    else:
        return label