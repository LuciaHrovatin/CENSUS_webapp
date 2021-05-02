from __future__ import absolute_import, annotations
import requests
import pandas as pd

def get_data(filename: str):
    data = pd.read_csv(filename)
    return print(data.head())

get_data("dataset/Tasso_occupazione.csv")
get_data("dataset/Tasso_disoccupazione.csv")

def clean_data(filename: str):
    data = pd.read_csv(filename)
    # rename value of occupazione/dispccupazione
    if filename == "dataset/Tasso_occupazione.csv":
        renamed_data = data.rename(columns={'Value': 'Tasso di occupazione'})
        renamed_data.to_csv(filename, index=None)
    elif filename == "dataset/Tasso_disoccupazione.csv":
        renamed_data = data.rename(columns={'Value': 'Tasso di disoccupazione'})
        renamed_data.to_csv(filename, index=None)
    # rename with NUTS3 code
    renamed_location = data.rename(columns={'ITTER107': 'NUTS3'})
    renamed_location.to_csv(filename, index=None)
    # delete Flag Code & Flags
    data.drop(['Flag Codes', 'Flags'], inplace=True, axis=1)


    print(data.head())

clean_data("dataset/Tasso_occupazione.csv")

