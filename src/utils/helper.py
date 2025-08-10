from enum import Enum
import glob
import pandas as pd
from datetime import datetime


class ModelClasses(Enum):
    """
    Enum for different model classes.
    """
    CLASSIFICATION = "Classification"
    REGRESSION = "Regression"
    CLUSTERING = "Clustering"
    TIME_SERIES = "Time Series"
    ANOMALY_DETECTION = "Anomaly Detection"


def get_logs_info():
    logs_info = glob.glob('.\\logs\\*\\*', recursive=True)
    log_info_df = pd.DataFrame(index=logs_info)
    log_info_df['uuid'] = log_info_df.index.str.split('\\').str[-2]
    log_info_df['file_name'] = log_info_df.index.str.split('\\').str[-1]
    log_info_df['path'] = log_info_df.index
    log_info_df['stage_name'] = log_info_df['file_name'].str.split('.').str[0].replace('\d', '', regex=True).map(lambda x:x[:-1] if x[-1] == '-' else x)
    log_info_df['stage_check'] = log_info_df['file_name'].str.split('.').str[1] == 'log'
    log_info_df['timestamp'] = log_info_df['file_name'].str.split('-').str[-1].str.split('.').str[0].map(lambda x:x if x.isdigit() else None)
    log_info_df['formatted_time'] = log_info_df['timestamp'].apply(lambda x: datetime.strptime(x, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S") if x is not None else None)
    log_info_df['success'] = False
    grouped_df = log_info_df.groupby('uuid')
    for uuid, group in grouped_df:
        if 'index.html' in group['file_name'].values:
            log_info_df.loc[log_info_df[log_info_df['uuid'] == uuid].index, 'success'] = True
    log_info_df.sort_values(by=['uuid', 'timestamp'], inplace=True)
    log_info_df.reset_index(drop=True, inplace=True)
    return log_info_df
