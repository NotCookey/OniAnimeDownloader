import os
import asyncio
import aiohttp
import requests
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QPixmap
from webbrowser import open_new
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

class AnimeWrapper:
    def __init__(self):
        self.search_link="https://gogoanime.pe//search.html?keyword={}"
        self.anime_movie="https://gogoanime.pe/anime-movies.html?aph=&page={}"

    async def get_response(self,query):
        async with aiohttp.ClientSession() as Session:
            async with Session.get(query) as response:
                return {"status":response.status,"content":await response.read()}

    def search_anime(self,query):
        start_loop=asyncio.get_event_loop()
        response=start_loop.run_until_complete(self.get_response(self.search_link.format(query)))

        search_results=[]

        if (response["status"]==200):
            content=BeautifulSoup(response["content"].decode(sys.stdout.encoding,errors='replace'),"html.parser")
            result_page=content.find("div",class_="last_episodes").find("ul",class_="items").find_all("li")
            for anime in result_page:
                anime_id=anime.find("p",class_="name").a.get("href")
                anime_title=anime.find("p",class_="name").text
                anime_release=anime.find("p",class_="released").text.strip()
                image_link=anime.find("div",class_="img").img.get("src")

                search_results.append({anime_title:{"id":anime_id,"date":anime_release,"image":image_link}})

            return search_results
        
        elif (response["status"]!=200):
            print(f"HTTP Response : {response['status']}")
        
        start_loop.close()

    def get_details(self,anime_id):
        start_loop=asyncio.get_event_loop()
        response=start_loop.run_until_complete(self.get_response("https://gogoanime.pe{}".format(anime_id)))

        if (response["status"]==200):
            content=BeautifulSoup(response["content"].decode(sys.stdout.encoding,errors='replace'),"html.parser")
            
            title=content.find("div",class_="anime_info_body_bg").h1.text
            description=content.find("div",class_="anime_info_body_bg").find_all("p",class_="type")[1].text.split(":")[1].strip()
            episodes=content.find("ul",id="episode_page").li.text.strip().replace("0-","1-")
            anime_type=content.find("div",class_="anime_info_body_bg").find_all("p",class_="type")[0].a.text
            release_date=content.find("div",class_="anime_info_body_bg").find_all("p",class_="type")[3].text

            details={"title":title,"description":description,"episodes":episodes,"type":anime_type,"release":release_date}

            return details

        elif (response["status"]!=200):
            print(f"HTTP Response : {response['status']}")

        start_loop.stop()

    def download(self,anime_id,episode):
        start_loop=asyncio.get_event_loop()
        response=start_loop.run_until_complete(self.get_response("https://www1.gogoanime.ai{}".format(anime_id)))

        if (response["status"]==200):
            content=BeautifulSoup(response["content"].decode(sys.stdout.encoding,errors='replace'),"html.parser")
            dlpage_response=start_loop.run_until_complete(self.get_response("https://gogoanime.pe/{}-episode-{}".format(anime_id.replace("/category/",""),episode)))
            dl_content=BeautifulSoup(dlpage_response["content"].decode(sys.stdout.encoding,errors='replace'),"html.parser")

            links=dl_content.find("div",class_="favorites_book").find("li",class_="dowloads").a.get("href")
            return links

        elif (response["status"]!=200):
            print(f"HTTP Response : {response['status']}")

        start_loop.stop()

    def movies_list(self):
        start_loop=asyncio.get_event_loop()
        response=start_loop.run_until_complete(self.get_response(self.anime_movie.format("1")))
        movie_list=[]

        if (response["status"]==200):
            content=BeautifulSoup(response["content"].decode(sys.stdout.encoding,errors='replace'),"html.parser")
            movies=content.find_all("p",class_="name")

            for name in movies:
                movie_list.append(name.text)
            return movie_list

        elif (response["status"]!=200):
            print(f"HTTP Response : {response['status']}")

        start_loop.stop()

class Ui_MainWindow(object):
    def __init__(self):
        self.api=AnimeWrapper()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("OniAnimeDownloader")
        MainWindow.resize(990, 595)
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 971, 571))
        self.frame.setStyleSheet("border-radius: 15px;\n"
"background-color: rgb(54, 57, 63);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.title = QtWidgets.QLabel(self.frame)
        self.title.setGeometry(QtCore.QRect(0, 0, 971, 131))
        self.title.setStyleSheet("font: 30pt \"UniSansHeavy\";\n"
"color: rgb(114, 137, 218);\n"
"text-align:center;\n"
"margin:20px;\n"
"border:2px solid transparent;\n"
"background-color: rgb(32, 34, 37);")
        self.title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.title.setScaledContents(True)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.title.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 130, 241, 181))
        self.frame_2.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(280, 230, 671, 81))
        self.frame_3.setStyleSheet("background-color: rgb(47, 49, 54);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.animename = QtWidgets.QLabel(self.frame_3)
        self.animename.setGeometry(QtCore.QRect(20, 10, 631, 31))
        self.animename.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"UniSansSemiBold\";")
        self.animename.setObjectName("animename")
        self.animename_3 = QtWidgets.QLabel(self.frame_3)
        self.animename_3.setGeometry(QtCore.QRect(20, 40, 631, 31))
        self.animename_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"UniSansSemiBold\";")
        self.animename_3.setObjectName("animename_3")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(20, 330, 461, 181))
        self.frame_4.setStyleSheet("background-color: rgb(47, 49, 54);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.animename_4 = QtWidgets.QLabel(self.frame_4)
        self.animename_4.setGeometry(QtCore.QRect(20, 5, 171, 31))
        self.animename_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"UniSansSemiBold\";")
        self.animename_4.setObjectName("animename_4")
        self.textEdit = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 421, 121))
        self.textEdit.setStyleSheet("background-color: rgb(31, 32, 36);\n"
"color:white;\n"
"font: 63 12pt \"Dosis\";")
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setGeometry(QtCore.QRect(500, 330, 451, 181))
        self.frame_5.setStyleSheet("background-color: rgb(47, 49, 54);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.animename_5 = QtWidgets.QLabel(self.frame_5)
        self.animename_5.setGeometry(QtCore.QRect(20, 5, 271, 31))
        self.animename_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"UniSansSemiBold\";")
        self.animename_5.setObjectName("animename_5")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_5)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 411, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(31, 32, 36);\n"
"font: 63 12pt \"Dosis\";\n"
"border-radius:10px;\n"
"color:white;\n"
"padding-left:10px;")
        self.lineEdit.setMaxLength(1000)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.frame_5)
        self.pushButton.clicked.connect(self.download)
        self.pushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 411, 41))
        self.pushButton.setStyleSheet("font: 63 12pt \"Dosis\";\n"
"color: rgb(255, 255, 255);\n"
"border:2px solid;\n"
"border-color: rgb(85, 170, 255);\n"
"background-color: rgb(35, 35, 35);")
        self.pushButton.setObjectName("pushButton")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setGeometry(QtCore.QRect(280, 130, 671, 91))
        self.frame_6.setStyleSheet("background-color: rgb(47, 49, 54);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.animename_7 = QtWidgets.QLabel(self.frame_6)
        self.animename_7.setGeometry(QtCore.QRect(20, 5, 101, 31))
        self.animename_7.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"UniSansSemiBold\";")
        self.animename_7.setObjectName("animename_7")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_6)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 40, 421, 31))
        self.lineEdit_3.setStyleSheet("background-color: rgb(31, 32, 36);\n"
"font: 63 12pt \"Dosis\";\n"
"border-radius:10px;\n"
"color:white;\n"
"padding-left:10px;")
        self.lineEdit_3.setMaxLength(1000)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_6)
        self.pushButton_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.clicked.connect(self.search)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 40, 201, 31))
        self.pushButton_3.setStyleSheet("font: 63 12pt \"Dosis\";\n"
"color: rgb(255, 255, 255);\n"
"border:2px solid;\n"
"border-radius:7px;\n"
"border-color: rgb(85, 170, 255);\n"
"background-color: rgb(35, 35, 35);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.clicked.connect(lambda:exit())
        self.pushButton_4.setGeometry(QtCore.QRect(200, 523, 281, 31))
        self.pushButton_4.setStyleSheet("font: 63 12pt \"Dosis\";\n"
"color: rgb(255, 255, 255);\n"
"border:2px solid;\n"
"border-radius:7px;\n"
"border-color: tomato;\n"
"background-color: rgb(35, 35, 35);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setGeometry(QtCore.QRect(500, 523, 281, 31))
        self.pushButton_5.setStyleSheet("font: 63 12pt \"Dosis\";\n"
"color: rgb(255, 255, 255);\n"
"border:2px solid;\n"
"border-radius:7px;\n"
"border-color: yellow;\n"
"background-color: rgb(35, 35, 35);")
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def search(self):
        self.pushButton_3.setEnabled(False)
        self.download_id=None
        if self.lineEdit_3.text():
            content=self.api.search_anime(self.lineEdit_3.text())[0]
            for key in content:
                img=content[key]["image"]
                self.download_id=content[key]["id"]
                desc=self.api.get_details(content[key]["id"])
            img_data=requests.get(url=img)
            file = open("avatar.jpg", "wb")
            file.write(img_data.content)
            file.close()
            self.frame_2.setStyleSheet("background-image:url('avatar.jpg');background-position:center;background-repeat:no-repeat;")
            self.animename.setText(f"Name : {desc['title']}")
            self.animename_3.setText(f"Episodes : {desc['episodes']}")
            self.textEdit.setPlainText(desc["description"])
        self.pushButton_3.setEnabled(True)

    def download(self):
        if self.lineEdit.text() and self.download_id:
            url=self.api.download(self.download_id, self.lineEdit.text())
            open_new(url=url)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.title.setText(_translate("MainWindow", "OniAnimeDownloader"))
        self.animename.setText(_translate("MainWindow", "Name :"))
        self.animename_3.setText(_translate("MainWindow", "Episodes :"))
        self.animename_4.setText(_translate("MainWindow", "Plot Summary :"))
        self.animename_5.setText(_translate("MainWindow", "Enter Episode Number To Download :"))
        self.pushButton.setText(_translate("MainWindow", "Download Episode"))
        self.animename_7.setText(_translate("MainWindow", "Anime Name"))
        self.pushButton_3.setText(_translate("MainWindow", "Search"))
        self.pushButton_4.setText(_translate("MainWindow", "Exit App"))
        self.pushButton_5.setText(_translate("MainWindow", "Made by : SecretsX"))

class MainWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dragPos = QtCore.QPoint()
        
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dir_ = QtCore.QDir("data")
    for file in os.listdir("data"):
        if file.endswith(".ttf"):
            font = QtGui.QFontDatabase.addApplicationFont(f"data/{file}")
            QtGui.QFontDatabase.applicationFontFamilies(font)
    window=MainWin()
    window.show()
    sys.exit(app.exec_())
