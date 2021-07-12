import numpy as np
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
import pandas as pd
from saver import MySQLManager

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": datetime.today(),
    'wait_for_downstream': True
}

dag_mysql = DAG('bdt_2021_mysql',
                default_args=default_args,
                description='Loading data to mysql',
                schedule_interval=None)

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

def open_connector(saver: MySQLManager, filename: str):
    saver.check_database("project_bdt")
    saver.create_table(lst_tables(filename))
    saver.save_sql(filename)


saver = PythonOperator(
    task_id= "open_connection",
    python_callable=MySQLManager,
    provide_context=True,
    op_kwargs={'host': "127.0.0.1",
               'port': 3307,
               'user': "root",
               'password': "password"},
    dag=dag_mysql

)

t1 = PythonOperator(
     task_id='file1',
     python_callable= open_connector,
     op_kwargs={'saver': saver,
                'filename': "dataset/Qualita_vita.csv"},
     dag=dag_mysql
)

t2 = PythonOperator(
     task_id='file2',
     python_callable=open_connector,
     op_kwargs={'saver': saver,
                'filename': "dataset/carcom16.csv"},
     dag=dag_mysql
)

t3 = PythonOperator(
    task_id='file3',
    python_callable=open_connector,
    op_kwargs={'saver': saver,
               'filename': "dataset/carcom14.csv"},
    dag=dag_mysql
)

t4 = PythonOperator(
    task_id='file4',
    python_callable=open_connector,
    op_kwargs={'saver': saver,
               'filename': "dataset/rfam14.csv"},
    dag=dag_mysql
)

t5 = PythonOperator(
    task_id='file5',
    python_callable=open_connector,
    op_kwargs={'saver': saver,
               'filename': "dataset/rfam16.csv"},
    dag=dag_mysql
)

t6 = PythonOperator(
    task_id='file6',
    python_callable=open_connector,
    op_kwargs={'saver': saver,
               'filename': "dataset/rper16.csv"},
    dag=dag_mysql
)

t7 = PythonOperator(
    task_id='file7',
    python_callable=open_connector,
    op_kwargs={'saver': saver,
               'filename': "dataset/rper14.csv"},
    dag=dag_mysql
)

saver.set_downstream(t1)
t1.set_downstream(t2)
t2.set_downstream(t3)
t3.set_downstream(t4)
t5.set_upstream(t4)
t6.set_upstream(t5)
t7.set_upstream(t6)
