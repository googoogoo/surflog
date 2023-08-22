import logging
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('surflog.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def insert_elastic(df):
    logger.info('connecting to elasticsearch')
    es = Elasticsearch("http://localhost:9200")

    if not es.indices.exists(index="surflog"):
        logger.info('creating index')
        mappings = {
            "properties": {
                "time": {"type": "date"},
                "metric": {"type": "text"},
                "icon": {"type": "float"},
                "meteo": {"type": "float"},
                "noaa": {"type": "float"},
                "sg": {"type": "float"}
            }
        }
        es.indices.create(index="surflog", mappings=mappings)

    logger.info('creating dataframes')
    metrics = ['swellHeight','swellDirection','swellPeriod','waveHeight','waveDirection','waveDirection']
    df_list = []
    for metric in metrics:
        df_name = 'df' + str(metric)
        df_name = df[['time', metric]].copy()
        df_name['metric'] = str(metric)
        df_temp = pd.DataFrame(df_name[metric].to_list())
        df_name = pd.concat([df_name, df_temp], axis='columns')
        df_name = df_name[['time', 'metric', 'icon', 'meteo', 'noaa', 'sg']].copy()
        df_name.fillna(0, inplace=True)
        df_list.append(df_name)

    dfmetrics = pd.concat(df_list)
    dfmetrics.reset_index(drop=True, inplace=True)

    logger.info('sending data to elasticsearch')
    for i, row in dfmetrics.iterrows():
        doc = {
            "time": row["time"],
            "metric": row["metric"],
            "icon": row["icon"],
            "meteo": row["meteo"],
            "noaa": row["noaa"],
            "sg": row["sg"]
        }
        es.index(index="surflog", id=i, document=doc)

    logger.info('data stored in elasticsearch')






