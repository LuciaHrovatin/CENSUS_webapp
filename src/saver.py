from __future__ import absolute_import, annotations
import mysql.connector
from mysql.connector import errorcode, Error
import pandas as pd


class MySQLManager:

    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        """
        Connects python to MySQL, requiring host, port, username, password and database.
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )
        self.connection.autocommit = True


    def label_irpef(self, table_name: str):
        """
        Creates census brackets following the Irpef (sub)categories.
        :param str table_name: Name of the table whose census data will be modified
        :return: modified table having the attribute "y" standardized
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
        """
        Selecting query to recall a table stored in the project_bdt database
        :param str table_name: name of the table that the user wants to recall
        :return: the table is returned as Pandas DataFrame
        """
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM {}".format(table_name)
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result)
        except Error as e:
            print(f"The error '{e}' occurred")

