from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class DatasetStorage(ABC):
    @abstractmethod
    def get_dataframe(self, data_entity: Any) -> pd.DataFrame:
        raise NotImplementedError
