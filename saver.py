from __future__ import absolute_import, annotations

import mysql.connector
from mysql.connector import errorcode, Error
import pandas as pd


class MySQLManager:

    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.connection.autocommit = True

    def create_database(self):
        """
        Creates a new database if the called one does not exist
        :param str name_DB: name of the database
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.connection.database))
        except Error as err:
            print("Failed in creation database: {}".format(err))
            exit(1)


    def check_database(self):
        """
        Checks whether the called database exists or not
        :param str name_DB: name of the database involved in further analyses
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("USE {}".format(self.connection.database))
            print("Database {} exists.".format(self.connection.database))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.connection.database))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(self.connection.database)
                print("Database {} created successfully.".format(self.connection.database))
                self.connection.database = self.connection.database
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

    def save_SQL(self, filename: str) -> None:
        """
        Inserting the records in the appropriate table
        :param str filename: name of the  file
        """
        cursor = self.connection.cursor()
        name = filename[filename.find("/") + 1: filename.find(".")].lower()
        data = pd.read_csv(filename)
        data.dropna(inplace=True)
        cols = "`, `".join([str(i).lower() for i in data.columns.tolist()])
        for i, row in data.iterrows():
            sql = "INSERT INTO " + name + "(`" + cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
            cursor.execute(sql, tuple(row))
        print("Data have been successfully inserted in table {}".format(name))

    def join_SQL(self, table_1: str, table_2: str, table_name: str):
        """
        Function that joins two tables and reports the new one on MySQL
        :param table_1: first table to join
        :param table_2: second table to join
        :param table_name: name of the final table
        :return: table generated by joining two tables on the attribute nquest (number of questionnaire)
        """
        cursor = self.connection.cursor()
        try:
            query = "CREATE TABLE {} as (SELECT n.*, s.Y from {} as n join {} as s on n.nquest = s.nquest)".format(table_name, table_1, table_2)
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(table_name))
            else:
                print(err.msg)
        cursor.close()


    def union_SQL(self, table_1: str, table_2: str, table_name: str):
        """
        merging two tables avoiding dupicates
        :param table_1: first table to merge
        :param table_2: second table to merge
        :param table_name: name of the final table
        :return: table generated by merging by means of UNION
        """
        cursor = self.connection.cursor()
        try:
            query = "CREATE TABLE {} as (SELECT * FROM {} UNION SELECT * FROM {} WHERE nquest NOT IN (SELECT nquest FROM {}))".format(table_name, table_1, table_2, table_1)
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(table_name))
            else:
                print(err.msg)
        cursor.close()

    def modify_columns(self, table_name: str, col_name_1: str, col_name_2: str):
        """
        Changes the order of the columns in order to merge them
        :param table_name: SQL table where columns are swapped
        :param col_name_1: name of first column to swap
        :param col_name_2: name of second column to swap
        """
        cursor = self.connection.cursor()
        try:
            query = "ALTER TABLE `{}` CHANGE COLUMN `{}` `{}` INT NOT NULL AFTER`{}`;".format(table_name, col_name_1, col_name_1, col_name_2)
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(table_name))
            else:
                print(err.msg)
        cursor.close()


    def label_irpef(self, table_name: str):
        """
        Creates census classes following the 5 Irpef categories.
        :param table_name: Name of the table whose census data will be modified
        :return: modified table having the attribute "Y" standardized
        """
        cursor = self.connection.cursor(buffered=True)
        try:
            query = " UPDATE {} SET Y = CASE" \
                    " WHEN Y < 15000 THEN '1'" \
                    " WHEN Y BETWEEN 15001 AND 22000 THEN '2'" \
                    " WHEN Y BETWEEN 22001 AND 28000 THEN '3'" \
                    " WHEN Y BETWEEN 28001 AND 35000 THEN '4'" \
                    " WHEN Y BETWEEN 35001 AND 42000 THEN '5'" \
                    " WHEN Y BETWEEN 42001 AND 49000 THEN '6'"\
                    " WHEN Y BETWEEN 49001 AND 55000 THEN '7'" \
                    " WHEN Y BETWEEN 55001 AND 75001 THEN '8'" \
                    " ELSE '9'"\
                    " END".format(table_name)
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(table_name))
            else:
                print(err.msg)
        cursor.close()


    def execute_read_query(self, table_name: str):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM {}".format(table_name)
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result)
        except Error as e:
            print(f"The error '{e}' occurred")








