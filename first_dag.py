from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from textwrap import dedent
from collector import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'email': ['luciahrovatin@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'wait_for_downstream': True,
    "start_date": days_ago(1)

}

dag = DAG('bdt_project_2021',
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

# bin shift operator
t1 >> [t2, t3, t4] >> t5

# t2 will depend on t1
# t1.set_downstream(t2)

# t3 will depend on t1
# t3.set_upstream(t1)

# tasks in parallel:
# t1.set_downstream([t2, t3])
