from __future__ import absolute_import, annotations

import mysql.connector
from mysql.connector import errorcode, Error
import pandas as pd


class MySQLManager:

    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        self.connection.autocommit = True

    def create_database(self, name_DB: str):
        """
        Creates a new database if the called one does not exist
        :param str name_DB: name of the database
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name_DB))
        except Error as err:
            print("Failed in creation database: {}".format(err))
            exit(1)


    def check_database(self, name_DB: str):
        """
        Checks whether the called database exists or not
        :param str name_DB: name of the database involved in further analyses
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("USE {}".format(name_DB))
            print("Database {} exists.".format(name_DB))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(name_DB))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(name_DB)
                print("Database {} created successfully.".format(name_DB))
                self.connection.database = name_DB
            else:
                print(err)
                exit(1)

    def create_table(self, new_table: tuple) -> None:
        """
        The function creates a new table if it is not already present in the database
        :param tuple new_table: tuple having as first element the name of the
        table and as second one its schema as SQL command
        :return: a new table inside the chosen database
        """
        cursor = self.connection.cursor()
        try:
            print("Table {} will be created: ".format(new_table[0]), end='')
            cursor.execute(new_table[1])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(new_table[0]))
            else:
                print(err.msg)
        cursor.close()

    def save_SQL(self, filename: str):
        cursor = self.connection.cursor()
        name = filename[filename.find("\\") + 1:filename.find(".")].lower()
        data = pd.read_csv(filename)
        cols = "`, `".join([str(i).lower() for i in data.columns.tolist()])
        for i, row in data.iterrows():
            sql = "INSERT INTO " + name + "(`" + cols + "`) VALUES (" + "%s,"*(len(row) - 1) + "%s)"
            cursor.execute(sql, tuple(row))
        print("Data have been successfully inserted in table {}".format(name))





