import requests
import urllib.request as urlRequest
import csv
import sys


class Dados(object):
    def __init__(self):
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

    def requestImageList(self, images):
        req = requests.get('https://isic-archive.com/api/v1/image?limit=%s&offset=0&sort=name' % images)
        return req.json()
    
    def requestImageSegmentationId(self, id):
        req = requests.get('https://isic-archive.com/api/v1/segmentation?imageId=%s' % (id))
        req = req.json()
        for imageExpert in req:
            if imageExpert['skill'] == 'expert':
                return imageExpert
    
    def downloadSegmentation(self, imageListJson, path, images):
        cont = 0
        for imageData in imageListJson:
            segmentationId = self.requestImageSegmentationId(imageData['_id'])
            urlRequest.urlretrieve('https://isic-archive.com/api/v1/segmentation/%s/mask' % (segmentationId['_id']), path + '\\' + imageData['name'] + '.png')
            cont+= 1
            self.progress_bar(cont, images, 40)

    def downloadImage(self, imageListJson, path, images):
        cont = 0
        for imageData in imageListJson:
            urlRequest.urlretrieve('https://isic-archive.com/api/v1/image/%s/download' % imageData['_id'], path + '\\' + imageData['name'] + '.jpg')
            cont+= 1
            self.progress_bar(cont, images, 40)
            self.idImage.append(imageData['_id'])
    
    def requestImageData(self, idImage):
        req = requests.get('https://isic-archive.com/api/v1/image/%s' % idImage)
        return req.json()

    def writeCsv(self, path):
        with open(path + '\\' + 'melanoma_dados.csv', 'w', newline='') as csv_file:
            fieldnames = ["id", "name", "benign_malignant", "diagnosis"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for id in self.idImage:
                imageData = self.requestImageData(id)
                writer.writerow({"id": id, "name": imageData['name'], "benign_malignant": imageData['meta']['clinical']['benign_malignant'], "diagnosis": imageData['meta']['clinical']['diagnosis']})