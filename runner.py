import time
import requests
from src.saver import MySQLManager
from src.classifier import redis_training
import os

# First (delayed) authentication
time.sleep(15)
url = 'http://localhost:8080/api/v1/pools'
r = requests.get(url, auth=('airflow', 'airflow'))

for dag_name in ["ingestion_phase", "etl_phase", "mySQL_phase"]:
    url = 'http://localhost:8080/api/v1/dags/' + dag_name + '/dagRuns'
    headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    r = requests.post(url, headers=headers, data="{}", auth=('airflow', 'airflow'))
    run = True
    print("{} is running".format(dag_name))
    while run:
        url = 'http://localhost:8080/api/v1/dags/' + dag_name + '/dagRuns'
        r = requests.get(url, auth=('airflow', 'airflow'))
        result = r.json()
        for entry in result["dag_runs"]:
            if entry["state"] == "success":
                run = False
            elif entry["state"] == "failed":
                print("Please access to Airflow websever")
        else:
            time.sleep(30)  # function freezes the code for 30 seconds, another interval can be set

cursor_Mysql = MySQLManager(host="localhost",
                            port=3310,
                            user="root",
                            password="password",
                            database="project_bdt")

cursor_Mysql.label_irpef(table_name="final")
cursor_Mysql.label_irpef(table_name="final_individual")

# Redis training of 4 models
# 1. Final dataset with variable sex
redis_training(saver=cursor_Mysql, table="final", case=1)

# 2. Final dataset without variable sex
redis_training(saver=cursor_Mysql, table="final", case=2, no_sex=True)

# 3. Final_individual (statciv=1) dataset with variable sex
redis_training(saver=cursor_Mysql, table="final_individual", case=3)

# 4. Final_individual (statciv=1) dataset without variable sex
redis_training(saver=cursor_Mysql, table="final_individual", case=4, no_sex=True)

# Connecting and launching flask
os.environ['FLASK_APP'] = 'main.py'
os.system("flask run")
