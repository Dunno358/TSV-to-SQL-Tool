import mysql.connector as mariadb
import os
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

while True:
    csvpath = input("Podaj ścieżke pliku TSV: ")
    try:
        csvfile = open(f"{csvpath}",encoding="utf-8")
        print("Trwa otwieranie pliku...")
        break
    except:
        print("Nie udało się otworzyć pliku, sprawdź poprawność ścieżki i spróbuj ponownie.")
        continue

lines = csvfile.read()
lines = lines.splitlines()
del lines[0]

data = []
for line in lines:
    datatoassign = line.split("\t")
    for x in datatoassign:
        data.append(x)

for x in data: 
    index = data.index(x)
    if len(x)==0:
        data[index] = "Brak"
    if "," in x and x[0] in ["1","2","3","4","5","6","7","8","9"]:
        data[index] = x.replace(",",".")
csvfile.close()
print("Plik został wczytany!")
while True:
    try:
        table = input("Podaj nazwę tabeli do której chcesz dodać dane: ")
        colCountComm = f"SELECT count(*) FROM information_schema.columns WHERE table_name = '{table}';"
        root.execute(colCountComm)
        colCount = root.fetchall()
        colCount = colCount[0][0]
        if colCount == 0:
            print("Nie znaleziono tabeli.")
        else:
            break
    except:
        print("Nie znaleziono tabeli!")
        continue


rowsCount = len(data)//colCount

it=0
errorCounter = 0
badData = []
for x in range(rowsCount):
    sqlComm = f'INSERT INTO {table} VALUES('
    sqlComm += f'"{data[0+it]}"'
    for x in range(colCount-1):
        sqlComm+= f',"{data[x+1+it]}"'
    sqlComm += ');'

    try:
        root.execute(sqlComm)
        conn.commit()
    except:
        errorCounter += 1
        sqlComm = sqlComm.replace(f"INSERT INTO {table} VALUES(","")
        sqlComm = sqlComm.replace(');','')
        badData.append(sqlComm)

    it += colCount
    os.system('cls')
    print(f"Przetworzono {it//colCount} z {rowsCount} rekordów.")
    timeSecAll = (rowsCount - (it//colCount))//5
    timeSec = timeSecAll%60
    timeMin = timeSecAll//60
    print(f"Przewidywany czas: {timeMin}m {timeSec}s")

os.system('cls')
print(f"Zakończono dodawanie, dodano {(it//colCount)-errorCounter} z {rowsCount} rekordów.")
print(f"Pominięto {errorCounter} rekordów z powodu niewłaściwych danych:")
badDataFile = open("NotAddedRecords.txt","w",encoding='utf-8')
badDataFile.write(f"Data not added to {table}:\n")
for data in badData:
    print(data)
    print("\n")
    badDataFile.write(data+"\n")
badDataFile.close()
conn.close()
os.system('pause')