from __future__ import absolute_import, annotations

import uuid
from datetime import datetime
from typing import Optional

import pandas as pd
import json

def get_data(filename: str):
    data = pd.read_csv(filename)
    return print(data.head())


get_data("dataset/Tasso_occupazione.csv")
get_data("dataset/Tasso_disoccupazione.csv")

# -----------------------------------------RENAMING/ DELETING COLUMNS ----------------------------------


def rename_column(filename: str):
    """

    The function renames the column of pandas dataframes given the file name
    and save it in a new folder
    :param filename: name of the file whose columns' names will be changed
    :return file: a new dataset with columns' names standardized
    """
    data = pd.read_csv(filename)
    file_n = filename[filename.find("/")+1:]  # extract the name

    # rename columns
    if file_n == "Qualita_vita.csv":
        renamed_data = data.rename(columns={'CODICE NUTS 3 2021': 'NUTS3',
                                            'RIFERIMENTO TEMPORALE': 'TIME'})
    elif "occupazione" in file_n:
        renamed_data = data.rename(columns={'Value': ('VALUE UNEMP' if "dis" in file_n else 'VALUE EMP'),
                                                'ITTER107': 'NUTS3',
                                                'SEXISTAT1': 'SEX',
                                                'ETA1': 'AGE'})
    renamed_data.to_csv("dataset_clean/" + file_n, index=None)



def delete_column(filename: str, cols_to_remove: list):
    """
    The function deletes the columns contained in the list cols_to_remove.
    :param str filename: name of the file on which the modifications are applied
    :param list cols_to_remove: list of columns' names that have to be removed
    :return: return the same dataset but updated
    """

    data = pd.read_csv(filename)
    del_col = []
    del_col.extend([i for i in cols_to_remove if i in data.columns])
    delete_column = data.drop(del_col, inplace=False, axis=1)
    delete_column.to_csv(filename, index=None)

# OCCUPAZIONE
# rename_column("dataset/Tasso_occupazione.csv")
# delete_column("dataset_clean/Tasso_occupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# DISOCCUPAZIONE
# rename_column("dataset/Tasso_disoccupazione.csv")
# delete_column("dataset_clean/Tasso_disoccupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# QUALITA VITA
rename_column("dataset/Qualita_vita.csv")
delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])


# -----------------------------------------CLEANING ROWS ----------------------------------

def clean_rows(filename: str, ind: Optional[bool] = False):
    """
    The function cleans the dataset from the rows which contains special cases.
    It also updates the value of certain rows
    :param filename: name of the file
    :return: the file updated
    """
    data = pd.read_csv(filename)
    count = 0
    row_lst = []
    if "occupazione" in filename:
        data = data.loc[data["SEX"] != 9]
        while count < len(data["NUTS3"]):
            if (data["NUTS3"][count].isalpha()) or ("Q" in data["TIME"][count]):
                row_lst.append(count)
            count += 1
        data = data.drop(data.index[row_lst], inplace=False)
    else:
        if not ind:
            target = "TIME"
            for row in data[target]:
                if not row.isnumeric():
                    value = parse_date(row)
                    row_lst.append((count, value))
                count += 1
        else:
            target = "INDICATORE"
            indicators_lst = list_arg("dataset_clean\indicators.json")
            for row in data[target]:
                value = indicators_lst[row][-1]
                row_lst.append((count, value))
                count += 1
        if 0 < len(row_lst):
            data.loc[[v[0] for v in row_lst], [target]] = [v[1] for v in row_lst]
    data.to_csv(filename, index=None)


def parse_date(stringa: str):
    try:
        value = [v for v in stringa.split() if v.isnumeric() and len(v) == 4]
        if len(value) == 1:
            return value[0]
    except Exception:
        print("Oops! Two years have been founded")

# DISOCCUPAZIONE
# clean_rows("dataset_clean/Tasso_disoccupazione.csv")

# OCCUPAZIONE
# clean_rows("dataset_clean/Tasso_occupazione.csv")


# QUALITA' DELLA VITA
clean_rows("dataset_clean/Qualita_vita.csv")


# ----------------------------------------- STORE PROPERLY ----------------------------------

def sub_table(filename: str):
    data = pd.read_csv(filename)
    table = dict()
    count = 0
    for row in data["INDICATORE"]:
        if row not in table:
            table[row] = [data["UNITA' DI MISURA"][count], "INDEX" + uuid.uuid4().hex[:6].upper()]
        count += 1
    return table

# TODO#
# Better implement the MANAGER
def save(table: dict):
    """
    Save the column of "Unità di misura" together with its indicator
    and add a randomly generated indentifier
    :param dict table: dictionary having indicators as keys and description of indicators as values
    :return: json file
    """
    with open("dataset_clean/indicators.json", "w") as f:
        json.dump(
            table,
            f,
            indent=4
            )

#save(sub_table("dataset_clean\Qualita_vita.csv"))

# TODO # --> done
# create a table where unit of measure and indicators are reported --> save it as JSON FILE
# it will correspond to another table having 3 columns
# --> 1 codice indicatore
# --> 2 indicatore stesso
# --> 3 unità di misura


# TODO# --> done
# Generare una stringa o un codice identificativo per ogni indice in
# maniera da avere una foreign key nella tabella secondaria


def list_arg(filename: str):
    with open(filename, "r") as f:
        rows = json.load(f)
        return rows

clean_rows("dataset_clean\Qualita_vita.csv", ind=True)

# --------------------------------------------- DELETE UNITA' di MISURA ---------------------------------------------------
# Delete the column of "unità di misura"
delete_column("dataset_clean\Qualita_vita.csv", ["UNITA' DI MISURA"])