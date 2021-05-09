from __future__ import absolute_import, annotations

import json
import os
import mysql.connector
from typing import Optional, List


class MySQLStationManager:

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
        cursor = self.cursor()
        table_to_be = []
        for column in columns:
            if type(columns[column]) is str:
                table_to_be.append(column + "VARCHAR(255)")
            elif type(columns[column]) is float or type(columns[column]) is int:
                table_to_be.append(column + "NUMERIC")
        cursor.execute("CREATE TABLE"+ db_table+ "(id INT AUTO_INCREMENT PRIMARY KEY," + table_to_be.join(",") + ")")

    # def save(self, table_name: str, columns: List) -> None:
    #     cursor = self.connection.cursor()
    #     seq_values = [i for i in columns].join(",")
    #     query = "INSERT into" + table_name + "(" + seq_values + "VALUES (" + "%s,"*len(columns) + ")"
    #
    #     for station in stations:
    #         cursor.execute(query, (
    #             station.id,
    #             station.name,
    #             station.address,
    #             station.position.lat,
    #             station.position.lon,
    #             station.city,
    #             station.slots,
    #             station.bikes,
    #             station.dt.isoformat()
    #         ))
    #
    #     cursor.close()
    #
    # def list(self):
    #     cursor = self.connection.cursor()
    #     query = "SELECT station_id, name, address, lat, lon, city, slots, bikes, timestamp from station"
    #     cursor.execute(query)
    #
    #     stations = []
    #     for station_id, name, address, lat, lon, city, slots, bikes, timestamp in cursor:
    #         stations.append(Station(
    #             station_id,
    #             name,
    #             address, bikes, slots, city,
    #             Position(lat, lon),
    #             datetime.fromisoformat(timestamp)
    #         ))
    #
    #     cursor.close()
    #
    #     return stations