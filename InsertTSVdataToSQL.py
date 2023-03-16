import mysql.connector as mariadb
import os

class Data():
    def __init__(self):
        self.mode = input("Choose mode:\n1 - Add from .tsv file\n2 - Add fixed records\n: ")
        self.reqs = ['IP: ', 'database: ', 'user: ', 'password: ']
        self.user_input = []
        for x in range(len(self.reqs)):
            self.user_input.append(input(self.reqs[x]))
class SQL():
    def __init__(self):     
        try:
            print('\nConnecting to database...')
            self.conn = mariadb.connect(
                user=data.user_input[2],
                password=data.user_input[3],
                host=data.user_input[0],
                database=data.user_input[1],
                port='3306'
            )
            print('Connected!')
        except:
            print("ERROR! Can't connect to:")
            for x in range(len(data.user_input)):
                print(f"{data.reqs[x]}{data.user_input[x]}")
            exit()
        self.root = self.conn.cursor()
    def list_tables(self,database):
        self.root.execute(f'SHOW TABLES from {database}')
        tables_list = self.root.fetchall()
        tables_str = ''
        for table in tables_list:
            tables_str += f"{table[0]}\n"
        return tables_str
    def close(self):
        self.conn.close()
    def insert_tsv_to_table(self,dataToRetrieve):
        while True:
            try:
                table = input("Type name of a table you want to add in or type list tables: ")
                if table.lower() == 'list tables':
                    print(sql.list_tables(data.user_input[1]))
                else:
                    colCountComm = f"SELECT count(*) FROM information_schema.columns WHERE table_name = '{table}';"
                    sql.root.execute(colCountComm)
                    colCount = sql.root.fetchall()
                    colCount = colCount[0][0]
                    if colCount == 0:
                        print("Table not found.")
                    else:
                        break
            except:
                print("Error occured when opening table!")
                continue

        rowsCount = len(dataToRetrieve)//colCount

        it=0
        errorCounter = 0
        badData = []
        for x in range(rowsCount):
            sqlComm = f'INSERT INTO {table} VALUES('
            sqlComm += f'"{dataToRetrieve[0+it]}"'
            for x in range(colCount-1):
                sqlComm+= f',"{dataToRetrieve[x+1+it]}"'
            sqlComm += ');'

            try:
                sql.root.execute(sqlComm)
                sql.conn.commit()
            except:
                errorCounter += 1
                sqlComm = sqlComm.replace(f"INSERT INTO {table} VALUES(","")
                sqlComm = sqlComm.replace(');','')
                badData.append(sqlComm)

            it += colCount
            os.system('cls')
            print(f"Processed {it//colCount} of {rowsCount} records.")
            timeSecAll = (rowsCount - (it//colCount))//5
            timeSec = timeSecAll%60
            timeMin = timeSecAll//60
            print(f"Time left: {timeMin}m {timeSec}s")

        os.system('cls')
        print(f"\nProcessing ended, added {(it//colCount)-errorCounter} of {rowsCount} records.")
        print(f"Ignored {errorCounter} records because of bad data:")
        if errorCounter > 0:
            badDataFile = open("NotAddedRecords.txt","w",encoding='utf-8')
            badDataFile.write(f"Data not added to {table}:\n")
            for x in badData:
                print(x)
                badDataFile.write(x+"\n")
            badDataFile.close()    
            print('\nCheck queries at "NotAddedRecords.txt" and start the program as Add fixed records.\n')
    def insert_one(self,query):
        try:
            self.root.execute(query)
            self.conn.commit()
            return True
        except:
            print(f"ERROR: {query}")
            return False
class File():
    def __init__(self):
        if data.mode == '1':
            while True:
                self.tsvpath = input("Type TSV file path: ")
                print("Opening file...")
                try:
                    self.tsvfile = open(f"{self.tsvpath}",encoding="utf-8")
                    print("Success! Loading...")
                    break
                except:
                    print("File cannot be open, check path and try again.")
                    continue
            self.load()
        else:
            self.handleBadData()
    def load(self,splitlines=True):
        lines = self.tsvfile.read()

        if splitlines:
            lines = lines.splitlines()
            del lines[0]

        dataRetrieve = []
        for line in lines:
            datatoassign = line.split("\t")
            for x in datatoassign:
                dataRetrieve.append(x)

        for x in dataRetrieve: 
            index = dataRetrieve.index(x)
            if len(x)==0:
                dataRetrieve[index] = "Blank"
            if "," in x and x[0] in ["1","2","3","4","5","6","7","8","9"]:
                dataRetrieve[index] = x.replace(",",".")
        self.tsvfile.close()
        print("File loaded!")
        sql.insert_tsv_to_table(dataRetrieve)
    def handleBadData(self):
        table = input("Type the name of table you want to add to: ")
                      
        badDataFile = open(f"notAddedRecords.txt",encoding="utf-8")
        data = badDataFile.read().split("\n")
        del data[0]
        badDataFile.close()

        iteratorSuccess = 0
        iteratorFailure = 0
        failures = []
        for x in range(len(data)):
            comm = f"INSERT INTO {table} VALUES({data[0]});"
            if sql.insert_one(comm):
                iteratorSuccess += 1
            else:
                iteratorFailure += 1
                failures.append(data[0])
            del data[0]

        badDataFile = open(f"notAddedRecords.txt","w")
        for record in failures:
            badDataFile.write(record)
        badDataFile.close()

        print(f"Added {iteratorSuccess} and ignored {iteratorFailure} records. Check log above if any errors occured.")

if __name__=='__main__':
    data=Data()
    sql=SQL()
    file=File()

    sql.close()
    os.system('pause')