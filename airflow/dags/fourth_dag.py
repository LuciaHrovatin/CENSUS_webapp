from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from first_dag import dag1
from second_dag import dag2
from third_dag import dag3

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": datetime.today()
}

with DAG('pipeline_dag',
         schedule_interval=None,
         default_args=default_args) as dag:

    external_dag_1 = ExternalTaskSensor(
        task_id='dag_1_completed_status',
        external_dag_id=dag1.dag_id,
        external_task_id=None, # wait for whole DAG to complete
        allowed_states=['success'],
        check_existence=True)

    external_dag_2 = ExternalTaskSensor(
        task_id='dag_2_completed',
        external_dag_id=dag2.dag_id,
        external_task_id=None,
        allowed_states=['success'],
        check_existence=True)

    external_dag_3 = ExternalTaskSensor(
        task_id='dag_3_completed',
        external_dag_id=dag3.dag_id,
        external_task_id=None,
        allowed_states=['success'],
        check_existence=True)

external_dag_1.set_downstream(external_dag_2)
external_dag_2.set_downstream(external_dag_3)