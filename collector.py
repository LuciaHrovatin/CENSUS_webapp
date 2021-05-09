from __future__ import absolute_import, annotations

import uuid
from typing import Optional

import pandas as pd
import json

from saver import MySQLManager


def get_data(filename: str):
    data = pd.read_csv(filename)
    return print(data.head())


# get_data("dataset/Tasso_occupazione.csv")
# get_data("dataset/Tasso_disoccupazione.csv")

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
    if file_n == "Qualita_vita.csv": # INDEX invece che indicatore
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
#rename_column("dataset/Tasso_disoccupazione.csv")
#delete_column("dataset_clean/Tasso_disoccupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# QUALITA VITA
rename_column("dataset/Qualita_vita.csv")
delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])


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
        return 2020 # opzione da controllare! il periodo di riferimento è 2021 - 2050



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



# DISOCCUPAZIONE
# clean_rows("dataset_clean/Tasso_disoccupazione.csv")

# OCCUPAZIONE
#clean_rows("dataset_clean/Tasso_occupazione.csv")


# QUALITA' DELLA VITA
# clean_rows("dataset_clean/Qualita_vita.csv")

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
    for row in data["INDICATORE"]:
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

save(sub_table("dataset_clean\Qualita_vita.csv"))


def list_arg(filename: str):
    with open(filename, "r") as f:
        rows = json.load(f)
        return rows

clean_rows("dataset_clean\Qualita_vita.csv", ind=True)

# --------------------------------------------- DELETE UNITA' di MISURA -----------------------------------------------
# Delete the column of "unità di misura"
# delete_column("dataset_clean\Qualita_vita.csv", ["UNITA' DI MISURA"])

# ---------------------------------------------CONNECTION WITH SERVER -------------------------------------------------
# saver = MySQLManager(host = "localhost",
#                      port = 3306,
#                      database= "project_bdt",
#                      user = "root",
#                      password = "Pr0tett0.98")
#
# def create_list(filename: str):
#     data = pd.read_csv(filename)
#     lst_variables = dict()
#     for var in data.columns:
#         lst_variables[var] = data[var][0]
#     return lst_variables
#
# saver.create_table("DB_disoccupazione", create_list("dataset_clean\Tasso_disoccupazione.csv"))



indicators = ["INDEX76871E", #Eventi sportivi
              "INDEXB05593", #Indice di lettura dei quotidiani
              "INDEX0491CE", #Spettacoli - Spesa al botteghino
              "INDEXDE3F0F", #Furti
              "INDEXE11E38", #Furti in abitazione
              "INDEXA8ECC7", #Furti in esercizi commerciali
              "INDEXFC3F69", #Estorsioni
              "INDEXB0650A", #Truffe e frodi informatiche
              "INDEX6A80DB", #Incendi
              "INDEX04D681", #Omicidi da incidente stradale
              "INDEX3C118A", #Violenze sessuali
              "INDEX63EC14", #Indice di litigiosit\u00e0
              "INDEXCB2857", #Durata media delle cause civili
              "INDEX714B87", #Indice di rotazione delle cause
              "INDEX366745", #Quota cause pendenti ultratriennali
              "INDEXFAE6DF", #Riciclaggio e impiego di denaro
              "INDEXD0AFFD", #Incidenti stradali
              "INDEX3EEFEF", #Cancellazioni anagrafiche
              "INDEXE4E4B4", #Iscrizioni anagrafiche
              "INDEX1D0B90", #Consumo di farmaci per asma e Bpco
              "INDEXDFA4EE", #Consumo di farmaci per diabete
              "INDEXA6392E", #Consumo di farmaci per ipertensione
              "INDEXB5A68C", #Consumo di farmaci per la depressione
              "INDEX010345", #Infermieri
              "INDEXFE4E12", #Pediatri
              "INDEX5F7000", #Calmanti e sonniferi
              "INDEX7DFBB3", #Casi Covid-19
              "INDEXF16526", #Rata media mensile
              "INDEXD2282E", #Popolazione con crediti attivi
              "INDEX57FDFB", #Fatture commerciali ai fornitori oltre i 30 giorni
              "INDEX374CD6", #Nuovi mutui per l'acquisto di abitazioni
              "INDEX928F97", #Protesti
              "INDEX566396", #Imprese in fallimento
              "INDEX97E1D9", #Imprese che fanno ecommerce
              "INDEXE71DD5", #Imprese straniere
              "INDEX3A4097", #Imprese in rete
              "INDEX50EF15", #Tasso di occupazione
              "INDEX575B7B", #Quota di export sul Pil
              "INDEX25CA91", #Banda larga
              "INDEXB4363E", #Cig ordinaria autorizzata
              "INDEXCBB68C", #Nuove iscrizioni di imprese
              "INDEX7CE928", #Indice di Rischio Climatico (CRI)
              "INDEXD501C1", #Fondi europei 2014-2020 per l'Agenda digitale
              "INDEX007575", #Fondi europei 2014-2020 per l'ambiente e la prevenzione dei rischi
              "INDEX3AFA5C", #Pago Pa - enti attivi
              "INDEX4E38A7", #Partecipazione alla formazione continua
              "INDEX5E3BEB", #Cie erogate
              "INDEXA41E08", #Spid erogate
              "INDEX125395" #Pos attivi
              ]


def del_indicators(filename: str, indicators: List):

    data = pd.read_csv(filename)
    row_lst = []
    for i in data["INDICATORE"]:
        if i in indicators:
            row_lst.append(i)
        data = data.drop(data.index[row_lst], inplace=False)
    # data = data.drop(data.index[row_lst], inplace=False)

# del_indicators("dataset_clean/Qualita_vita.csv", indicators)


# TODO#
# crea un nuovo file definito "runner" per far runnare le funzioni
# lascia qui le funzioni
# creare la funzione dell'indicatore



