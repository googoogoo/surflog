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
    es = Elasticsearch("http://admin_admin@localhost:9200")

    if not es.indices.create(es, "surflog"):
        mappings = {
            "properties": {
                "time": {"type": "date"},
                "dwd": {"type": "float"},
                "icon": {"type": "float"},
                "meteo": {"type": "float"},
                "noaa": {"type": "float"},
                "sg": {"type": "float"}
            }
        }

        es.indices.create(index="surflog", mappings=mappings)
    else:
        pass


    metrics = ['swellHeight', 'swellDirection', 'swellPeriod', 'waveDirection', 'waveHeight']
    list_metrics = []

    logger.info('creating dataframes')

    for metric in metrics:
        time = []
        dwd = []
        icon = []
        meteo = []
        noaa = []
        sg = []

        for hour in df['time']:
            time.append(hour)

        for hour in df[metric]:
            if 'dwd' in hour:
                dwd.append(hour['dwd'])
            else:
                dwd.append(0)
            if 'icon'in hour:
                icon.append(hour['icon'])
            else:
                icon.append(0)
            if 'meteo'in hour:
                meteo.append(hour['meteo'])
            else:
                meteo.append(0)
            if 'noaa'in hour:
                noaa.append(hour['noaa'])
            else:
                noaa.append(0)
            if 'sg'in hour:
                sg.append(hour['sg'])
            else:
                sg.append(0)

        name_metric= 'df_'+ metric
        
        df_metric = pd.DataFrame()
        
        df_metric['time'] = time
        df_metric['time'] = pd.to_datetime(df['time'])
        
        df_metric['dwd'] = dwd
        df_metric['icon'] = icon
        df_metric['meteo'] = meteo
        df_metric['noaa'] = noaa
        df_metric['sg'] = sg

        dic_metric = dict()
        dic_metric[name_metric] = df_metric

        list_metrics.append(dic_metric)

    logger.info('sending data to elasticsearch')
    for index in range(len(list_metrics)):
        for key in list_metrics[index]:
            for i, row in list_metrics[index][key].iterrows():
                doc = {
                    "time": row["time"],
                    "dwd": row["dwd"],
                    "icon": row["icon"],
                    "meteo": row["meteo"],
                    "noaa": row["noaa"],
                    "sg": row["sg"]
                }
                es.index(index="surflog", id=i, document=doc)

    logger.info('data stored in elasticsearch')






