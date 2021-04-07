import sys
import Dados
import Database


def main():
    if len(sys.argv) < 6:
        help()
    else:
        dados = Dados.Dados(
            sys.argv[1], sys.argv[6])

        imageListJson = dados.requestImageList()
        dados.downloadImage(imageListJson)
        dados.writeCsv()

        database = Database.Database(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[1], sys.argv[6])

        database.createDatabase()
        database.changeDB()
        database.createTable()
        database.insertData()

        print('Done')

def help():
    print('''
        Este script necessita de 5 argumentos sendo eles na seguinte ordem.
        
        Caminho: onde as imagens deverão ser guardadas após o download;
        host: endereço do banco de dados;
        user: usuário do banco de dados;
        password: senha do banco de dados;
        database: nome do banco de dados;
        imagens: número de imagens que o script irá trazer.

        O script criará um banco de dados e uma tabela. Ele também irá popular ela com os dados recebidos da plataforma ISIIC.
        ''')


if __name__ == '__main__':
    main()
