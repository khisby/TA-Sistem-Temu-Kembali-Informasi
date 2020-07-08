import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from bs4 import BeautifulSoup
import csv


class Scraping(QtCore.QThread):
    update_progressbar = pyqtSignal(float)

    def __init__(self,jumlah = 0, parent=None):
        super(Scraping,self).__init__(parent)
        self.jumlah = jumlah

    def run(self):
        i = 1
        status = True
        while status:
            if self.jumlah != 0 :
                data = []
                for i in range(0, self.jumlah):
                    url = 'https://www.hadits.id/'
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    btncontent = soup.findAll("input", {"type": "button"})
                    linkHadits = str(btncontent[0]).replace("<input onclick=\"window.location=\'/", "").replace(
                        "\'\" type=\"button\" value=\"Hadits Acak\"/>", "")
                    responseHadits = response = requests.get(url + linkHadits)
                    soupHadits = BeautifulSoup(responseHadits.text, "html.parser")
                    haditsDari = soupHadits.find(class_='hadits-about').find('h2').getText()
                    haditsJudul = soupHadits.find(class_='hadits-content').find('h1').getText()
                    haditsContent = soupHadits.find(class_='hadits-content').find_all('p')
                    teksArab = haditsContent[0].getText()
                    teksIndonesia = haditsContent[1].getText()
                    if not haditsJudul in data:
                        data.append(
                            str(str(haditsDari) + "|" + str(haditsJudul) + "|" + str(teksIndonesia) + "|" + str(
                                teksArab)))
                    self.update_progressbar.emit(i + 1)
                no = 0
                with open('data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow(["dari", "judul", "indonesia", "arab"])
                    for d in data:
                        spamwriter.writerow(data[no].split("|"))
                        no = no + 1

            status = False