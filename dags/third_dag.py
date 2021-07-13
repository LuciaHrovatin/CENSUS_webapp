import numpy as np
from airflow import DAG
from datetime import timedelta, datetime
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": datetime.today(),
    'wait_for_downstream': True
}

dag_google = DAG('bdt_2021_google',
                default_args=default_args,
                description='Loading data to GoogleBigQuery',
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

csv_to_bigquery = GoogleCloudStorageToBigQueryOperator(
    task_id= 'csv_to_bigquery',
    google_cloud_storage_conn_id='google_cloud_default',
    bucket= 'airflow_bucket',
    source_objects=['dataset/rper16.csv'],
    
    skip_leading_rows=1,
    bigquery_conn_id='google_cloud_default',
    destination_project_dataset_table='{}.{}.{}'.format("project_bdt", "bdt", "rper12"),
    source_format='CSV',
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_APPEND',
    schema_update_options=['ALLOW_FIELD_RELAXATION', 'ALLOW_FIELD_ADDITION'],
    autodetect=True,
    dag=dag_google
)

csv_to_bigquery
