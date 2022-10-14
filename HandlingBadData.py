import os
import mysql.connector as mariadb
from InsertTSVdataToSQL import table

def decipher(txt):
    deciphered = ""
    for x in txt:
        index = txt.index(x)
        deciphered += chr(ord(x)-1)
    return deciphered

try:
    conn = mariadb.connect(
        user='root',
        password=decipher('Njdibmfl51'),
        host='178.183.86.202',
        database='avtsysdb',
        port='3306'
    )
except:
    print("Nie udało się nawiązać połączenia z bazą SQL.")
    exit()
root = conn.cursor()

badDataFile = open(f"notAddedRecords.txt",encoding="utf-8")
data = badDataFile.read().split("\n")
del data[0]
badDataFile.close()

for x in range(len(data)):
    comm = f"inster into {table} values({data[0]})"
    del data[0]

    