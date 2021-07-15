import time
import requests
from saver import MySQLManager
from classifier import redis_training
import os


# rename_column("dataset/Qualita_vita.csv")
# delete_column("dataset/Qualita_vita.csv", ['CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])
#
# # DATA 2016 e 2014 hanno le stesse colonne !!
# delete_column("dataset/carcom16.csv", ["perc", "parent", "ETA", "cit", "isco", "aningr", "motiv", "tipolau", "votoedu", "suedu", "selode", "annoedu", "tipodip",
#                                              "univer", "apqual", "asnonoc", "NASCAREA", "nace", "nordp", "motent", "annoenus", "NASCREG", "ACOM5",
#                                              "QUAL","ISCO","CLETA5", "AREA5", "studio", "Q", "SETT", "PESOFIT", "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"])
#
# delete_column("dataset/carcom14.csv", ["perc", "AREA5", "parent", "ETA", "cit", "isco", "aningr", "motiv", "tipolau", "VOTOEDU", "SUEDU", "selode", "annoedu", "tipodip",
#                                               "univer", "apqual", "asnonoc", "NASCAREA", "nace", "nordp", "motent", "annoenus", "NASCREG", "ACOM5",
#                                               "QUAL","ISCO","CLETA5", "studio", "Q", "SETT", "PESOFIT", "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"])
#
# # Stessa cosa vale per rfam14 e 16
# delete_column("dataset/rfam14.csv", ['YL', 'YL1', 'YL2', 'YT', 'YTP', 'YTP1', 'YTP2', 'YTA','YTA1',
#                                             'YTA2', 'YTA3', 'YTA31', 'YTA32', 'YM', 'YMA1', 'YMA2', 'YC',
#                                             'YCA', 'YCA1', 'YCA2', 'YCF', 'YCF1', 'YCF2', 'YCF3', 'YCF4', 'CLY',
#                                             'CLY2'])
#
# delete_column("dataset/rfam16.csv", ['YL', 'YL1', 'YL2', 'YT', 'YTP', 'YTP1', 'YTP2', 'YTA','YTA1',
#                                            'YTA2', 'YTA3', 'YTA31', 'YTA32', 'YM', 'YMA1', 'YMA2', 'YC',
#                                            'YCA', 'YCA1', 'YCA2', 'YCF', 'YCF1', 'YCF2', 'YCF3', 'YCF4', 'CLY',
#                                            'CLY2'])
# # Stessa cosa vale per rper14 e 16
# delete_column("dataset/rper16.csv", ['YL1','YL2','YTP1','YTP2','YTA1','YTA2','YTA31','YTA32',
#                                           'YL','YTP','YTA3','YTA','YT','YM','YCA1','YCA2','YCA','YCF1','YCF2','YCF3',
#                                           'YCF4','YCF','YC','YMA1','YMA2'])
#
# delete_column("dataset/rper14.csv", ['YL1','YL2','YTP1','YTP2','YTA1','YTA2','YTA31','YTA32',
#                                            'YL','YTP','YTA3','YTA','YT','YM','YCA1','YCA2','YCA','YCF1','YCF2','YCF3',
#                                            'YCF4','YCF','YC','YMA1','YMA2'])
#
# # QUALITA' DELLA VITA -> save indicators
# save(sub_table("dataset/Qualita_vita.csv", "INDEXES"))
#
# # QUALITA' DELLA VITA -> clean rows
# clean_rows("dataset/Qualita_vita.csv")
# clean_rows("dataset/Qualita_vita.csv", ind=True)
#
# # --------------------------------------------- DELETE INDECES NOT NEEDED --------------------------------------------
# # List of indicators that will be deleted due to their inconsistency with the project purpose
#
#
# lst_index = list_arg("dataset/indicators.json")
# del_indicators("dataset/Qualita_vita.csv")
#
# # --------------------------------------------- DELETE "UNITA' di MISURA" -----------------------------------------------
# # Delete the column of "unità di misura"
# delete_column("dataset\Qualita_vita.csv", ["UNITA' DI MISURA"])


for dag_name in ["ingestion_phase", "etl_phase", "mySQL_phase"]:
    url = 'http://localhost:8080/api/v1/dags/'+dag_name+'/dagRuns'
    headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    r = requests.post(url, headers=headers, data="{}", auth=('airflow', 'airflow'))
    run = True
    allowed_state = 'success'
    while run:
        url = 'http://localhost:8080/api/v1/dags/'+dag_name+'/dagRuns'
        r = requests.get(url, auth=('airflow', 'airflow'))
        result = r.json()
        for entry in result["dag_runs"]:
            if entry["state"] == allowed_state:
                run = False
        else:
            time.sleep(20)

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
os.system('cmd /c "set FLASK_APP=main.py"')
os.system('cmd /c "flask run"')







