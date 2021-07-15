from errno import errorcode

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.hooks.mysql_hook import MySqlHook
from airflow.sensors.external_task import ExternalTaskSensor


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)}

dag3 = DAG('mySQL_phase', schedule_interval=None, default_args=default_args)


def join_SQL(table_1: str, table_2: str, table_name: str):
    """
    Queries mysql and returns a cursor to the results.
    """

    mysql = MySqlHook(mysql_conn_id='mysql_test_conn', schema="project_bdt")
    conn = mysql.get_conn()
    cursor = conn.cursor()
    try:
        query = "CREATE TABLE {} as (SELECT n.*, s.y from {} as n join {} as s on n.{} = s.{})".format(table_name, table_1, table_2, "nquest", "nquest")
        cursor.execute(query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table {} already exists.".format(table_name))
        else:
            print(err.msg)
    cursor.close()


def union_SQL(table_1: str, table_2: str, table_name: str):
    """
    merging two tables avoiding dupicates
    :param table_1: first table to merge
    :param table_2: second table to merge
    :param table_name: name of the final table
    :return: table generated by merging by means of UNION
    """
    mysql = MySqlHook(mysql_conn_id='mysql_test_conn', schema="project_bdt")
    conn = mysql.get_conn()
    cursor = conn.cursor()
    try:
        query = "CREATE TABLE {} as (SELECT * FROM {} UNION SELECT * FROM {} WHERE {} NOT IN (SELECT {} FROM {}))".format(table_name, table_1, table_2, "nquest", "nquest", table_1)
        cursor.execute(query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table {} already exists.".format(table_name))
        else:
            print(err.msg)
    cursor.close()

t1 = PythonOperator(
    task_id='final_create',
    dag=dag3,
    python_callable=join_SQL,
    op_kwargs={'table_1': "carcom16",
               'table_2': "rfam16",
               'table_name': "data_2016_fam"}
)

t2 = PythonOperator(
    task_id='final_create_2',
    dag=dag3,
    python_callable=join_SQL,
    op_kwargs={'table_1': "carcom14",
               'table_2': "rfam14",
               'table_name': "data_2014_fam"}
)

t3 = PythonOperator(
    task_id='final_create_3',
    dag=dag3,
    python_callable=join_SQL,
    op_kwargs={'table_1': "carcom16",
               'table_2': "rper16",
               'table_name': "data_2016"}
)

t4 = PythonOperator(
    task_id='final_create_4',
    dag=dag3,
    python_callable=join_SQL,
    op_kwargs={'table_1': "carcom14",
               'table_2': "rper14",
               'table_name': "data_2014"}
)

t5 = PythonOperator(
    task_id='final_db_1',
    dag=dag3,
    python_callable=union_SQL,
    op_kwargs={'table_1': "data_2016",
               'table_2': "data_2014",
               'table_name': "final_individual"}
)

t6 = PythonOperator(
    task_id='final_db_2',
    dag=dag3,
    python_callable=union_SQL,
    op_kwargs={'table_1': "data_2016_fam",
               'table_2': "data_2014_fam",
               'table_name': "final"}
)

external_dag_2 = ExternalTaskSensor(
    task_id='dag_2_completed',
    external_dag_id='etl_phase',
    external_task_id=None,
    allowed_states=['success'],
    check_existence=True)


external_dag_2 >> t1 >> t2 >> t3 >> t4 >> t5 >> t6