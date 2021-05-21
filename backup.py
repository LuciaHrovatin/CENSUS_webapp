import os
from datetime import datetime
import pipes
from saver import MySQLManager


class Backup:

    def __init__(self, saver: MySQLManager, DB_NAME: str, BACKUP_PATH: str):
        self.DB_HOST = saver.connection.server_host
        self.DB_USER = saver.connection.user
        self.DB_PASSWORD = saver.connection._password
        self.DB_NAME = DB_NAME
        self.BACKUP_PATH = BACKUP_PATH

    # DB_USER = 'root'
    # DB_USER_PASSWORD = '_mysql_user_password_'
    # DB_NAME = '/backup/dbnameslist.txt'
    # DB_NAME = 'db_name_to_backup'
    # BACKUP_PATH = '/backup/dbbackup'

    def set_backup(self):
        # Getting current DateTime to create the separate backup folder like "20180817-123433".
        today = datetime.now().isoformat()
        for x in ["-", ":", "."]:
            today = today.replace(x, "")
        today = today.replace("T", "-")

        today_backup = self.BACKUP_PATH + '/' + today

        # Checking if backup folder already exists or not.
        # If not exists will create it.
        try:
            os.stat(today_backup)
        except:
            os.mkdir(today_backup)

        multi = 0
        if os.path.exists(self.DB_NAME):
            multi = 1
            print("Databases file found...")
            print("Starting backup of all dbs listed in file " + self.DB_NAME)
        else:
            print("Databases file not found...")
            print("Starting backup of database " + self.DB_NAME)

        # Starting actual database backup process.
        if multi:
            in_file = open(self.DB_NAME, "r")
            file_length = len(in_file.readlines())
            in_file.close()
            p = 1
            db_file = open(self.DB_NAME, "r")

            while p <= file_length:
                db = db_file.readline()  # reading database name from file
                db = db[:-1]  # deletes extra line
                dump_command = "mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p" + self.DB_PASSWORD + " " + \
                          db + " > " + pipes.quote(today_backup) + "/" + db + ".sql"
                os.system(dump_command)
                zip_command = "gzip " + pipes.quote(today_backup) + "/" + db + ".sql"
                os.system(zip_command)
                p += 1
            db_file.close()
        else:
            dump_command = "mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p " + self.DB_PASSWORD + " " + \
                           self.DB_NAME + " > " + pipes.quote(today_backup) + "/" + self.DB_NAME + ".sql"
            os.system(dump_command)
            zip_command = "gzip " + pipes.quote(today_backup) + "/" + self.DB_NAME + ".sql"
            os.system(zip_command)

        print("")
        print("Backup script completed")
        print("Your backups have been created in '" + today_backup + "' directory")
