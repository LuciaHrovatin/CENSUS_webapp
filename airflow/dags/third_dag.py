from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.mysql_operator import MySqlOperator
import pandas as pd
import requests
import json

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag_mySQL = DAG('MySQL', schedule_interval=None, default_args=default_args)

def lst_tables(filename: str) -> tuple:
    """
    The function prepares the SQL command to insert a new table into the chosen database
    :param str filename: name of the dataset to be inserted
    :return: tuple having as first element the name of the new table and as second element the SQL command
    """
    name = filename[filename.find("/") + 1:filename.find(".")].lower()
    data = pd.read_csv(filename)
    table_to_be = []
    cols = [str(i) for i in data.columns.tolist()]
    primary_key = 0
    for i in range(len(cols)):
        pointer = data.loc[0, cols[i]]
        if cols[i].lower() == "id":
            primary_key = ", PRIMARY KEY(`{}`))".format(cols[i].lower())
        if isinstance(pointer, str):
            table_to_be.append("`" + cols[i].lower() + "` VARCHAR(255) NOT NULL")
        elif isinstance(pointer, np.int64):
            table_to_be.append("`" + cols[i].lower() + "` INT NOT NULL")
        elif isinstance(pointer, float):
            table_to_be.append("`" + cols[i].lower() + "` FLOAT NOT NULL")
    if not primary_key:
        data_set = "CREATE TABLE `" + name + "` ( `id` int NOT NULL AUTO_INCREMENT, \n" + \
                   ", \n".join(table_to_be) + ", PRIMARY KEY(`id`))"
    else:
        data_set = "CREATE TABLE `" + name + "` ( " + ", \n".join(table_to_be) + primary_key
    return name, data_set



def check_table_exists(name:str, **kwargs):
    query = "select count(*) from {}.tables where table_name=".format("project_bdt", name)
    mysql_hook = MySqlHook(mysql_conn_id='mysql_test_conn', schema='project_bdt')
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def store_data(filename: str, **kwargs):
    res = lst_tables(filename)
    table_status = check_table_exists(res[0])
    mysql_hook = MySqlHook(mysql_conn_id='mysql_test_conn', schema='project_bdt')
    if table_status[0][0] == 0:
        print("----- table does not exists, creating it")    
        create_sql = res[1]
        mysql_hook.run(create_sql)
    else:
        print("----- table already exists")
    name = filename[filename.find("/") + 1: filename.find(".")].lower()
    data = pd.read_csv(filename)
    data.dropna(inplace=True)
    cols = "`, `".join([str(i).lower() for i in data.columns.tolist()])
    for i, row in data.iterrows():
        sql = "INSERT INTO " + name + "(`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
        mysql_hook.run(sql, parameters=(data.get("title"), data.get("id")))


py1 = PythonOperator(
    task_id='store_opt',
    dag=dag_mySQL,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/rper16.csv'}
)

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello World from Task 1"',
    dag=dag_mySQL)

py1 >> t1