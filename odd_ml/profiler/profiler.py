from abc import ABC, abstractmethod

import pandas as pd


class Profiler(ABC):
    @abstractmethod
    def profile(self, dataframe: pd.DataFrame) -> None:
        raise NotImplementedError

    @abstractmethod
    def profile_to_notebook(self, dataframe: pd.DataFrame) -> None:
        raise NotImplementedError
