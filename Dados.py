import requests
import urllib.request as urlRequest
import csv
import sys


class Dados(object):
    def __init__(self, path, image):
        self.path = path
        self.image = int(image)
        self.idImage = []

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

    def requestImageList(self):
        req = requests.get('https://isic-archive.com/api/v1/image?limit=%s&offset=0&sort=name' % self.image)
        return req.json()
    
    def downloadImage(self, imageListJson):
        cont = 0
        for imageData in imageListJson:
            urlRequest.urlretrieve('https://isic-archive.com/api/v1/image/%s/download' % imageData['_id'], self.path + '\\' + imageData['name'] + '.jpg')
            cont+= 1
            self.progress_bar(cont, self.image, 40)
            self.idImage.append(imageData['_id'])
    
    def requestImageData(self, idImage):
        req = requests.get('https://isic-archive.com/api/v1/image/%s' % idImage)
        return req.json()

    def writeCsv(self):
        with open(self.path + '\\' + 'melanoma_dados.csv', 'w', newline='') as csv_file:
            fieldnames = ["id", "name", "benign_malignant", "diagnosis"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for id in self.idImage:
                imageData = self.requestImageData(id)
                writer.writerow({"id": id, "name": imageData['name'], "benign_malignant": imageData['meta']['clinical']['benign_malignant'], "diagnosis": imageData['meta']['clinical']['diagnosis']})