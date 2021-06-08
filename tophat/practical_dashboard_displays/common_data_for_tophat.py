import datetime
from random import random

import pandas as pd


def get_segmented_metric_example_df():
    _category_1 = [f'1{char}' for char in 'ABC']
    _category_2 = [f'2{char}' for char in 'XYZ']
    _t = [datetime.datetime(2020, 1, 1) + datetime.timedelta(days=x) for x in range(0, 25)]
    rows = []
    for t in _t:
        for c1 in _category_1:
            for c2 in _category_2:
                rows.append({
                    'Day':        t,
                    'Category 1': c1,
                    'Category 2': c2,
                    'Revenue':    50 + hash(c1) % 10 + (hash(c2) % 2 * _t.index(t) / 4) + 10 * random(),
                })
    _df = pd.DataFrame.from_records(rows)
    return _df


INCREASING_SALES_TIME_SERIES = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv')\
    .set_index('Month')['Sales']\
    .round()

STABILIZING_SALES_TIME_SERIES = INCREASING_SALES_TIME_SERIES.copy()**-2 + 300

AMBIGUOUS_TIME_SERIES = INCREASING_SALES_TIME_SERIES.copy().update(
    pd.Series(
        [1300, 900],
        index=INCREASING_SALES_TIME_SERIES.index[-2:],
    )
)

SEGMENTED_REVENUE_DATAFRAME = get_segmented_metric_example_df()