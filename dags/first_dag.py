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
    'queue': 'bash_queue'

}

dag = DAG('bdt_2021',
          default_args=default_args,
          description='ETL part of BDT project',
          schedule_interval='@once'
          )

t1 = BashOperator(
    task_id='start',
    bash_command=print("start downloading files"),
    dag=dag
)

t2 = BashOperator(
    task_id='file1',
    bash_command=download_file(
        url="https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind16_ascii.zip",
        target_path="bancaditalia_dataset_16.zip",
        file_to_keep=["carcom16.csv", "rfam16.csv", "rper16.csv"]),
    dag=dag
)

t3 = BashOperator(
    task_id='file2',
    bash_command=download_file(
        url="https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind14_ascii.zip",
        target_path="bancaditalia_dataset_14.zip",
        file_to_keep=["carcom14.csv", "rfam14.csv", "rper14.csv"],
        multistep=True),
    dag=dag
)

t4 = BashOperator(
    task_id='file3',
    bash_command=download_file(url="https://github.com/IlSole24ORE/QDV/raw/main/20201214_QDV2020_001.csv",
                               target_path="dataset/Qualita_vita.csv"),
    dag=dag
)

t5 = BashOperator(
    task_id='end',
    bash_command=print("end downloading files"),
    dag=dag
)

t6 = BashOperator(
    task_id='rename_column',
    bash_command=rename_column("dataset/Qualita_vita.csv"),
    dag=dag
)

t7 = BashOperator(
    task_id='del_col1',
    bash_command=delete_column("dataset/Qualita_vita.csv", ['CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE']),
    dag=dag
)

t8 = BashOperator(
    task_id='del_col2',
    bash_command=delete_column("dataset/carcom16.csv", ["PERC", "parent", "ETA", "cit", "isco", "aningr", "motiv", "tipolau", "votoedu", "suedu", "selode", "annoedu", "tipodip",
                                             "univer", "apqual", "asnonoc", "NASCAREA", "nace", "nordp", "motent", "annoenus", "NASCREG", "ACOM5",
                                             "QUAL","ISCO","CLETA5", "AREA5", "studio", "Q", "SETT", "PESOFIT", "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"]),
    dag=dag
)

t9 = BashOperator(
    task_id='fine',
    bash_command=print("ho finito!"),
    dag=dag
)


# bin shift operator
t1 >> [t2, t3, t4] >> t5 >> t6 >> [t7, t8]

# t2 will depend on t1
# t1.set_downstream(t2)

# t3 will depend on t1
# t3.set_upstream(t1)

# tasks in parallel:
# t1.set_downstream([t2, t3, t4]) # data collection
# t3.set
