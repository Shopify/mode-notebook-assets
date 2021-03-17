import base64
from io import BytesIO

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from plotly import express as px


def map_actionability_score_to_color(x: float, is_valence_ambiguous=False, is_higher_good=True, is_lower_good=False,
                                     good_palette=None, bad_palette=None, ambiguous_palette=None, neutral_color=None):
    _good_palette = list(good_palette or px.colors.sequential.Greens[3:-2])
    _bad_palette = list(bad_palette or px.colors.sequential.Reds[3:-2])
    _ambiguous_palette = list(ambiguous_palette or ['rgb(255,174,66)'])
    _neutral_color = neutral_color or 'rgb(211,211,211)'

    if pd.isnull(x):
        return _ambiguous_palette[-1]

    if x == 0:
        return _neutral_color
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


def sparkline(data, point_marker='.', point_size=6, point_alpha=1.0, figsize=(4, 0.25), **kwargs):
    """
    Create a single HTML image tag containing a base64 encoded
    sparkline style plot.

    Forked from https://github.com/crdietrich/sparklines on 2020-12-22.
    """

    data = list(data)

    fig = plt.figure(figsize=figsize)  # set figure size to be small
    ax = fig.add_subplot(111)
    plot_len = len(data)
    point_x = plot_len - 1

    plt.plot(data, linewidth=2, color='gray', **kwargs)

    # turn off all axis annotations
    ax.axis('off')

    # plot the right-most point larger
    plt.plot(point_x, data[point_x], color='gray',
             marker=point_marker, markeredgecolor='gray',
             markersize=point_size,
             alpha=point_alpha, clip_on=False)

    # squeeze axis to the edges of the figure
    fig.subplots_adjust(left=0)
    fig.subplots_adjust(right=0.99)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    # save the figure to html
    bio = BytesIO()
    plt.savefig(bio)
    plt.close()
    html = """<img style="width=100%%;height=auto" src="data:image/png;base64,%s"/>""" % base64.b64encode(bio.getvalue()).decode('utf-8')
    return html


def dot(color='gray', figsize=(.5, .5), title_text=None, **kwargs):

    fig = plt.figure(figsize=figsize)  # set figure size to be small
    ax = fig.add_subplot(111)

    ax.add_artist(plt.Circle((.5, .5), .25, color=color))

    # turn off all axis annotations
    ax.axis('off')

    # save the figure to html
    bio = BytesIO()
    plt.savefig(bio, dpi=300)
    plt.close()
    html = f"""<img title="{'Hover text unavailable.' if title_text is None else title_text}" style="height:40px;width:40px;" src="data:image/png;base64,{base64.b64encode(bio.getvalue()).decode('utf-8')}"/>"""
    return html