from __future__ import absolute_import, annotations

import json
import os
import mysql.connector
from typing import Optional, List


class MySQLManager:

    def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.connection.autocommit = True

    def create_table(self, db_table: str, columns: dict) -> None:
        cursor = self.connection.cursor()
        table_to_be = []
        for column in columns:
            if type(columns[column]) is str:
                table_to_be.append(column + " VARCHAR(255)")
            else: #isinstance(columns[column], int):
                table_to_be.append(column + " NUMERIC")
        #print("CREATE TABLE" + db_table+ "(id INT AUTO_INCREMENT PRIMARY KEY," + ",".join(table_to_be) + ")")
        cursor.execute("CREATE TABLE " + db_table+ " (id INT AUTO_INCREMENT PRIMARY KEY," + ",".join(table_to_be) + ")")


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

