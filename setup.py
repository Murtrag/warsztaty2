import os
import psycopg2

from configparser import ConfigParser

username = "postgres"
password = "postgres"
db_name = "mailserver"
db_server = "db"
domain = "test.pl"

current_file = os.path.realpath(__file__)
script_dir = os.path.dirname(current_file)
# username = input("Podaj nazwę urzytkownika dostępu do psql: ")
# password = input("Podaj hasło usera {} do psql: ".format(user))
# db_name = input("Podaj nazwę bazy danych jaką chcesz utworzyć dla programu: ")

# print("1. Przechodze do katalogu\n [#     ] ")
print("1. Going to catalogue [#     ] \n")
os.chdir(script_dir)
# print("2. Tworzenie venv\n [##    ] ")
# os.system("virtualenv -p python3 env")
# os.system("source /env/bin/activate")
print("3. Installing dependiences \n [##   ] ")
os.system("pip3 install -r requirements.txt")
print("4. Creating database \n [###  ] ")

con = psycopg2.connect(user=username, password=password, host=db_server)
con.autocommit = True
cur = con.cursor()
try:
    cur.execute("DROP DATABASE {};".format(db_name))
except Exception:
    pass
cur.execute("CREATE DATABASE {};".format(db_name))
con.close()
print("5. Creating tabes in database \n [##### ] ")
con = psycopg2.connect(user=username, password=password, dbname=db_name, host=db_server)
con.autocommit = True
cur = con.cursor()
cur.execute(
    """
CREATE TABLE users (
  id serial NOT NULL,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
"""
)


cur.execute(
    """
CREATE TABLE messages (
id serial NOT NULL,
title VARCHAR(255) NOT NULL,
message TEXT NOT NULL,
sender VARCHAR(255) NOT NULL,
receiver VARCHAR(255) NOT NULL,
creation_date timestamp,
PRIMARY KEY (id),
FOREIGN KEY(sender) REFERENCES users(email),
FOREIGN KEY(receiver) REFERENCES users(email)
);
"""
)
con.close()
# print("6. Finalizacja instalacji\n [######] ")
print("6. Finalizing instalation \n [######] ")
os.chdir("database")

config = ConfigParser()
config["db"] = {
    "username": username,
    "password": password,
    "db_name": db_name,
    "db_server": db_server,
    "domain": domain,
}

with open("config.ini", "w") as file:
    config.write(file)
os.chdir("..")
os.system("chmod 775 users.py message.py")
print("---------------------\n INSTALATION WENT SUCCESSFULLY \\o/")
