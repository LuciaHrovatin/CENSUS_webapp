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

    def create_database(self, DB_name: str):
        """
        Creates a new database if the called one does not exist
        :param str DB_name: name of the database
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_name))
        except Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)


    def check_database(self, DB_name: str):
        """
        Checks whether the called database exists or not
        :param str DB_name: name of the database involved in further analyses
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("USE {}".format(DB_name))
            print("Database {} exists.".format(DB_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(DB_name)
                print("Database {} created successfully.".format(DB_name))
                self.connection.database = DB_name
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
            print("Creating table {}: ".format(new_table[0]), end='')
            cursor.execute(new_table[1])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(new_table[0]))
            else:
                print(err.msg)
        else:
            print("DONE")
        cursor.close()



