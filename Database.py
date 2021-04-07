import mysql.connector
import base64
import csv
import sys

class Database(object):
    def __init__(self, host, user, password, database, path, images):
        self.path = path
        self.images = int(images)
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.mydb = mysql.connector.connect(
            host= host,
            user= user,
            password= password
        )
        self.cursor = self.mydb.cursor()


    def progress_bar(self, value, max, barsize):
        chars = int(value * barsize / float(max))
        numero = max - value
        percent = int((numero * 100) / max)
        percent = 100 - percent
        sys.stdout.write("#" * chars)
        sys.stdout.write(" " * (barsize - chars + 2))
        if value >= max:
            sys.stdout.write("Done. \n\n")
            print()
        else:
            sys.stdout.write("[%3i%%]\r" % percent)
            sys.stdout.flush()

    def createDatabase(self):
        query = 'CREATE DATABASE IF NOT EXISTS imagens_melanoma;'
        self.cursor.execute(query)
        self.cursor.close()
        self.mydb.close()

    def changeDB(self):
        self.mydb = mysql.connector.connect(
            host= self.host,
            user= self.user,
            password= self.password,
            database= self.database
        )
        self.cursor = self.mydb.cursor()

    def createTable(self):
        query = "CREATE TABLE IF NOT EXISTS `tabela_imagens` (`id` varchar(50) NOT NULL, `name` varchar(50) NOT NULL, `benign_malignant` varchar(25) NOT NULL, `diagnosis` varchar(25) NOT NULL, `imagem` longblob NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;"
        self.cursor.execute(query)

    def insertData(self):
        cont = 0
        with open(self.path + '\\' + 'melanoma_dados.csv') as csv_file:

             csv_reader = csv.DictReader(
             csv_file, fieldnames=["id", "name", "benign_malignant", "diagnosis"])

             csv_reader.__next__()

             for row in csv_reader:
                 cont += 1
                 self.progress_bar(cont, self.images, 50)
                 with open(self.path + "\\" + row["name"] + '.jpg', "rb") as image:
                      imagem = base64.b64encode(image.read())
                      self.cursor.execute("INSERT INTO tabela_imagens (id, name, benign_malignant, diagnosis, imagem) VALUES (%s, %s, %s, %s, %s)",
                       (row["id"], row["name"], row["benign_malignant"], row["diagnosis"], imagem))
        self.cursor.close()
        self.mydb.commit()
        self.mydb.close()