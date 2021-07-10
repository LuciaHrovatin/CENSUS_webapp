from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from saver import *
from collector import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": days_ago(1),
    'wait_for_downstream': True,
}

dag_mysql = DAG('bdt_2021_2',
          default_args=default_args,
          description='Loading data to mysql',
          schedule_interval='@once')

def open_connector(file_to_process: str):
    saver = MySQLManager(host="localhost",
                         port=3310,
                         user="root",
                         password="Pr0tett0.98")
    saver.check_database("project_bdt")
    saver.create_table(lst_tables(file_to_process))
    saver.save_SQL(file_to_process)


t1 = BashOperator(
    task_id='start_mysql',
    bash_command=print("start loading data to mysql"),
    dag=dag_mysql
)

t2 = BashOperator(
    task_id='file1',
    bash_command=open_connector("dataset/Qualita_vita.csv"),
    dag=dag_mysql
)

t3 = BashOperator(
    task_id='file2',
    bash_command=open_connector("dataset/carcom16.csv"),
    dag=dag_mysql
)

t4 = BashOperator(
    task_id='file3',
    bash_command=open_connector("dataset/carcom14.csv"),
    dag=dag_mysql
)

t5 = BashOperator(
    task_id='file4',
    bash_command=open_connector("dataset/rfam14.csv"),
    dag=dag_mysql
)

t6 = BashOperator(
    task_id='file5',
    bash_command=open_connector("dataset/rfam16.csv"),
    dag=dag_mysql
)

t7 = BashOperator(
    task_id='file6',
    bash_command=open_connector("dataset/rper14.csv"),
    dag=dag_mysql
)

t8 = BashOperator(
    task_id='file7',
    bash_command=open_connector("dataset/rper16.csv"),
    dag=dag_mysql
)

t9 = BashOperator(
    task_id='end',
    bash_command=print("Loadings ended"),
    dag=dag_mysql
)

t1.set_downstream([t2, t3, t4, t5, t6, t7, t8])

