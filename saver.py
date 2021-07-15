from __future__ import absolute_import, annotations
import mysql.connector
from mysql.connector import errorcode, Error
import pandas as pd


class MySQLManager:

    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )
        self.connection.autocommit = True

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
            query = " UPDATE {} SET {} = CASE" \
                    " WHEN {} < 15000 THEN '1'" \
                    " WHEN {} BETWEEN 15001 AND 22000 THEN '2'" \
                    " WHEN {} BETWEEN 22001 AND 28000 THEN '3'" \
                    " WHEN {} BETWEEN 28001 AND 35000 THEN '4'" \
                    " WHEN {} BETWEEN 35001 AND 42000 THEN '5'" \
                    " WHEN {} BETWEEN 42001 AND 49000 THEN '6'" \
                    " WHEN {} BETWEEN 49001 AND 55000 THEN '7'" \
                    " WHEN {} BETWEEN 55001 AND 75000 THEN '8'" \
                    " ELSE '9'" \
                    " END".format(table_name, "y", "y", "y", "y", "y", "y", "y", "y", "y")
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

