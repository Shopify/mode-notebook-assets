from dataclasses import dataclass
from typing import List, Callable, Union

import numpy as np

from mode_notebook_assets.practical_dashboard_displays.helper_functions import functional_setattr

UNSPECIFIED_METRIC_CHECK_LABEL = 'Unspecified Metric Check'

COMBINED_METRIC_CHECK_LABEL = 'Combined Metric Check'

AMBIGUOUS_VALENCE_LABEL = 'Ambiguous'


@dataclass
class ValenceScore:
    """
    The ValenceScore is the output of a MetricCheck at a point in time.

    Goals of this class are:
    * Store valence_score and all the information we need to interpret it
    * Define logic for combining ValenceScores, which may have conflicting valences or priorities
    * Store combined ValenceScores to maintain a simple data interface without loss of information
    * Allow subclassing for common patterns of MetricCheck results. For example, an ActionabilityValenceScore
      might automatically populate valence_label with one of "Extraordinary", "Better than Normal", "Normal",
      "Worse than Normal", or "Potential Crisis".

    Initialization
    ----------
    valence_score: This is a **directional** actionability score computed by a MetricCheck.
    priority_score: ValenceScores will ignore lower priority results when combined.
    is_override: Should this check override checks regardless of priority?
    is_ambiguous: Do the highest-priority checks have conflicting valences?
    metric_check_label: What kind of check produced this result?
    valence_label: A one to three word human readable description of the valence and actionability level.
    valence_description: A longer description of the valence, e.g. "The metric increased suddenly".
    text_separator: How do you concatenate descriptions?
    child_metric_check_results: Track *original* (never combined) ValenceScores to avoid information loss.
    """
    valence_score: float
    valence_label: str
    valence_description: str
    priority_score: int = 3
    is_override: bool = False
    is_ambiguous: bool = False
    metric_check_label: str = UNSPECIFIED_METRIC_CHECK_LABEL
    text_separator: str = ' - '
    # todo: rename params
    child_metric_check_results: List[Union['ValenceScore', None]] = None

    # todo: rename files, tests, references

    # todo: repr
    def __post_init__(self):
        # tweak inputs
        self.child_metric_check_results = self.child_metric_check_results or []
        self.valence_score_magnitude = np.abs(self.valence_score)

        # validate inputs
        assert (self.priority_score >= 0), 'Priority score is invalid'

        for r in self.child_metric_check_results:
            assert (r.child_metric_check_results == []), 'Arbitrary nesting of ValenceScore is forbidden.'

    def __add__(self, other: 'ValenceScore'):
        """
        Combine together two ValenceScores.
        """

        def choose_result(func: Callable, attr_name: str, do_not_allow_ties=True) -> Union['ValenceScore', None]:
            """
            Choose self or other using func and key. Return None in the case of a disallowed tie.

            Parameters
            ----------
            func: max or min
            attr_name: attribute name
            do_not_allow_ties: by default, ties return None instead of func default behaviour

            Returns
            -------
            ValenceScore or None
            """
            _self_value = getattr(self, attr_name)
            _other_value = getattr(other, attr_name)
            if do_not_allow_ties and _self_value == _other_value:
                return None
            else:
                return func(self, other, key=lambda r: getattr(r, attr_name))

        # Choose the preferred record (if applicable) to simplify case logic and return statement
        _higher_override_result = choose_result(max, 'is_override')
        _higher_priority_result = choose_result(min, 'priority_score')
        _higher_valence_result = choose_result(max, 'valence_score_magnitude', do_not_allow_ties=False)

        # Pre-compute combined attributes (some may be ignored)
        _combined_child_metric_check_results = self.child_metric_check_results + other.child_metric_check_results
        _combined_valence_description = (
            self.text_separator.join(
                set(
                    self.valence_description.split(sep=self.text_separator)
                    + other.valence_description.split(sep=other.text_separator)
                )
            )
        )

        _combined_valence_score = max(self.valence_score, other.valence_score)
        _combined_priority_score = min(self.priority_score, other.priority_score)
        _combined_is_ambiguous = not(
                self.valence_score != other.valence_score
                and np.sign(self.valence_score) == np.sign(other.valence_score)
        )

        _combined_valence_label = (
            AMBIGUOUS_VALENCE_LABEL if _combined_is_ambiguous
            else _higher_valence_result.valence_label
        )

        if self.is_override and other.is_override:
            if not _higher_priority_result:
                return ValenceScore(
                    valence_score=max(self.valence_score, other.valence_score),
                    priority_score=min(self.priority_score, other.priority_score),
                    is_override=True,
                    is_ambiguous=True,
                    metric_check_label=COMBINED_METRIC_CHECK_LABEL,
                    valence_label=AMBIGUOUS_VALENCE_LABEL,
                    valence_description=_combined_valence_description,
                    child_metric_check_results=_combined_child_metric_check_results,
                )
            else:
                return functional_setattr(
                    _higher_priority_result,
                    'child_metric_check_results',
                    _combined_child_metric_check_results
                )
        elif _higher_override_result:
            return functional_setattr(
                _higher_override_result,
                'child_metric_check_results',
                _combined_child_metric_check_results
            )
        elif _higher_priority_result:
            return functional_setattr(
                _higher_priority_result,
                'child_metric_check_results',
                _combined_child_metric_check_results
            )
        else:
            return ValenceScore(
                valence_score=_combined_valence_score,
                priority_score=_combined_priority_score,
                is_ambiguous=_combined_is_ambiguous,
                metric_check_label=COMBINED_METRIC_CHECK_LABEL,
                valence_label=_combined_valence_label,
                valence_description=_combined_valence_description
            )
