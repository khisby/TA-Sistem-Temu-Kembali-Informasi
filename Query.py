import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
nltk.download('punkt')
from operator import itemgetter
from math import log

from bs4 import BeautifulSoup
import csv
import pandas as pd

class Query(QtCore.QThread):
    update_progressbar = pyqtSignal(float)

    def __init__(self, parent=None, query=''):
        super(Query,self).__init__(parent)
        self.query = query

    def run(self):
        i = 1
        status = True
        while status:
            df = pd.read_csv('data.csv', sep=",")
            dataAfter = pd.read_csv('post-preprocessing.csv', sep="|")
            data = self.query.split(" ")

            # Query Kata Dasar
            querykd = []
            for d in data:
                # StopWordRemover
                factory = StopWordRemoverFactory()
                stopword = factory.create_stop_word_remover()

                # Tokenize
                stop = nltk.tokenize.word_tokenize(stopword.remove(str(d.lower())))

                # Stemmer
                factory = StemmerFactory()
                stemmer = factory.create_stemmer()
                katadasar = stemmer.stem(str(stop))

                querykd.append(katadasar)
                # print(str(i)+ str(','), end='')
                # print(d)
                # i=i+1

            # TF - DF
            termFrequency = []
            dokumenfrequency = []
            for index, term in enumerate(querykd):
                countDokumen = []
                countDokumenFrequency = 0
                for dokumen in dataAfter['teks']:
                    count = 0
                    for kata in dokumen.split(' '):
                        if kata == term:
                            count += 1
                    countDokumen.append(count)

                    if count > 0:
                        countDokumenFrequency += 1
                termFrequency.append(countDokumen)
                dokumenfrequency.append(countDokumenFrequency)

            # IDF + 1
            idfSatu = []
            jumlahDokumen = len(df)
            for i in dokumenfrequency:
                idfSatu.append(log(jumlahDokumen / (i + 1)))

            # Pembobotan TFIDF (bisa di ganti COSIM)
            weight = termFrequency[:]
            for i in range(len(weight)):
                for j in range(len(weight[i])):
                    weight[i][j] = termFrequency[i][j] * idfSatu[i]

            # Menghitung total bobot dokumen
            jumlahWeight = []
            for i in range(len(weight[0])):
                jumlahWeight.append([i, 0])

            for i in range(len(weight)):
                for j in range(len(weight[i])):
                    jumlahWeight[j][1] += weight[i][j]

            # sorting bobot dokumen tertinggi = relevan
            JumlahWeight = sorted(jumlahWeight, key=itemgetter(1), reverse=True)

            for i in range(0, 20):
                print(str(i + 1) + str('. ') + str(df['judul'][JumlahWeight[i][0]]) + " | " + str(JumlahWeight[i][1]))

            status = False