from flask import Flask, jsonify, request
import pandas as pd
from operator import itemgetter
from math import log
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
from flask_cors import CORS, cross_origin
import os


nltk.download('punkt')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return "Hallo ini adalah API untuk mengelola Khisoft Hadits!"

@app.route('/search/<string:query>', methods=['get'])
@cross_origin()
def get_task(query):
    df = pd.read_csv('data.csv', sep=",")
    dataAfter = pd.read_csv('post-preprocessing.csv', sep="|")
    data = query.split(" ")
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

    # print(termFrequency)
    # print(dokumenfrequency)
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

    tampil = 0
    if len(JumlahWeight) > 20:
        tampil = 20
    else:
        tampil = len(JumlahWeight)
    teks = []
    for i in range(0, tampil):
        # self.teks = self.teks + df['judul'][JumlahWeight[i][0]]
        teks.append([str(df['judul'][JumlahWeight[i][0]]),str(df['indonesia'][JumlahWeight[i][0]]),str(df['arab'][JumlahWeight[i][0]]), str(JumlahWeight[i][1])])
        # self.text = self.text + str(i)
    # self.text = self.text + str("okay")
    # print(self.teks)
    return jsonify({'data': teks}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
    print("App runing at port " + str(port))