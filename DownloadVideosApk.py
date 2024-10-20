#############################################
 # @@@ Author: Ariel Araújo dos Santos @@@ #
#############################################

from PyQt5 import QtCore, QtGui, QtWidgets
from yt_dlp import YoutubeDL
from PyQt5.QtCore import QThread, pyqtSignal

#Class configurada para emitir um sinal ao final do download, notificando "Download Concluído"
class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, url, options):
        super().__init__()
        self.url = url
        self.options = options

    def run(self):
        with YoutubeDL(self.options) as ydl:
            ydl.download([self.url])
        self.progress_signal.emit("Download concluído!") #label que mostra mensagem para o usuário saber quando a música foi baixada


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(738, 313)

        #Bloqueia a maximização do app
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("#MainWindow{ background-color: #FF0000; }")

        MainWindow.setWindowIcon(QtGui.QIcon("C:/Users/Ariel/PycharmProjects/Scripts/Ytb/Img/icon.png"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, -50, 741, 381))
        self.widget.setStyleSheet("#widget{ background-color: #FF0000; }")
        self.widget.setObjectName("widget")

        
        self.btn_down = QtWidgets.QPushButton(self.widget)
        self.btn_down.setGeometry(QtCore.QRect(100, 250, 351, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.btn_down.setFont(font)
        self.btn_down.setStyleSheet("#btn_down {"
                                     " background-color: #4CAF50;"
                                     " color: white;"
                                     " border: none;"
                                     " padding: 15px 30px;"
                                     " border-radius: 8px;"
                                     " font-size: 18px;"
                                     " font-weight: bold;"
                                     " display: inline-flex;"
                                     " align-items: center;"
                                     " gap: 10px;"
                                     " cursor: pointer;"
                                     " transition: background-color 0.3s, transform 0.2s;"
                                     " text-decoration: none;"
                                     "}")
        self.btn_down.setObjectName("btn_down")

    
        self.btn_down.clicked.connect(self.download)

     
        self.rb_mp3 = QtWidgets.QRadioButton(self.widget)
        self.rb_mp3.setGeometry(QtCore.QRect(590, 240, 111, 41))
        self.rb_mp3.setStyleSheet("#rb_mp3{ color: white; }")
        self.rb_mp3.setObjectName("rb_mp3")

        self.txt_titulo = QtWidgets.QLineEdit(self.widget)
        self.txt_titulo.setGeometry(QtCore.QRect(90, 180, 371, 21))
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.txt_titulo.setFont(font)
        self.txt_titulo.setObjectName("txt_titulo")

        self.txt_link = QtWidgets.QLineEdit(self.widget)
        self.txt_link.setGeometry(QtCore.QRect(90, 140, 621, 21))
        self.txt_link.setFont(font)
        self.txt_link.setObjectName("txt_link")

        self.rb_mp4 = QtWidgets.QRadioButton(self.widget)
        self.rb_mp4.setGeometry(QtCore.QRect(590, 200, 111, 41))
        self.rb_mp4.setStyleSheet("#rb_mp4{ color: white; }")
        self.rb_mp4.setObjectName("rb_mp4")

    
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(20, 170, 71, 41))
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("#label_2{ color: white; }")
        self.label_2.setObjectName("label_2")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 140, 47, 21))
        self.label.setFont(font)
        self.label.setStyleSheet("#label{ color: white; }")
        self.label.setObjectName("label")

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(200, 70, 341, 41))
        font.setPointSize(26)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("#label_3{ color: white; }")
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #Funcao de downlaod
    def download(self):
            url = self.txt_link.text()
            titulo = self.txt_titulo.text()
            diretorio_musica = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.MusicLocation)
            #Condição para saber se mp3 foi selecionado
            if self.rb_mp3.isChecked():
                options = {
                    'format': 'bestaudio/best', 
                    'outtmpl': f"{diretorio_musica}/{titulo}.mp3",  # Salva como MP3 na pasta de Músicas
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                self.label_3.setText("Baixando...") 
                self.thread = DownloadThread(url, options)
                self.thread.progress_signal.connect(self.on_download_complete)
                self.thread.start()
            #Condição para saber se mp4 foi selecionado
            elif self.rb_mp4.isChecked():
                options = {
                    'format': 'best',
                    'outtmpl': f"{diretorio_musica}/{titulo}.mp4",  # Salva como MP4 na pasta de Músicas
                }
                self.label_3.setText("Baixando...")
                self.thread = DownloadThread(url, options)
                self.thread.progress_signal.connect(self.on_download_complete)
                self.thread.start()
    #Mudal o label para download
    def on_download_complete(self):
            self.label_3.setText("Download concluído!")  # Atualiza o texto após o download

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Download Vídeos"))
        self.btn_down.setText(_translate("MainWindow", "Download"))
        self.rb_mp3.setText(_translate("MainWindow", "MP3"))
        self.rb_mp4.setText(_translate("MainWindow", "MP4"))
        self.label_2.setText(_translate("MainWindow", "Título:"))
        self.label.setText(_translate("MainWindow", "Link:"))
        self.label_3.setText(_translate("MainWindow", "Youtube Download"))

#Inicializador
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
