import csv
import json
import uuid
from typing import Optional
import numpy as np
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, datetime
from airflow.hooks.mysql_hook import MySqlHook


# -----------------------------------
def rename_column(filename: str):
    """
    The function renames the column of pandas dataframes given the file name
    and save it in a new folder
    :param filename: name of the file whose columns' names will be changed
    :return file: a new dataset with columns' names standardized
    """
    data = pd.read_csv(filename)
    file_n = filename[filename.find("/") + 1:]  # extract the name
    if file_n == "Qualita_vita.csv":
        renamed_data = data.rename(columns={'CODICE NUTS 3 2021': 'NUTS3',
                                            'RIFERIMENTO TEMPORALE': 'TIME',
                                            'INDICATORE': 'INDEXES',
                                            'NOME PROVINCIA (ISTAT)': 'PROVINCE'})
    renamed_data.to_csv("dataset/" + file_n, index=None)


def delete_column(filename: str, cols_to_remove: list):
    """
    The function deletes the columns contained in the list cols_to_remove.
    :param str filename: name of the file on which the modifications are applied
    :param list cols_to_remove: list of columns' names that have to be removed
    :return: return the same dataset but updated
    """
    data = pd.read_csv(filename)
    del_col = [i for i in cols_to_remove if i in data.columns]
    data = data.drop(del_col, inplace=False, axis=1)
    data.to_csv(filename, index=None)

# -----------------------------------------CLEANING ROWS ----------------------------------

def parse_date(str_date: str):
    """
    Checks whether a string contains a year and return that year. If more than one year is found,
    the function yields an exception
    :param str str_date: string where there is at least one year
    :return str: a string containing only the year
    """
    value = [v for v in str_date.split() if (v.isnumeric() and len(v) == 4)]
    if len(value) == 1:
        return value[0]
    else:
        return 2020  # inserted due to rows 2021-2050


def clean_rows(filename: str, ind: Optional[bool] = False):
    """
    The function cleans the dataset from the rows which contains special cases.
    It also updates the value of certain rows
    :param str filename: name of the file
    :param ind:
    :return: the file updated
    """
    data = pd.read_csv(filename)
    count = 0
    row_lst = []
    target = "INDEXES"
    indicators_lst = list_arg("dataset/indicators.json")
    if not ind:
        target = "TIME"
    for row in data[target]:
        if not ind:
            if not row.isnumeric():
                value = parse_date(row)
                row_lst.append((count, value))
        else:
            value = indicators_lst[row][-1]
            row_lst.append((count, value))
        count += 1
    if 0 < len(row_lst):
        data.loc[[v[0] for v in row_lst], [target]] = [v[1] for v in row_lst]
    data.to_csv(filename, index=None)


# ----------------------------------------- STORE PROPERLY ----------------------------------

def sub_table(filename: str, col_name: str):
    """
    The function saves each indicator with the corresponding measure and a randomly generated index
    :param str col_name: name of the involved column
    :param str filename: name of the file
    :return: a dictionary having as keys the indicators and as values a list with measure and unique index
    """
    data = pd.read_csv(filename)
    table = dict()
    count = 0
    for row in data[col_name]:
        if col_name == "INDEXES":
            if row not in table:
                table[row] = [data["UNITA' DI MISURA"][count], "INDEXES" + uuid.uuid4().hex[:6].upper()]
        else:
            table[row] = str(row) + "A" + str(count)
        count += 1
    return save(table)


def save(table: dict):
    """
    Save the column of "Unità di misura" together with its indicator
    and add a randomly generated index
    :param dict table: dictionary having indicators as keys and description of indicators as values
    :return: json file
    """
    with open("dataset/indicators.json", "w") as f:
        json.dump(
            table,
            f,
            indent=4
        )


def list_arg(filename: str):
    """
    The function returns the content of the json file given as input
    :param filename: name of the json file
    :return: content of the file
    """
    with open(filename, "r") as f:
        rows = json.load(f)
        return rows

# ---------------------------------------------DELETE NOT RELEVANT INDICATORS-----------------------------------------

def del_indicators(filename: str):
    """
    The function deletes all rows containing an index not relevant for further analyses
    :param str filename: name of the file from which deleting the rows
    :param list indicators: list of indicators not relevant for further analyses
    :return: cleaned file
    """
    lst_index = list_arg("dataset/indicators.json")
    indicators = [lst_index["Eventi sportivi"][1],
                  lst_index["Indice di lettura dei quotidiani"][1],
                  lst_index["Spettacoli - Spesa al botteghino"][1],
                  lst_index["Furti"][1],
                  lst_index["Furti in abitazione"][1],
                  lst_index["Furti in esercizi commerciali"][1],
                  lst_index["Estorsioni"][1],
                  lst_index["Truffe e frodi informatiche"][1],
                  lst_index["Incendi"][1],
                  lst_index["Omicidi da incidente stradale"][1],
                  lst_index["Violenze sessuali"][1],
                  lst_index["Indice di litigiosit\u00e0"][1],
                  lst_index["Durata media delle cause civili"][1],
                  lst_index["Indice di rotazione delle cause"][1],
                  lst_index["Quota cause pendenti ultratriennali"][1],
                  lst_index["Riciclaggio e impiego di denaro"][1],
                  lst_index["Incidenti stradali"][1],
                  lst_index["Cancellazioni anagrafiche"][1],
                  lst_index["Iscrizioni anagrafiche"][1],
                  lst_index["Consumo di farmaci per asma e Bpco"][1],
                  lst_index["Consumo di farmaci per diabete"][1],
                  lst_index["Consumo di farmaci per ipertensione"][1],
                  lst_index["Consumo di farmaci per la depressione"][1],
                  lst_index["Infermieri"][1],
                  lst_index["Pediatri"][1],
                  lst_index["Calmanti e sonniferi"][1],
                  lst_index["Casi Covid-19"][1],
                  lst_index["Rata media mensile"][1],
                  lst_index["Popolazione con crediti attivi"][1],
                  lst_index["Fatture commerciali ai fornitori oltre i 30 giorni"][1],
                  lst_index["Nuovi mutui per l'acquisto di abitazioni"][1],
                  lst_index["Protesti"][1],
                  lst_index["Partecipazione elettorale"][1],
                  lst_index["Imprese in fallimento"][1],
                  lst_index["Imprese che fanno ecommerce"][1],
                  lst_index["Imprese straniere"][1],
                  lst_index["Imprese in rete"][1],
                  lst_index["Tasso di occupazione"][1],
                  lst_index["Quota di export sul Pil"][1],
                  lst_index["Banda larga"][1],
                  lst_index["Cig ordinaria autorizzata"][1],
                  lst_index["Ecosistema urbano"][1],
                  lst_index["Assegni sociali"][1],
                  lst_index["Il trend del Pil pro capite"][1],
                  lst_index["Riqualificazioni energetiche degli immobili"][1],
                  lst_index["Nuove iscrizioni di imprese"][1],
                  lst_index["Indice di Rischio Climatico (CRI)"][1],
                  lst_index["Fondi europei 2014-2020 per l'Agenda digitale"][1],
                  lst_index["Fondi europei 2014-2020 per l'ambiente e la prevenzione dei rischi"][1],
                  lst_index["Pago Pa - enti attivi"][1],
                  lst_index["Indice trasormazione digitale"][1],
                  lst_index["Partecipazione alla formazione continua"][1],
                  lst_index["Cie erogate"][1],
                  lst_index["Spid erogate"][1],
                  lst_index["Pos attivi"][1]]
    data = pd.read_csv(filename)
    row_lst = []
    count = 0
    for i in data["INDEXES"]:
        if i in indicators:
            row_lst.append(count)
        count += 1
    data = data.drop(data.index[row_lst], inplace=False)
    data.to_csv(filename, index=None)


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


# ------------------------------------------- DAG -----------------------------------------------

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "start_date": datetime.now(),
    'wait_for_downstream': True,
    'trigger_rule': 'all_success',
}

dag2 = DAG('etl_phase',
          default_args=default_args,
          description='ETL files',
          schedule_interval=None
          )

fam_canc = ['YL', 'YL1', 'YL2', 'YT', 'YTP', 'YTP1', 'YTP2', 'YTA', 'YTA1',
            'YTA2', 'YTA3', 'YTA31', 'YTA32', 'YM', 'YMA1', 'YMA2', 'YC',
            'YCA', 'YCA1', 'YCA2', 'YCF', 'YCF1', 'YCF2', 'YCF3', 'YCF4', 'CLY', 'CLY2']

per_canc = ['YL1', 'YL2', 'YTP1', 'YTP2', 'YTA1', 'YTA2', 'YTA31', 'YTA32',
            'YL', 'YTP', 'YTA3', 'YTA', 'YT', 'YM', 'YCA1', 'YCA2', 'YCA', 'YCF1', 'YCF2', 'YCF3',
            'YCF4', 'YCF', 'YC', 'YMA1', 'YMA2']

t1 = PythonOperator(
    task_id='rename_column',
    python_callable=rename_column,
    op_kwargs={'filename': "dataset/Qualita_vita.csv"},
    dag=dag2
)

t2 = PythonOperator(
    task_id='del_col1',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/Qualita_vita.csv",
               'cols_to_remove': ['CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE']},
    dag=dag2
)

t3 = PythonOperator(
    task_id='save_indicators',
    python_callable=sub_table,
    op_kwargs={'filename': "dataset/Qualita_vita.csv",
               'col_name': "INDEXES"},
    dag=dag2
)

t4 = PythonOperator(
    task_id='clean_rows1',
    python_callable=clean_rows,
    op_kwargs={'filename': "dataset/Qualita_vita.csv"},
    dag=dag2
)

t5 = PythonOperator(
    task_id='clean_rows2',
    python_callable=clean_rows,
    op_kwargs={'filename': "dataset/Qualita_vita.csv",
               'ind': True},
    dag=dag2
)

t6 = PythonOperator(
    task_id='del_indicators',
    python_callable=del_indicators,
    op_kwargs={'filename': "dataset/Qualita_vita.csv"},
    dag=dag2
)

t7 = PythonOperator(
    task_id='del_col2',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/Qualita_vita.csv",
               'cols_to_remove': ["UNITA' DI MISURA"]},
    dag=dag2
)

t8 = PythonOperator(
    task_id='del_col3',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/carcom16.csv",
               'cols_to_remove': ["PERC", "parent", "ETA", "cit", "isco", "aningr", "motiv",
                                  "tipolau", "votoedu", "suedu", "selode", "annoedu", "tipodip",
                                  "univer", "apqual", "asnonoc", "NASCAREA", "nace", "nordp",
                                  "motent", "annoenus", "NASCREG", "ACOM5", "QUAL", "ISCO",
                                  "CLETA5", "AREA5", "studio", "Q", "SETT", "PESOFIT", "CFRED",
                                  "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"]},
    dag=dag2
)

t9 = PythonOperator(
    task_id='del_col4',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/carcom14.csv",
               'cols_to_remove': ["PERC", "AREA5", "parent", "ETA", "cit", "isco", "aningr",
                                  "motiv", "tipolau", "VOTOEDU", "SUEDU", "selode", "annoedu",
                                  "tipodip", "univer", "apqual", "asnonoc", "NASCAREA", "nace",
                                  "nordp", "motent", "annoenus", "NASCREG", "ACOM5",
                                  "QUAL", "ISCO", "CLETA5", "studio", "Q", "SETT", "PESOFIT",
                                  "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"]},
    dag=dag2
)

t10 = PythonOperator(
    task_id='del_col5',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/rfam16.csv",
               'cols_to_remove': fam_canc},
    dag=dag2
)

t11 = PythonOperator(
    task_id='del_col6',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/rfam14.csv",
               'cols_to_remove': fam_canc},
    dag=dag2
)

t12 = PythonOperator(
    task_id='del_col7',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/rper14.csv",
               'cols_to_remove': per_canc},
    dag=dag2
)

t13 = PythonOperator(
    task_id='del_col8',
    python_callable=delete_column,
    op_kwargs={'filename': "dataset/rper16.csv",
               'cols_to_remove': per_canc},
    dag=dag2
)

def lst_tables(filename: str) -> tuple:
    """
    The function prepares the SQL command to insert a new table into the chosen database
    :param str filename: name of the dataset to be inserted
    :return: tuple having as first element the name of the new table and as second element the SQL command
    """
    name = filename[filename.find("/")+1 :filename.find(".")].lower()
    data = pd.read_csv(filename)
    table_to_be = []
    cols = [str(i) for i in data.columns.tolist()]
    for i in range(len(cols)):
        pointer = data.loc[0, cols[i]]
        if isinstance(pointer, str):
            table_to_be.append("`" + cols[i].lower() + "` VARCHAR(255) NOT NULL")
        elif isinstance(pointer, np.int64):
            table_to_be.append("`" + cols[i].lower() + "` INT NOT NULL")
        elif isinstance(pointer, float):
            table_to_be.append("`" + cols[i].lower() + "` FLOAT NOT NULL")
    data_set = "CREATE TABLE `" + name + "` ( " + ", \n".join(table_to_be) + ")"
    return name, data_set



def create_db(filename: str, **kwargs):
    res = lst_tables(filename)
    mysql_hook = MySqlHook(mysql_conn_id='mysql_test_conn', schema="project_bdt")
    mysql_hook.run(res[1])


def store_data(filename: str, **kwargs):
    res = lst_tables(filename)
    mysql_hook = MySqlHook(mysql_conn_id='mysql_test_conn', schema="project_bdt")
    with open(filename, "r", newline='') as f:
        results = csv.reader(f)
        next(results, None) # skip the header
        mysql_hook.insert_rows(table=res[0], rows=results)


py1 = PythonOperator(
     task_id='create_db',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/rfam14.csv'}
 )


py2 = PythonOperator(
    task_id='store_opt',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/rfam14.csv'}
)


py3 = PythonOperator(
     task_id='create_db_2',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/rfam16.csv'}
 )


py4 = PythonOperator(
    task_id='store_opt_2',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/rfam16.csv'}
)


py5 = PythonOperator(
     task_id='create_db_3',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/rper16.csv'}
 )


py6 = PythonOperator(
    task_id='store_opt_3',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/rper16.csv'}
)


py7 = PythonOperator(
     task_id='create_db_4',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/rper14.csv'}
 )


py8 = PythonOperator(
    task_id='store_opt_4',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/rper14.csv'}
)

py9 = PythonOperator(
     task_id='create_db_5',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/carcom14.csv'}
 )


py10 = PythonOperator(
    task_id='store_opt_5',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/carcom14.csv'}
)

py11 = PythonOperator(
     task_id='create_db_6',
     dag=dag2,
     python_callable=create_db,
     op_kwargs={'filename': 'dataset/carcom16.csv'}
 )


py12 = PythonOperator(
    task_id='store_opt_6',
    dag=dag2,
    python_callable=store_data,
    op_kwargs={'filename': 'dataset/carcom16.csv'}
)



# Sequence of the DAG
t1 >> [t2, t8, t9, t10, t11, t12, t13] >> t3 >> t4 >> t5 >> t6 >> t7 >> py1 >> py2 >> py3 >> py4 >> py5 >> py6 >> py7 >> py8 >> py9 >> py10 >> py11 >> py12