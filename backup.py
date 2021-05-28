import os
from datetime import datetime
import pipes
from saver import MySQLManager


class Backup:

    def __init__(self, saver: MySQLManager, backup_path: str):
        self.DB_HOST = saver.connection.server_host
        self.DB_USER = saver.connection.user
        self.DB_PASSWORD = saver.connection._password
        self.BACKUP_PATH = backup_path
        self.DB_NAME = saver.connection.database
        self.CURSOR = saver.connection.cursor()

    def set_backup(self):
        # Getting current timestamp to create a separate backup folder
        today = "MySQL_" + datetime.now().strftime("%Y%m%d%H%M%S")
        today_backup = self.BACKUP_PATH + '/' + today

        # Check if backup folder already exists in the directory or not.
        try:
            os.stat(today_backup)
        except:
            os.mkdir(today_backup)

        cursor = self.CURSOR
        cursor.execute('show tables')
        f = cursor.fetchall()
        for table in f:
            for data in table:
                dump_command = "mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p" + self.DB_PASSWORD + " " + \
                               self.DB_NAME + ' ' + data + ' ' + " > " + pipes.quote(today_backup) + "/" + self.DB_NAME + ".sql"
                os.system(dump_command)
        zip_command = "gzip " + pipes.quote(today_backup) + "/" + self.DB_NAME + ".sql"
        os.system(zip_command)
        cursor.close()
