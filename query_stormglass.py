import requests
import json
import schedule
import time
from apscheduler.schedulers.background import BlockingScheduler
import logging
import os
import requests
import pandas as pd
import etl_mysql
import etl_elastic


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('surflog.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def query_api():
  try:
    #Request data from the API
    logger.info('requesting data from stormglass')
    response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
        'lat': 41.404015,
        'lng': 2.218565,
        'params': ','.join(['swellHeight','swellDirection','swellPeriod','waveHeight','waveDirection','waveDirection'])
      },
      headers={
        'Authorization': os.environ.get('API_KEY')
      }
    )
    logger.info('data collected from stormglass')
    
    json_data = response.json()
    if os.path.exists("stormglass_data.json"):
      os.remove("stormglass_data.json")

    with open("stormglass_data.json", 'w') as f:
      json.dump(json_data, f)

  except requests.exceptions.HTTPError as errh:
    logger.error("HTTP Error")
    logger.error(errh.args[0])
  except requests.exceptions.ReadTimeout as errrt:
    logger.error("Time out")
  except requests.exceptions.ConnectionError as conerr:
    logger.error("Connection error")
  except requests.exceptions.RequestException as errex:
    logger.error("Exception request")



  logger.info('cleaning data and creating dataframe')
  #Create dataframe with the results of our query
  df = pd.DataFrame(json_data['hours'])

  return df


def main():
  df = query_api()
  etl_mysql.insert_mysql(df)
  etl_elastic.insert_elastic(df)

if __name__ == "__main__":
  main()
  scheduler = BlockingScheduler()
  scheduler.add_job(main, 'interval', hours = 24)
  scheduler.start()