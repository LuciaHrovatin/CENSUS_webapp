from __future__ import absolute_import, annotations

import uuid
from datetime import datetime

import ns as ns
import pandas as pd
import json
from typing import Optional, List
import numpy as np


# class File:
#
#     def __init__(self, filename: str):
#         self.filename = filename

# TODO #
# inserire in __init__ la possibilità di inserire il nome corto del file ex: filename[filename.find("/")+1:]
# così da poterlo richiamare in futuro
# Inserire funzione GET_NAME (solo nome senza dataet... e csv)

    # ----------------------------------------- GETTING DATA -----------------------------------------------

    # def get_data(self):
    #     data = pd.read_csv(self.filename)
    #     return print(data.head())

# -----------------------------------------RENAMING/ DELETING COLUMNS ----------------------------------
from numpy import datetime64


def rename_column(filename: str):
    """
    The function renames the column of pandas dataframes given the file name
    and save it in a new folder
    :param filename: name of the file whose columns' names will be changed
    :return file: a new dataset with columns' names standardized
    """
    data = pd.read_csv(filename)
    file_n = filename[filename.find("/")+1:]  # extract the name
    if file_n == "Qualita_vita.csv":
        renamed_data = data.rename(columns={'CODICE NUTS 3 2021': 'NUTS3',
                                            'RIFERIMENTO TEMPORALE': 'TIME',
                                            'INDICATORE': 'INDEX'})
    elif "occupazione" in file_n:
        renamed_data = data.rename(columns={'Value': ('Value_UNEMP' if "dis" in file_n else 'Value_EMP'),
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
    :param filename: name of the file
    :return: the file updated
    """
    data = pd.read_csv(filename)
    count = 0
    row_lst = []
    if "occupazione" in filename:
        while count < len(data["NUTS3"]):
            if (data["NUTS3"][count].isalpha()) or ("Q" in data["TIME"][count]) or (data["SEX"][count] == 9):
                row_lst.append(count)
            count += 1
        data = data.drop(data.index[row_lst], inplace=False)
    else:
        target = "INDEX"
        indicators_lst = list_arg("dataset_clean/indicators.json")  # problem in running functions ?
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

def sub_table(filename: str):
    """
    The function saves each indicator with the corresponding measure and a randomly generated index
    :param filename: name of the file
    :return: a dictionary having as keys the indicators and as values a list with measure and unique index
    """
    data = pd.read_csv(filename)
    table = dict()
    count = 0
    for row in data["INDEX"]:
        if row not in table:
            table[row] = [data["UNITA' DI MISURA"][count], "INDEX" + uuid.uuid4().hex[:6].upper()]
        count += 1
    return table

def save(table: dict):
    """
    Save the column of "Unità di misura" together with its indicator
    and add a randomly generated index
    :param dict table: dictionary having indicators as keys and description of indicators as values
    :return: json file
    """
    with open("dataset_clean/indicators.json", "w") as f:
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

def del_indicators(filename: str, indicators: List):
    """
    The function deletes all rows containing an index not relevant for further analyses
    :param str filename: name of the file from which deleting the rows
    :param list indicators: list of indicators not relevant for further analyses
    :return: cleaned file
    """
    data = pd.read_csv(filename)
    row_lst = []
    count = 0
    for i in data["INDEX"]:
        if i in indicators:
            row_lst.append(count)
        count += 1
    data = data.drop(data.index[row_lst], inplace=False)
    data.to_csv(filename, index=None)

# ---------------------------------------------- CREATE LIST OF TABLES ---------------------------------------

def lst_tables(filename: str) -> tuple:
    """
    The function prepares the SQL command to insert a new table into the chosen database
    :param str filename: name of the dataset to be inserted
    :return: tuple having as first element the name of the new table and as second element the SQL command
    """
    name = filename[filename.find("\\")+1:filename.find(".")].lower()
    data = pd.read_csv(filename, parse_dates=["TIME"])
    table_to_be = []
    cols = [str(i) for i in data.columns.tolist()]
    for i in range(len(cols)):
        pointer = data.loc[0, cols[i]]
        if isinstance(pointer, datetime):
            table_to_be.append("`" + cols[i].lower() + "` DATETIME NOT NULL")
        elif isinstance(pointer, str):
            table_to_be.append("`" + cols[i].lower() + "` VARCHAR(255) NOT NULL")
        elif isinstance(pointer, np.int64):
            table_to_be.append("`" + cols[i].lower() + "` INT NOT NULL")
        elif isinstance(pointer, float):
            table_to_be.append("`" + cols[i].lower() + "` FLOAT NOT NULL")
    data_set = "CREATE TABLE `" + name + "` ( `id` int NOT NULL AUTO_INCREMENT, \n" +\
               ", \n".join(table_to_be) + ", PRIMARY KEY(`id`))"
    return print(name, data_set)









