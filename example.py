# TENTATIVO DI AVVIARE AIRFLOW
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'tutorial',
    default_args=default_args,
    start_date=datetime(2015, 12, 1),
    description='A simple tutorial DAG',
    schedule_interval='@once',
    catchup=False)

