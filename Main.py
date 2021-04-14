import sys
import Dados
import Database


def main():
    dados = Dados.Dados()

    images = 500

    imageListJson = dados.requestImageList(images)
    dados.downloadSegmentation(
        imageListJson, r'C:\Users\rapha\Documents\ISIIC_Download_Segmentation', images)
    dados.downloadImage(
        imageListJson, r'C:\Users\rapha\Documents\ISIC-download', images)
    dados.writeCsv(r'C:\Users\rapha\Documents\ISIC-download')

    # database = Database.Database(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[1], sys.argv[6])

    # database.createDatabase()
    # database.changeDB()
    # database.createTable()
    # database.insertData()

    print('Done')


if __name__ == '__main__':
    main()
