import sys
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QDateEdit
from PyQt5.QtGui import qRgb, qRed, qGreen, qBlue
import random
from PyQt5 import QtCore, QtGui, QtWidgets

WORDS = []
BTN_COLOR = ''
BTN_WRONG_COLOR = '#474A51'
BTN_GOOD_COLOR = '#7CFC00'
MAIN_FILE = 'data.txt'
alph = ['АБВГДЕЁЖЗИЙКЛ','МНОПРСТУФХЦЧШ','ЩЪЫЬЭЮЯ']

def refresh_words():
    f_text = open(MAIN_FILE, 'r', encoding='utf-8')
    buffer = f_text.readlines()
    n = int(buffer[0])
    ind = 1
    for i in range(n):
        word = buffer[ind].strip()
        ind += 1
        k = int(buffer[ind])
        ind += 1
        info = ''
        for j in range(k):
            info += buffer[ind]
            ind += 1
        WORDS.append((word, info))
    f_text.close()

refresh_words()

class W2(QMainWindow): # Window add New Word
    def __init__(self):
        super().__init__()
        #uic.loadUi('file_2.ui', self)
        self.setupUi(self)
        self.add_tip.clicked.connect(self.add_new_word)

    def add_new_word(self): # Add new word
        name = self.name_word.text()
        tip = self.your_tip.toPlainText()
        file = open(MAIN_FILE, 'r', encoding='utf-8')
        all = file.readlines()
        all[0] = str(int(all[0].strip()) + 1) + '\n'
        all.append('\n' + name + '\n')
        all.append(str(len(tip.split('\n'))) + '\n')
        all.append(str(tip))
        file.close()
        file = open(MAIN_FILE, 'w', encoding='utf-8')
        for i in all:
            file.write(i)
        file.close()
        self.close()
        WORDS = []
        refresh_words()

    def setupUi(self, MainWindow): # Window's design
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(245, 356)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 30, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 80, 121, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.your_tip = QtWidgets.QTextEdit(self.centralwidget)
        self.your_tip.setGeometry(QtCore.QRect(40, 100, 171, 171))
        self.your_tip.setObjectName("your_tip")
        self.name_word = QtWidgets.QLineEdit(self.centralwidget)
        self.name_word.setGeometry(QtCore.QRect(40, 50, 171, 20))
        self.name_word.setObjectName("name_word")
        self.add_tip = QtWidgets.QPushButton(self.centralwidget)
        self.add_tip.setGeometry(QtCore.QRect(60, 280, 121, 23))
        self.add_tip.setObjectName("add_tip")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 245, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow): # Translate window
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label_2.setText(_translate("MainWindow", "Загаданное слово"))

        self.label.setText(_translate("MainWindow", "Подсказка к слову"))

        self.add_tip.setText(_translate("MainWindow", "Добавить слово"))




class Game(QMainWindow): #Game Window
    def __init__(self):
        super().__init__()
        #self.setupUi(self)
        uic.loadUi('file_1.ui', self)
        #self.setStyleSheet("background-color: white;")

        self.people = ['первый', 'второй', 'третий', 'четвёртый']
        for i in self.level_btn.buttons():
            i.clicked.connect(self.change_level)
        self.btn = []
        for i in range(len(alph)):
            for j in range(len(alph[i])):
                a = QPushButton(alph[i][j], self)
                a.whatsThis = str(i) + ',' + str(j)
                a.resize(20, 20)
                a.move(200 + 22 * j, 25 * i + 135)
                a.clicked.connect(self.func)
                #a.setStyleSheet("background-color: red;")
                self.btn.append(a)

        for i in self.cnt_players.buttons():
            i.clicked.connect(self.change_cnt_players)

        self.radioButton.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.restart.clicked.connect(self.new_word)
        self.main_add_word.clicked.connect(self.open_new_window)
        self.cnt_players = 2
        self.now_word = ''
        self.ans = ''
        self.btn_show = []
        self.now_bad = 0
        self.level = 15
        self.now_hod = 0
        self.stop_game = False
        self.new_word()

    def func(self): # Use button
        if not self.stop_game:
            self.sender().setStyleSheet("background-color: " + BTN_WRONG_COLOR)

        if not self.stop_game:
            now = self.sender()
            if now.text().upper() in self.now_word.upper():
                for i in range(len(self.btn_show)):
                    if now.text().upper() in self.btn_show[i].whatsThis.upper():
                        self.btn_show[i].setText(now.text().upper())
                        self.btn_show[i].setStyleSheet("background-color: " + BTN_GOOD_COLOR)
            else:
                self.now_bad += 1
                self.now_hod += 1
                self.now_hod %= self.cnt_players

            self.check_lost()
            self.update_tracker()
            self.check_win()

            if not self.stop_game:
                self.game_status.setText('Ходит ' + self.people[self.now_hod] + ' игрок')

    def change_cnt_players(self): # Change count users
        a = self.sender()
        self.cnt_players = int(a.whatsThis())

    def change_level(self): # Change level
        self.level = int(self.sender().whatsThis())
        self.death.setMaximum(self.level)
        self.update_tracker()

    def new_word(self): # Change word
        for i in range(len(self.btn_show)):
            self.btn_show[i].deleteLater()
        self.btn_show = []
        word = random.choice(WORDS)
        self.now_word = word[0].upper()
        self.help_info = word[1].upper()
        self.ans = '*' * len(self.now_word)
        for i in range(len(self.ans)):
            a = QPushButton('*', self)
            a.whatsThis = self.now_word[i]
            a.resize(20, 20)
            a.move(200 + 20 * i, 100)
            a.show()
            self.btn_show.append(a)
        self.game_status.setText('Ходит ' + self.people[self.now_hod] + ' игрок')
        self.now_bad = 0
        self.stop_game = False
        self.update_tracker()
        self.help_window.setText(self.help_info)
        for i in range(len(self.btn_show)):
            self.btn_show[i].setStyleSheet("background-color: ")
        for i in self.btn:
            i.setStyleSheet("background-color: " + BTN_COLOR)

    def check_lost(self): # Check lose
       if self.now_bad >= self.level:
            self.game_status.setText('Увы, но никто не отгадал слово!')
            self.stop_game = True

    def check_win(self): # Check win
        flag = True
        for i in self.btn_show:
            if i.text() == '*':
                flag = False
        if flag:
            self.game_status.setText(self.people[self.now_hod][0].upper() + self.people[self.now_hod][2:] + ' игрок отгадал слово!')
            self.stop_game = True

    def update_tracker(self): # Update Progressbar
        self.death.setMaximum(self.level)
        self.death.setValue(self.now_bad)

    def open_new_window(self): # Open window add new word
        self.w1 = W2()
        self.w1.show()

    def setupUi(self, MainWindow): # Design main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(697, 379)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.death = QtWidgets.QProgressBar(self.centralwidget)
        self.death.setGeometry(QtCore.QRect(100, 30, 581, 21))
        self.death.setMouseTracking(False)
        self.death.setMinimum(0)
        self.death.setProperty("value", 0)
        self.death.setTextVisible(False)
        self.death.setObjectName("death")
        self.restart = QtWidgets.QPushButton(self.centralwidget)
        self.restart.setGeometry(QtCore.QRect(10, 30, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.restart.setFont(font)
        self.restart.setObjectName("restart")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(530, 120, 141, 94))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.level_btn = QtWidgets.QButtonGroup(MainWindow)
        self.level_btn.setObjectName("level_btn")
        self.level_btn.addButton(self.radioButton)
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.level_btn.addButton(self.radioButton_2)
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.level_btn.addButton(self.radioButton_3)
        self.verticalLayout.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.level_btn.addButton(self.radioButton_4)
        self.verticalLayout.addWidget(self.radioButton_4)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, 100, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 300, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.game_status = QtWidgets.QLabel(self.centralwidget)
        self.game_status.setGeometry(QtCore.QRect(10, 310, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.game_status.setFont(font)
        self.game_status.setObjectName("game_status")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.help_window = QtWidgets.QTextBrowser(self.centralwidget)
        self.help_window.setGeometry(QtCore.QRect(10, 110, 161, 161))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.help_window.setFont(font)
        self.help_window.setObjectName("help_window")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(530, 250, 141, 88))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton_7 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.radioButton_7.setFont(font)
        self.radioButton_7.setObjectName("radioButton_7")
        self.cnt_players = QtWidgets.QButtonGroup(MainWindow)
        self.cnt_players.setObjectName("cnt_players")
        self.cnt_players.addButton(self.radioButton_7)
        self.gridLayout.addWidget(self.radioButton_7, 2, 0, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setObjectName("radioButton_5")
        self.cnt_players.addButton(self.radioButton_5)
        self.gridLayout.addWidget(self.radioButton_5, 0, 0, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.radioButton_6.setFont(font)
        self.radioButton_6.setObjectName("radioButton_6")
        self.cnt_players.addButton(self.radioButton_6)
        self.gridLayout.addWidget(self.radioButton_6, 1, 0, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.radioButton_8.setFont(font)
        self.radioButton_8.setObjectName("radioButton_8")
        self.cnt_players.addButton(self.radioButton_8)
        self.gridLayout.addWidget(self.radioButton_8, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(530, 230, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 697, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow): # Translate window
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Игра: Отгадай слово", "Игра: Отгадай слово"))

        self.restart.setText(_translate("MainWindow", "RESTART"))

        self.radioButton.setWhatsThis(_translate("MainWindow", "15"))

        self.radioButton.setText(_translate("MainWindow", "Лёгкий"))

        self.radioButton_2.setWhatsThis(_translate("MainWindow", "12"))

        self.radioButton_2.setText(_translate("MainWindow", "Средний"))

        self.radioButton_3.setWhatsThis(_translate("MainWindow", "8"))

        self.radioButton_3.setText(_translate("MainWindow", "Сложный"))

        self.radioButton_4.setWhatsThis(_translate("MainWindow", "6"))

        self.radioButton_4.setText(_translate("MainWindow", "Непроходимый"))

        self.label.setText(_translate("MainWindow", "Уровень сложности"))

        self.label_2.setText(_translate("MainWindow", "Статус игры:"))

        self.game_status.setText(_translate("MainWindow", "Выберите букву!"))

        self.label_3.setText(_translate("MainWindow", "Подсказка к слову:"))

        self.radioButton_7.setWhatsThis(_translate("MainWindow", "3"))

        self.radioButton_7.setText(_translate("MainWindow", "Три игрока"))

        self.radioButton_5.setWhatsThis(_translate("MainWindow", "1"))

        self.radioButton_5.setText(_translate("MainWindow", "Один игрок"))

        self.radioButton_6.setWhatsThis(_translate("MainWindow", "2"))

        self.radioButton_6.setText(_translate("MainWindow", "Два игрока"))

        self.radioButton_8.setWhatsThis(_translate("MainWindow", "4"))

        self.radioButton_8.setText(_translate("MainWindow", "Четыре игрока"))

        self.label_4.setText(_translate("MainWindow", "Количество игроков"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec())