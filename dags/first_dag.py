import os
import shutil
from typing import Optional
from zipfile import ZipFile
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime


def download_file(url: str, target_path: str, file_to_keep: Optional[list] = None, multistep: Optional[bool] = False):
    """
    Using a url and setting a target_path, the function downloads the required files saving
    them locally into the folder "dataset".
    :param str url: link to the repository online
    :param str target_path: directory in which files will be saved
    :param list file_to_keep: list containing only the files to keep
    :param bool multistep: by default it is set to False, but if switched to True performs a two-step file extraction
    """
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()

    if not file_to_keep is None:
        if multistep:
            with ZipFile(target_path, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall(path='dataset')

            for i in file_to_keep:
                shutil.move("dataset/CSV/" + i, "dataset")

            if os.path.exists('dataset/CSV'):
                shutil.rmtree('dataset/CSV')
        else:
            with ZipFile(target_path, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                # zipObj.extractall(path='./dataset')
                for i in file_to_keep:
                    zipObj.extract(i, path='dataset')
        os.remove(target_path)


default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": datetime.now(),
    'wait_for_downstream': True,
    'trigger_rule': 'all_success',
}

dag = DAG('bdt_2021',
          default_args=default_args,
          description='Files download',
          schedule_interval=None
          )



t01 = PythonOperator(
    task_id='file1',
    python_callable = download_file,
    op_kwargs={'url': "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind16_ascii.zip",
        'target_path': "bancaditalia_dataset_16.zip",
        'file_to_keep': ["carcom16.csv", "rfam16.csv", "rper16.csv"]},
    dag=dag
)

t02 = PythonOperator(
    task_id='file2',
    python_callable = download_file,
    op_kwargs={'url': "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind14_ascii.zip",
        'target_path':"bancaditalia_dataset_14.zip",
        'file_to_keep': ["carcom14.csv", "rfam14.csv", "rper14.csv"],
        'multistep':True},
    dag=dag
)

t03 = PythonOperator(
    task_id='file3',
    python_callable=download_file,
    op_kwargs={
        'url': "https://github.com/IlSole24ORE/QDV/raw/main/20201214_QDV2020_001.csv",
        'target_path':"dataset/Qualita_vita.csv"},
    dag=dag
)



# sequence of events
t01.set_downstream(t02)
t02.set_downstream(t03)