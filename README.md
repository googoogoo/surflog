# SurfLog
A Python program to monitor the waves at my local surf spot. Create a free account for the Stormglass API here: https://stormglass.io/.

### Requirements
Python 3 and Docker Desktop installed and running.

### Install (Mac, Linux)
```console
python3 -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```

### Launch docker containers
```console
docker-compose up -d
```
#### Expected output
```console
[+] Running 3/3
 ✔ Container elasticsearch      Started                                                                                   1.3s 
 ✔ Container surflog_db         Started                                                                                   0.7s 
 ✔ Container surflog-grafana-1  Started                                                                                   1.8s 
```
### Launch program
```console
python query_stormglass.py
```
#### Expected output
```console
2023-08-15 16:35:43,653 - __main__ - INFO - requesting data from stormglass
2023-08-15 16:35:44,725 - __main__ - INFO - data collected from stormglass
2023-08-15 16:35:44,768 - __main__ - INFO - cleaning data and creating dataframe
2023-08-15 16:35:44,774 - etl_mysql - INFO - connecting to mysql
2023-08-15 16:35:44,891 - etl_mysql - INFO - creating dataframes
2023-08-15 16:35:44,901 - etl_mysql - INFO - sending data to mysql
2023-08-15 16:35:45,260 - etl_mysql - INFO - sending data to mysql
2023-08-15 16:35:45,447 - etl_mysql - INFO - sending data to mysql
2023-08-15 16:35:45,651 - etl_mysql - INFO - sending data to mysql
2023-08-15 16:35:45,997 - etl_mysql - INFO - sending data to mysql
2023-08-15 16:35:47,002 - etl_mysql - INFO - data stored in mysql
2023-08-15 16:35:47,002 - etl_elastic - INFO - connecting to elasticsearch
2023-08-15 16:35:47,004 - etl_elastic - INFO - creating dataframes
2023-08-15 16:35:47,038 - etl_elastic - INFO - sending data to elasticsearch
2023-08-15 16:36:01,670 - etl_elastic - INFO - data stored in elasticsearch
```
#### Program execution
The program runs once every 24 hours. To stop the program, press Ctrl + C.

### Explore data
* In your browser, type *localhost:3000* to access Grafana.
* Login with *user: admin* and *password: secret*.
* Browse the existing Dashboard or build a new one with existing datasource.
