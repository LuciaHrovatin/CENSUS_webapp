from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from collector import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": days_ago(1),
    'wait_for_downstream': True,
    'trigger_rule': 'all_success'
}

dag = DAG('bdt_2021',
          default_args=default_args,
          description='ETL part of BDT project',
          schedule_interval="@once"
          )

carc_delete = ["PERC", "parent", "ETA", "cit", "isco", "aningr", "motiv", "tipolau", "votoedu", "suedu", "selode", "annoedu", "tipodip",
                                             "univer", "apqual", "asnonoc", "NASCAREA", "nace", "nordp", "motent", "annoenus", "NASCREG", "ACOM5",
                                             "QUAL","ISCO","CLETA5", "AREA5", "studio", "Q", "SETT", "PESOFIT", "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"]

fam_canc = ['YL', 'YL1', 'YL2', 'YT', 'YTP', 'YTP1', 'YTP2', 'YTA','YTA1',
                                            'YTA2', 'YTA3', 'YTA31', 'YTA32', 'YM', 'YMA1', 'YMA2', 'YC',
                                            'YCA', 'YCA1', 'YCA2', 'YCF', 'YCF1', 'YCF2', 'YCF3', 'YCF4', 'CLY',
                                            'CLY2']
per_canc = ['YL1','YL2','YTP1','YTP2','YTA1','YTA2','YTA31','YTA32',
                                          'YL','YTP','YTA3','YTA','YT','YM','YCA1','YCA2','YCA','YCF1','YCF2','YCF3',
                                          'YCF4','YCF','YC','YMA1','YMA2']

t01 = BashOperator(
    task_id='start',
    bash_command=print("start downloading files"),
    dag=dag
)

t02 = BashOperator(
    task_id='file1',
    bash_command=download_file(
        url="https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind16_ascii.zip",
        target_path="bancaditalia_dataset_16.zip",
        file_to_keep=["carcom16.csv", "rfam16.csv", "rper16.csv"]),
    dag=dag
)

t03 = BashOperator(
    task_id='file2',
    bash_command=download_file(
        url="https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind14_ascii.zip",
        target_path="bancaditalia_dataset_14.zip",
        file_to_keep=["carcom14.csv", "rfam14.csv", "rper14.csv"],
        multistep=True),
    dag=dag
)

t04 = BashOperator(
    task_id='file3',
    bash_command=download_file(url="https://github.com/IlSole24ORE/QDV/raw/main/20201214_QDV2020_001.csv",
                               target_path="dataset/Qualita_vita.csv"),
    dag=dag
)

t05 = BashOperator(
    task_id='end',
    bash_command=print("end downloading files"),
    dag=dag
)

t06 = BashOperator(
    task_id='rename_column',
    bash_command=rename_column("dataset/Qualita_vita.csv"),
    dag=dag
)

t07 = BashOperator(
    task_id='del_col1',
    bash_command=delete_column("dataset/Qualita_vita.csv", ['CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE']),
    dag=dag
)

t08 = BashOperator(
    task_id='del_col2',
    bash_command=delete_column("dataset/carcom16.csv", carc_delete),
    dag=dag
)

t09 = BashOperator(
    task_id='del_col3',
    bash_command=delete_column("dataset/carcom14.csv", carc_delete),
    dag=dag
)

t10 = BashOperator(
    task_id='del_col4',
    bash_command=delete_column("dataset/rfam16.csv", fam_canc),
    dag=dag
)

t11 = BashOperator(
    task_id='del_col5',
    bash_command=delete_column("dataset/rfam14.csv", fam_canc),
    dag=dag
)

t12 = BashOperator(
    task_id='del_col6',
    bash_command=delete_column("dataset/rper14.csv", per_canc),
    dag=dag
)

t13 = BashOperator(
    task_id='del_col7',
    bash_command=delete_column("dataset/rper16.csv", per_canc),
    dag=dag
)

t14 = BashOperator(
    task_id='del_col8',
    bash_command=delete_column("dataset/rper16.csv", per_canc),
    dag=dag
)

t15 = BashOperator(
    task_id = "end_final",
    bash_command = print("end"),
    dag = dag
)


t01.set_downstream([t02, t03, t04])
t05.set_downstream(t06)
t06.set_downstream([t07, t08, t09, t10, t11, t12, t13, t14])
