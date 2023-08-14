# SurfLog
A Python program to monitor the waves at my local surf spot.

# Requirements
Python 3 and Docker Desktop installed and running.

# Install
```console
python -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```

# Run
```console
docker-compose up -d
python query_stormglass.py
```

# Explore
In your browser, access localhost:3000 to access Grafana. Login with user: admin y password: secret. Browse the configured Dashboards or a new one.
