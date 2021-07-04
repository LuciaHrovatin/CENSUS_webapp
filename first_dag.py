
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from textwrap import dedent
from collector import * 

default_args = {
    'owner': 'airflow',
    'depends_on_past':True,
    'email_on_failure': ['luciahrovatin@gmail.com'],
    'email_on_retry': ['luciahrovatin@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'wait_for_downstream': True,
    "start_date": days_ago(1)
}

with DAG(
    'bdt_project_2021',
    default_args=default_args,
    description='ETL part of BDT project',
    schedule_interval='@once',
) as dag:



    # t1, t2 and t3 are examples of tasks created by instantiating operators
    # [START basic_task]

    t1 = BashOperator(
        task_id='initialise',
        bash_command=rename_column("dataset/Qualita_vita.csv"),
        dag = dag
    )

    t2 = BashOperator(
        task_id='delete',
        bash_command=delete_column("dataset_clean/Qualita_vita.csv", ['CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE']),
        dag=dag
    )
    # [END basic_task]

    t3 = BashOperator(
         task_id='print',
         bash_command=print("DONE"),
        dag= dag
     )

    # bin shift operator
    t1 >> t2 >> t3

    # t2 will depend on t1
    #t1.set_downstream(t2)

 #t3 will depend on t1
 #t3.set_upstream(t1)

    # tasks in parallel:
    #t1.set_downstream([t2, t3])
