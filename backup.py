import os
from datetime import datetime
import pipes

import MySQLdb

from saver import MySQLManager


class Backup:

    def __init__(self, saver: MySQLManager, backup_path: str):
        self.DB_HOST = saver.connection.server_host
        self.DB_USER = saver.connection.user
        self.DB_PASSWORD = saver.connection._password
        self.BACKUP_PATH = backup_path

    def set_backup(self, db_name: str):
        # Getting current timestamp to create the separate backup folder
        today = "MySQL_" + datetime.now().strftime("%Y%m%d%H%M%S")
        today_backup = self.BACKUP_PATH + '/' + today

        # Checking if backup folder already exists or not.
        # If not exists will create it.
        try:
            os.stat(today_backup)
        except:
            os.mkdir(today_backup)

        # Connect the database, if fails yields an exception
        try:
            db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, db_name, connect_timeout=2)
            cursor = db.cursor()
        except Exception:
            print("Failed to connect to the database")

        cursor.execute('show tables')
        f = cursor.fetchall()
        for table in f:
            for data in table:
                dump_command = "mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p" + self.DB_PASSWORD + " " + \
                               db_name + ' ' + data + ' ' + " > " + pipes.quote(today_backup) + "/" + db_name + ".sql"
                os.system(dump_command)
        zip_command = "gzip " + pipes.quote(today_backup) + "/" + db_name + ".sql"
        os.system(zip_command)
        cursor.close()
        db.close()
