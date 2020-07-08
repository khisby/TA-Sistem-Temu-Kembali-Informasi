# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'desain.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from Scraping import *
from Preprocessing import *
import os
from urllib.request import urlopen
import pandas as pd
from operator import itemgetter
from math import log
from shutil import copyfile

class Ui_mainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_mainWindow, self).__init__(parent)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(807, 635)
        mainWindow.setWindowOpacity(5.0)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnLoadDataHadits = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadDataHadits.setGeometry(QtCore.QRect(190, 110, 161, 23))
        self.btnLoadDataHadits.setObjectName("btnLoadDataHadits")
        self.btnLihatDataHadits = QtWidgets.QPushButton(self.centralwidget)
        self.btnLihatDataHadits.setGeometry(QtCore.QRect(360, 110, 75, 23))
        self.btnLihatDataHadits.setObjectName("btnLihatDataHadits")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 101, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 160, 161, 23))
        self.pushButton.setObjectName("pushButton")
        self.btnLihatDataPreprocessing = QtWidgets.QPushButton(self.centralwidget)
        self.btnLihatDataPreprocessing.setGeometry(QtCore.QRect(320, 160, 75, 23))
        self.btnLihatDataPreprocessing.setObjectName("btnLihatDataPreprocessing")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_4.setObjectName("label_4")
        self.leQuery = QtWidgets.QLineEdit(self.centralwidget)
        self.leQuery.setGeometry(QtCore.QRect(150, 220, 251, 20))
        self.leQuery.setObjectName("leQuery")
        self.btnCari = QtWidgets.QPushButton(self.centralwidget)
        self.btnCari.setGeometry(QtCore.QRect(410, 220, 75, 23))
        self.btnCari.setObjectName("btnCari")
        self.pteHasil = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pteHasil.setGeometry(QtCore.QRect(150, 290, 591, 221))
        self.pteHasil.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.pteHasil.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.pteHasil.setObjectName("pteHasil")
        self.pbLoading = QtWidgets.QProgressBar(self.centralwidget)
        self.pbLoading.setGeometry(QtCore.QRect(10, 570, 791, 23))
        self.pbLoading.setProperty("value", 24)
        self.pbLoading.setObjectName("pbLoading")
        self.leAngka = QtWidgets.QLineEdit(self.centralwidget)
        self.leAngka.setGeometry(QtCore.QRect(150, 110, 31, 20))
        self.leAngka.setObjectName("leAngka")
        self.btnDefault = QtWidgets.QPushButton(self.centralwidget)
        self.btnDefault.setGeometry(QtCore.QRect(590, 220, 150, 23))
        self.btnDefault.setObjectName("btnDefault")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 21))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        self.pbLoading.setValue(0)


        self.btnLoadDataHadits.clicked.connect(self.prosesScraping)
        self.btnLihatDataHadits.clicked.connect(self.loadDataHadits)
        self.btnLihatDataPreprocessing.clicked.connect(self.loadDataPreprocessing)
        self.pushButton.clicked.connect(self.loadPreprocessing)
        self.btnCari.clicked.connect(self.queryProcess)
        self.btnDefault.clicked.connect(self.setDefaultDataset)

    def setDefaultDataset(self):
        copyfile('data_default.csv', 'data.csv')
        copyfile('post-preprocessing_defaut.csv', 'post-preprocessing.csv')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText('Berhasil meload dataset default')
        msg.setWindowTitle("Sucess")
        msg.exec()

    def queryProcess(self):
        if self.leQuery.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Masukkan Query terlebih dahulu!')
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            self.query = self.leQuery.text()
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
            if len(JumlahWeight) > 20 :
                tampil = 20
            else:
                tampil = len(JumlahWeight)
            self.teks = ""
            for i in range(0, tampil):
                # self.teks = self.teks + df['judul'][JumlahWeight[i][0]]
                self.teks = self.teks + str(i + 1) + str('. ') + str(df['judul'][JumlahWeight[i][0]]) + " | " + str(JumlahWeight[i][1]) + "\n"
                # self.text = self.text + str(i)
            # self.text = self.text + str("okay")
            # print(self.teks)
            self.pteHasil.setPlainText(self.teks)

    def prosesScraping(self):
        if self.internet_on() == True:
            if self.leAngka.text() == '' :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Masukkan jumlah data yang ingin diambil!')
                msg.setWindowTitle("Error")
                msg.exec()
            else:
                self.jumlah = int(self.leAngka.text())
                self.pbLoading.setMinimum(1)
                self.pbLoading.setMaximum(self.jumlah)
                self.btnCari.setDisabled(True)
                self.btnLihatDataHadits.setDisabled(True)
                self.btnLihatDataPreprocessing.setDisabled(True)
                self.btnLoadDataHadits.setDisabled(True)
                self.pushButton.setDisabled(True)
                self.btnDefault.setDisabled(True)
                self.threadclass = Scraping(self.jumlah)
                self.threadclass.start()
                self.threadclass.update_progressbar.connect(self.update_progressbar)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Harus ada koneksi internet!')
            msg.setWindowTitle("Error")
            msg.exec()

    def loadPreprocessing(self):
        if os.path.exists("data.csv"):
            df = pd.read_csv('data.csv', sep=",")
            df = pd.DataFrame(df)
            self.jumlah = df.shape[0]
            self.pbLoading.setMinimum(1)
            self.pbLoading.setMaximum(self.jumlah)
            self.btnCari.setDisabled(True)
            self.btnLihatDataHadits.setDisabled(True)
            self.btnLihatDataPreprocessing.setDisabled(True)
            self.btnLoadDataHadits.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.btnDefault.setDisabled(True)
            self.threadclass = Preprocessing()
            self.threadclass.start()
            self.threadclass.update_progressbar.connect(self.update_progressbar)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Tidak ada file data.csv. Silahkan proses scraping dulu!')
            msg.setWindowTitle("Error")
            msg.exec()

    def update_progressbar(self, val):
        self.pbLoading.setValue(val)
        if val < self.jumlah:
            self.btnCari.setDisabled(True)
            self.btnLihatDataHadits.setDisabled(True)
            self.btnLihatDataPreprocessing.setDisabled(True)
            self.btnLoadDataHadits.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.btnDefault.setDisabled(True)

        else:
            self.btnCari.setDisabled(False)
            self.btnLihatDataHadits.setDisabled(False)
            self.btnLihatDataPreprocessing.setDisabled(False)
            self.btnLoadDataHadits.setDisabled(False)
            self.pushButton.setDisabled(False)
            self.btnDefault.setDisabled(False)

    def loadDataHadits(self):
        if os.path.exists("data.csv"):
            os.system("start EXCEL.EXE data.csv")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Tidak ada file data.csv. Silahkan isi jumlah dan klik Load Data!')
            msg.setWindowTitle("Error")
            msg.exec()

    def loadDataPreprocessing(self):
        if os.path.exists("post-preprocessing.csv"):
            os.system("start EXCEL.EXE post-preprocessing.csv")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Tidak ada file post-preprocessing.csv. proses pre-processing dulu!')
            msg.setWindowTitle("Error")
            msg.exec()

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Khisoft Hadits - Khisoft 2020"))
        self.btnLoadDataHadits.setText(_translate("mainWindow", "Load Data"))
        self.btnLihatDataHadits.setText(_translate("mainWindow", "Lihat Data"))
        self.label.setText(_translate("mainWindow", "Data Hadits"))
        self.label_2.setText(_translate("mainWindow", "<html><head/><body><p>Khisoft Hadits</p></body></html>"))
        self.label_3.setText(_translate("mainWindow", "Preprocessing"))
        self.pushButton.setText(_translate("mainWindow", "Proses"))
        self.btnLihatDataPreprocessing.setText(_translate("mainWindow", "Lihat Data"))
        self.label_4.setText(_translate("mainWindow", "Masukkan Query"))
        self.btnCari.setText(_translate("mainWindow", "Cari"))
        self.btnDefault.setText(_translate("mainWindow", "Load Default Dataset"))

    def internet_on(self):
        try:
            response = urlopen('https://www.google.com/', timeout=10)
            return True
        except:
            return False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
