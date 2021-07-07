from __future__ import absolute_import, annotations
import requests
from zipfile import ZipFile
import os
import shutil
from typing import Optional, List
import uuid
import pandas as pd
import numpy as np
import json


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


# -----------------------------------------RENAMING/ DELETING COLUMNS ----------------------------------

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
    return table


def change_nquest(filename: str):
    """
    Function that introduces an unique primary key changing the nquest value

    :param filename: name of the dataset that will be interested by this change
    :return: the same dataset whose column nquest contains unique values
    """
    data = pd.read_csv(filename)
    changes = sub_table(filename, col_name="nquest")
    actual = [x for x in changes]
    future = [changes[x] for x in changes]
    data["nquest"].replace(to_replace=actual, value=future, inplace=True)
    data.to_csv(filename, index=None)


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
    for i in data["INDEXES"]:
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


def number_regions(filename: str, province: str) -> int:
    """
    Takes the province and returns the integer according to the data encoded in the dataset.
    :param str filename: json file containing all the Italian region
    :param str province: name of the province
    :return: integer of the region (1-20)
    """
    with open(filename) as f:
        data = json.load(f)
        # region numbers come from the dataset
        regions_n = {
            "Piemonte": 1,
            "Valle d'Aosta": 2,
            "Lombardia": 3,
            "Trentino": 4,
            "Veneto": 5,
            "Friuli": 6,
            "Liguria": 7,
            "Emilia Romagna": 8,
            "Toscana": 9,
            "Umbria": 10,
            "Marche": 11,
            "Lazio": 12,
            "Abruzzo": 13,
            "Molise": 14,
            "Campania": 15,
            "Puglia": 16,
            "Basilicata": 17,
            "Calabria": 18,
            "Sicilia": 19,
            "Sardegna": 20
        }
        for region in data:
            for prov in data[region]:
                if province in prov["nome"]:
                    region = region.split("-")[0]
                    return regions_n[region]
