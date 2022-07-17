from typing import Any

import pandas as pd
from pandas_profiling import ProfileReport

from odd_ml.profiler.profiler import Profiler


class PandasProfiler(Profiler):
    def profile_to_notebook(self, dataframe: pd.DataFrame) -> Any:
        profile = ProfileReport(dataframe, title="Pandas Profiling Report")
        return profile.to_notebook_iframe()

    def profile(self, dataframe: pd.DataFrame) -> Any:
        profile = ProfileReport(dataframe, title="Pandas Profiling Report")
        return profile.to_json()
