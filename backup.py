import sys
import pyodbc
import os
import datetime
import config
from os.path import join
import win32com.shell.shell as shell

current_date = datetime.date.today().strftime("%Y-%m-%d")

def make_backup():
    backup_file = f"D:\\DB_Backup\\Backup_Compta_{current_date}.bak"
    conn_info = "DRIVER={SQL Server};SERVER=%s;DATABASE=master;UID=%s;PWD=%s" % (config.login["SERVER"],
                                                                                 config.login["USER"],
                                                                                 config.login["PASS"])
    cnct_str = pyodbc.connect(conn_info, autocommit=True)
    cur = cnct_str.cursor()
    cur.execute(
        """BACKUP DATABASE [%s] TO  DISK = N'%s' WITH NOFORMAT, NOINIT,  
        NAME = N'%s-Full Database Backup', SKIP, NOREWIND, NOUNLOAD,  STATS = 10""" % (config.login["DATABASE"],
                                                                                       backup_file,
                                                                                       config.login["DATABASE"]))
    while cur.nextset():
        pass
    print("make_backup completed successfully")

def restore_backup(filename, db_name):
    filepath = f"D:\\DB_Backup\\{filename}"
    print(filepath)
    conn_info = "DRIVER={SQL Server};SERVER=%s;DATABASE=master;UID=%s;PWD=%s" % (config.login["SERVER"],
                                                                                 config.login["USER"],
                                                                                 config.login["PASS"])
    cnct_str = pyodbc.connect(conn_info, autocommit=True)
    cur = cnct_str.cursor()
    cur.execute(
        """RESTORE DATABASE [%s] FROM  DISK = N'%s' WITH  FILE = 1, NOUNLOAD, REPLACE, STATS = 5""" % (db_name, filepath))
    while cur.nextset():
        pass
    print("restore_backup completed successfully")

if "-h" in sys.argv:
    with open("help.txt", "r") as help:
        for line in help:
            print(line)
elif len(sys.argv) > 1:
    for cmdarg in sys.argv[1:]:
        if cmdarg == "-b":
            make_backup()
            print("Backup successful. Exiting...\n\n")
        elif cmdarg == "-r":
            filename = f"Backup_Compta_{current_date}.bak"  # Corrected the string formatting
            db_name = "CASA_COMPTA"
            restore_backup(filename, db_name)
            print("Restore backup successful. Exiting...")
        else:
            print("Invalid arguments. Please use 'python backup.py -h' for help.\n")
else:
    print("Not enough arguments. Please use 'python backup.py -h' for help.\n")