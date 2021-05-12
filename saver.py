from __future__ import absolute_import, annotations

import mysql.connector
from mysql.connector import errorcode, Error


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

    def insert_data(self, add_str: str, table_name: str) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(add_str)
            print("Data have been sucessfully insertedd in table {}".format(table_name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_TABLE_ERROR:
                print("Table {} does not exists.". format(table_name))
            else:
                print(err.msg)
        cursor.close()




