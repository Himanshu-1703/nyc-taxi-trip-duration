import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from src.logger import CustomLogger, create_log_path


TARGET_COLUMN = 'trip_duration'
PLOT_PATH = Path("/reports/figures")

log_file_path = create_log_path('modify_features')
# create the custom logger object
dataset_logger = CustomLogger(logger_name='modify_features',
                              log_filename=log_file_path)
# set the level of logging to INFO
dataset_logger.set_log_level(level=logging.INFO)


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

def plot_target(dataframe: pd.DataFrame, target_column: str, save_path: str):
    sns.kdeplot(data=dataframe, x=target_column)
    plt.title(f'Distribution of {target_column}')
    plt.savefig(save_path)
    
    
    
def drop_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe_after_removal = dataframe.drop(columns=['id','dropoff_datetime'])
    return dataframe_after_removal


def make_datetime_features(dataframe: pd.DataFrame,column_type:str='pickup') -> pd.DataFrame:
    dataframe[f'{column_type}_hour'] = dataframe[f'{column_type}_datetime'].dt.hour 
    dataframe[f'{column_type}_date'] = dataframe[f'{column_type}_datetime'].dt.day
    dataframe[f'{column_type}_month'] = dataframe[f'{column_type}_datetime'].dt.month
    dataframe[f'{column_type}_day'] = dataframe[f'{column_type}_datetime'].dt.weekday
    dataframe[f'is_weekend'] = dataframe.apply(lambda row: row[f'{column_type}_day'] >= 5,axis=1).astype('int')
    return dataframe


def remove_passengers(dataframe: pd.DataFrame) -> pd.dataFrame:
    passengers_to_include = list(range(1,7))
    new_dataframe_filter = dataframe['passenger_count'].isin(passengers_to_include)
    new_dataframe = dataframe.loc[new_dataframe_filter,:]
    return new_dataframe


def input_modifications(dataframe: pd.DataFrame) -> pd.DataFrame:
    new_df = drop_columns(dataframe)
    df_passengers_modifications = remove_passengers(new_df)
    df_with_datetime_features = make_datetime_features(dataframe)
    return df_with_datetime_features

   
def target_modifications(dataframe: pd.DataFrame, target_column: str=TARGET_COLUMN) -> pd.DataFrame:
    minutes_dataframe = convert_target_to_minutes(dataframe,target_column)
    target_outliers_removed_df = drop_above_hundred_minutes(minutes_dataframe,target_column)
    plot_target(dataframe=target_outliers_removed_df,target_column=target_column,
                save_path=PLOT_PATH / 'target_distribution.png')
    return target_outliers_removed_df


# * Make Excalidraw for the steps 

# TODO 1. Make a function to read the dataframe from the dvc.yaml file
# TODO 2. Add Logging Functionality to each function
# TODO 3. Run the code in notebook mode to test with print statements
# ! Code not tested yet
# ? Should logging be added to each function or the main function for specific steps


def main():
    pass
