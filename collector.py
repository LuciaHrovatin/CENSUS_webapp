from __future__ import absolute_import, annotations
import requests
import pandas as pd
import re

def get_data(filename: str):
    data = pd.read_csv(filename)
    return print(data.head())

get_data("dataset/Tasso_occupazione.csv")
get_data("dataset/Tasso_disoccupazione.csv")

def rename_column(filename: str):
    """
    The function renames the column of pandas dataframes given the file name
    and save it in a new folder
    :param filename: name of the file whose columns' names will be changed
    :return file: a new dataset with columns' names standardized
    """
    data = pd.read_csv(filename)
    file_n = filename[filename.find("/")+1:] # extract the name

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

    return print(data.head())

def delete_column(filename: str, cols_to_remove: list):
    data = pd.read_csv(filename)
    del_col = []
    del_col.extend([i for i in cols_to_remove if i in data.columns])
    delete_column = data.drop(del_col, inplace=False, axis=1)
    delete_column.to_csv(filename, index=None)

    print(data.head())

# OCCUPAZIONE
#rename_column("dataset/Tasso_occupazione.csv")
#delete_column("dataset_clean/Tasso_occupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# DISOCCUPAZIONE
rename_column("dataset/Tasso_disoccupazione.csv")
delete_column("dataset_clean/Tasso_disoccupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato', 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# QUALITA VITA
# rename_column("dataset/Qualita_vita.csv")
# delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])

def clean_rows(filename: str):
    data = pd.read_csv(filename)
    if "occupazione" in filename:
        data = data.loc[data["SEX"] != 9]
        count = 0
        del_lst = []
        while count < len(data["NUTS3"]):
            if (data["NUTS3"][count].isalpha()) or ("Q" in data["TIME"][count]):
                del_lst.append(count)
            count += 1
        data = data.drop(data.index[del_lst], inplace=False)
        data.to_csv(filename, index=None)
    elif filename == "dataset_clean/Qualita_vita.csv":
        # data = data["TIME"]
        # row_del = []
        # count = 0
        # for i in data:
        #     if i.isnumeric() == False:
        #         tokens = i.split()
        #         if tokens[0].isnumeric() == False:
        #             print(tokens)

        # for i in data:
        #     if i.isnumeric() == False:
        #         i = i.split()
        #         for n in i:
        #             if n.isalpha():
        #                 del_str = i.pop(0)

        # data['TIME'] = data['TIME'].replace(r'\D', '').to_csv(filename, index=None)
        # print(data)
        count = 0
        rows_lst = []
        values = []
        for i in data:
            if not i.isnumeric():
                rows_lst.append(count)
                values.append()
        data = data.loc(rows_lst, values)
        data.to_csv(filename, index = None)












# DISOCCUPAZIONE
#clean_rows("dataset_clean/Tasso_disoccupazione.csv")

# OCCUPAZIONE
#clean_rows("dataset_clean/Tasso_occupazione.csv")

# QUALITA' DELLA VITA
# clean_rows("dataset_clean/Qualita_vita.csv")

#----TODO-----#
#Delete rows
#tasso occupazione/disoccupazione:
#9 in column SEX --> done
#IT/ITC in column NUTS3 (isalpha = False) --> done
#Q in Time --> done