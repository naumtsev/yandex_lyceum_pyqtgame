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
alph = ['АБВГДЕЁЖЗИЙКЛ',
        'МНОПРСТУФХЦЧШ',
        'ЩЪЫЬЭЮЯ']

def add_words():
    f_text = open('data.txt', 'r', encoding='utf-8')
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

add_words()

class W2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('file_2.ui', self)
        self.add_tip.clicked.connect(self.add_new_word)

    def add_new_word(self):
        name = self.name_word.text()
        tip = self.your_tip.toPlainText()
        #print(pname)
        #print(ptip)
        #print(pname, ptip)

        file = open('data.txt', 'r', encoding='utf-8')
        all = file.readlines()
        all[0] = str(int(all[0].strip()) + 1) + '\n'
        all.append('\n' + name + '\n')
        all.append(str(len(tip.split('\n'))) + '\n')
        all.append(str(tip))
        file.close()
        file = open('data.txt', 'w', encoding='utf-8')
        for i in all:
            file.write(i)
        file.close()
        self.close()
        WORDS = []
        add_words()


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('file_1.ui', self)

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

    def func(self):
        if not self.stop_game:
            self.sender().setStyleSheet("background-color: " + BTN_WRONG_COLOR)
        if not self.stop_game:
            now = self.sender()
            if now.text().upper() in self.now_word.upper():
                print(1)
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

    def change_cnt_players(self):
        a = self.sender()
        self.cnt_players = int(a.whatsThis())

    def change_level(self):
        self.level = int(self.sender().whatsThis())
        self.death.setMaximum(self.level)
        self.update_tracker()

    def new_word(self):
        for i in range(len(self.btn_show)):
            self.btn_show[i].deleteLater()
        self.btn_show = []
        word = random.choice(WORDS)
        self.now_word = word[0]
        self.help_info = word[1]
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

    def check_lost(self):
       if self.now_bad >= self.level:
            self.game_status.setText('Увы, но никто не отгадал слово!')
            self.stop_game = True

    def check_win(self):
        flag = True
        for i in self.btn_show:
            if i.text() == '*':
                flag = False
        if flag:
            self.game_status.setText(self.people[self.now_hod][0].upper() + self.people[self.now_hod][2:] + ' игрок отгадал слово!')
            self.stop_game = True

    def update_tracker(self):
        self.death.setMaximum(self.level)
        self.death.setValue(self.now_bad)

    def open_new_window(self):
        pass
        self.w1 = W2()
        self.w1.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec())