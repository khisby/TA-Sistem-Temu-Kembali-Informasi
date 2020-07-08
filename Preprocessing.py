import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk

try:
	nltk.data.find('tokenizers/punkt')
except LookupError:
	nltk.download('punkt')


from bs4 import BeautifulSoup
import csv
import pandas as pd

class Preprocessing(QtCore.QThread):
    update_progressbar = pyqtSignal(float)

    def __init__(self, parent=None):
        super(Preprocessing,self).__init__(parent)

    def run(self):
        i = 1
        status = True
        while status:
            df = pd.read_csv('data.csv', sep=",")

            data = list(df["indonesia"].astype(str).str.lower())
            kd = []
            i = 1
            for d in data:
                # StopWordRemover
                factory = StopWordRemoverFactory()
                stopword = factory.create_stop_word_remover()

                # Tokenize
                stop = nltk.tokenize.word_tokenize(stopword.remove(str(d)))

                # Stemmer
                factory = StemmerFactory()
                stemmer = factory.create_stemmer()
                katadasar = stemmer.stem(str(stop))

                kd.append(katadasar)
                self.update_progressbar.emit(i + 1)
                i = i + 1

            no = 0
            with open('post-preprocessing.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(["teks"])
                for d in kd:
                    spamwriter.writerow([kd[no]])
                    no = no + 1

            status = False