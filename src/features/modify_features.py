import numpy as np
import pandas as pd
import logging
from pathlib import Path
from src.logger import CustomLogger, create_log_path


def convert_target_to_minutes(dataframe: pd.DataFrame, target_column: str) -> pd.DataFrame:
    dataframe.loc[:,target_column] = dataframe[target_column] / 60
    return dataframe

def drop_above_hundred_minutes(dataframe: pd.DataFrame, target_column: str) -> pd.DataFrame:
    filter_series = dataframe[target_column] <= 100
    new_dataframe = dataframe.loc[filter_series,:].copy()
    max_value = new_dataframe[target_column].max()
    
    if max_value <= 100:
        return new_dataframe
    else:
        raise ValueError('')         # TODO Think of a good error message 

