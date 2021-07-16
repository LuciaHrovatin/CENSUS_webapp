import time
import requests
from saver import MySQLManager
from classifier import redis_training
import os

url = 'http://localhost:8080/api/v1/pools'
r = requests.get(url, auth=('airflow', 'airflow'))

for dag_name in ["ingestion_phase", "etl_phase", "mySQL_phase"]:
    url = 'http://localhost:8080/api/v1/dags/' + dag_name + '/dagRuns'
    headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    r = requests.post(url, headers=headers, data="{}", auth=('airflow', 'airflow'))
    run = True
    allowed_state = 'success'
    while run:
        url = 'http://localhost:8080/api/v1/dags/' + dag_name + '/dagRuns'
        r = requests.get(url, auth=('airflow', 'airflow'))
        result = r.json()
        print("{} is running".format(dag_name))
        for entry in result["dag_runs"]:
            if entry["state"] == allowed_state:
                run = False
        else:
            time.sleep(40)

cursor_Mysql = MySQLManager(host="localhost",
                            port=3310,
                            user="root",
                            password="password",
                            database="project_bdt")

cursor_Mysql.label_irpef(table_name="final")
cursor_Mysql.label_irpef(table_name="final_individual")

# Redis training
redis_training(saver=cursor_Mysql, table="final", case=1)
redis_training(saver=cursor_Mysql, table="final", case=2, sex=True)
redis_training(saver=cursor_Mysql, table="final_individual", case=3)
redis_training(saver=cursor_Mysql, table="final_individual", case=3, sex=True)

# Connecting to flask
os.environ['FLASK_APP'] = 'main.py'
os.system("flask run")
