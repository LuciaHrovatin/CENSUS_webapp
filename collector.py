from __future__ import absolute_import, annotations
import requests
import pandas as pd

def get_data(filename: str):
    data = pd.read_csv(filename)
    return print(data.head())

get_data("dataset/Tasso_occupazione.csv")
get_data("dataset/Tasso_disoccupazione.csv")

def rename_column(filename: str):
    data = pd.read_csv(filename)
    file_n = filename[filename.find("/")+1: ]
    # rename columns
    if file_n == "Tasso_occupazione.csv":
        renamed_data = data.rename(columns={'Value': 'VALUE EMP', 'ITTER107': 'NUTS3', 'SEXISTAT1': 'SEX', 'ETA1': 'AGE'})
        renamed_data.to_csv("dataset_clean/" + file_n, index=None)
    elif file_n == "Tasso_disoccupazione.csv":
        renamed_data = data.rename(columns={'Value': 'VALUE UNEMP', 'ITTER107': 'NUTS3', 'SEXISTAT1': 'SEX', 'ETA1': 'AGE'})
        renamed_data.to_csv("dataset_clean/" + file_n, index=None)
    elif file_n == "Qualita_vita.csv":
        renamed_data = data.rename(columns={'CODICE NUTS 3 2021': 'NUTS3', 'RIFERIMENTO TEMPORALE': 'TIME'})
        renamed_data.to_csv("dataset_clean/" + file_n, index=None)
    return print(data.head())

def delete_column(filename: str, cols_to_remove: list):
    data = pd.read_csv(filename)
    #cols_to_remove = ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags']
    del_col = []
    for i in cols_to_remove:
         if i in data.columns:
             del_col.append(i)

    delete_column = data.drop(del_col, inplace=False, axis=1)
    delete_column.to_csv(filename, index=None)

    print(data.head())

#delete_column("dataset_clean/Tasso_disoccupazione.csv")

#rename_column("dataset/Qualita_vita.csv")

delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])

# data = pd.read_csv("dataset/Tasso_disoccupazione.csv")
# renamed_data = data.rename(columns={'Value': 'Tasso di disoccupazione'})
# renamed_data.to_csv("dataset_clean/Tasso_disoccupazione.csv", index=None)

#Delete rows
#tasso occupazione/disoccupazione:
#9 in column SEX
#IT/ITC in column NUTS3 (isalpha = False)
#Q in Time