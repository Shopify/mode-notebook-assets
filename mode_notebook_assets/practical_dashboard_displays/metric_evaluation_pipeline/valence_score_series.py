import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore


class ValenceScoreSeries:
    """
    A ValenceScoreSeries stores ValenceScores for every point in a time series.
    It can be created as the result of applying a MetricCheck to a time series.
    A ValenceScoreSeries can be combined with other ValenceScoreSeries objects,
    for example to combine the results of two MetricChecks.

    A ValenceScoreSeries can also be created as the result of applying a
    MetricEvaluationPipeline to data. In this case it is the combined result
    of all of the MetricChecks used by the MetricEvaluationPipeline.

    The ValenceScoreSeries class can only be initialized with a Pandas Series of
    ValenceScore objects, and can only be combined with another ValenceScoreSeries
    with an identical index.
    """

    def __init__(self, s: pd.Series):
        """
        Initializes the ValenceScoreSeries. The initialization
        series is only used to copy the input to self._score_series.

        Parameters
        ----------
        s: pd.Series of ValenceScore objects
        """

        for obj in s:
            assert isinstance(obj, ValenceScore), \
                'ValenceScoreSeries can only be initialized with a Pandas Series of ValenceScore objects'

        self._score_series = s.copy()

    def __add__(self, other: 'ValenceScoreSeries') -> 'ValenceScoreSeries':
        """
        Combines two ValenceScoreSeries. This method has a strong assertion
        that the two ValenceScoreSeries combined have the same index. This
        prevents potentially invalid results.

        Parameters
        ----------
        other: ValenceScoreSeries

        Returns
        -------
        ValenceScoreSeries
        """
        assert self._score_series.index == other._score_series.index
        return self._score_series + other._score_series

    def __repr__(self) -> str:
        """
        Defines the REPL representation of the ValenceScoreSeries.

        Returns
        -------
        str
        """
        return f'ValenceScoreSeries with {self._score_series.len()} periods.' \
               f'The more recent period index is {self._score_series.index[-1]}.' \
               f'The most recent ValenceScore is {self.last_record().valence_label}' \
               f'from {self.last_record().metric_check_label}.'

    def last_record(self) -> ValenceScore:
        """
        Returns the final ValenceScore in the series. This represents the current period
        for reporting.

        Returns
        -------
        ValenceScore
        """
        return self._score_series.tail(1)
