from PyQt5.QtCore import Qt, QCoreApplication, QEvent, pyqtSignal, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QRadioButton,
    QPushButton,
    QLabel,
    QDesktopWidget,
    QMessageBox,
)
from PyQt5 import QtGui
import json, sys
from random import sample, shuffle


class Quiz(QWidget):
    resized = pyqtSignal()

    
    def resize_win(self):
        self.move(self.width() * -2, 0)
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)

    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.points = 0
        self.counter = 0
        self.true_answer = None
        self.question = QLabel("""                       Добро пожаловать 
                        это тест по python
пожалуйста выберите количество вопросов""")
        self.font = QtGui.QFont("Times", 16, QtGui.QFont.Bold)
        self.font_btn = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.question.setFont(self.font)
        self.resolved = QLabel('')
        self.resolved.setFont(self.font_btn)
        self.RadioGroupBox = QGroupBox('Варианты ответа')
        self.button_answer_one = QRadioButton('')
        self.button_answer_one.setFont(self.font_btn)
        self.button_answer_two = QRadioButton('')
        self.button_answer_two.setFont(self.font_btn)
        self.button_answer_three = QRadioButton('')
        self.button_answer_three.setFont(self.font_btn)
        self.button_answer_four = QRadioButton('')
        self.button_answer_four.setFont(self.font_btn)
        self.push_button = QPushButton('Далее')
        self.push_button_five = QPushButton('5')
        self.push_button_fifteen = QPushButton('15')
        self.push_button_thirty = QPushButton('30')
        self.push_button.setFont(self.font_btn)

        self.layout_main = QVBoxLayout()
        self.layout_main.setSpacing(85)
        self.layout_question = QHBoxLayout()
        self.layout_left = QHBoxLayout()
        self.layout_right = QHBoxLayout()
        self.layout_push = QHBoxLayout()
        self.layout_left_right = QVBoxLayout()

        self.layout_question.addWidget(self.question, alignment=Qt.AlignCenter)
        self.layout_push.addWidget(self.push_button_five, alignment=Qt.AlignCenter)
        self.layout_push.addWidget(self.push_button_fifteen, alignment=Qt.AlignCenter)
        self.layout_push.addWidget(self.push_button_thirty, alignment=Qt.AlignCenter)
        self.layout_left.addWidget(self.button_answer_one, alignment=Qt.AlignCenter)
        self.layout_left.addWidget(self.button_answer_two, alignment=Qt.AlignCenter)
        self.layout_right.addWidget(self.button_answer_three, alignment=Qt.AlignCenter)
        self.layout_right.addWidget(self.button_answer_four, alignment=Qt.AlignCenter)

        self.layout_main.addLayout(self.layout_question)
        self.layout_left_right.addLayout(self.layout_left)
        self.layout_left_right.addLayout(self.layout_right)
        self.RadioGroupBox.setLayout(self.layout_left_right)
        self.layout_main.addWidget(self.RadioGroupBox, stretch=1)
        self.layout_main.addLayout(self.layout_push)
        self.RadioGroupBox.hide()

        self.setLayout(self.layout_main)

        self.push_button.clicked.connect(self.quiz)
        self.push_button_five.clicked.connect(lambda: self.set_counter_question(5))
        self.push_button_fifteen.clicked.connect(lambda: self.set_counter_question(15))
        self.push_button_thirty.clicked.connect(lambda: self.set_counter_question(30))
        self.resized.connect(self.resize_win)

        self.setStyleSheet('QWidget{background-image: url(fon.png)}')  


    def resizeEvent(self, event):
        self.resized.emit()
        return super(Quiz, self).resizeEvent(event)


    def initUI(self):
        self.setWindowTitle('Викторина по Python')
        self.width_screen = QDesktopWidget().screenGeometry(-1).width()
        self.height_screen = QDesktopWidget().screenGeometry(-1).height()
        self.width_win = int(QDesktopWidget().screenGeometry(-1).width()*0.35)
        self.height_win = int(QDesktopWidget().screenGeometry(-1).height()*0.5)
        self.resize(self.width_win, self.height_win)
        self.move((self.width_screen-self.width())//2, (self.height_screen-self.height())//2)
        self.setWindowIcon(QtGui.QIcon('icon.png'))


    def keyPressEvent(self, e):
        if self.counter >= 1:
            if e.key() == Qt.Key(49): 
                self.button_answer_one.setChecked(True)
            elif e.key() == Qt.Key(50): 
                self.button_answer_two.setChecked(True)
            elif e.key() == Qt.Key(51): 
                self.button_answer_three.setChecked(True)
            elif e.key() == Qt.Key(52): 
                self.button_answer_four.setChecked(True)
            elif e.key() == Qt.Key(32) or e.key() == Qt.Key(16777220): 
                self.quiz()
        

    def set_counter_question(self, number):
        with open('вопросы.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.counter_question = number
        questions_beta = list()
        self.questions = dict()
        for quest in data:
            questions_beta.append(quest)
        questions_beta = sample(questions_beta, self.counter_question)
        for quest in questions_beta:
            self.questions[quest] = data[quest]
        self.push_button_five.deleteLater()
        self.push_button_fifteen.deleteLater()
        self.push_button_thirty.deleteLater()
        self.layout_question.addWidget(self.resolved, alignment=Qt.AlignRight)
        self.RadioGroupBox.show()
        self.layout_push.addWidget(self.push_button,  alignment=Qt.AlignCenter)
        self.quiz()


    def quiz(self):
        self.hit_test = True
        for answer in [self.button_answer_one, self.button_answer_two, self.button_answer_three, self.button_answer_four]:
            if answer.isChecked():
                self.hit_test = False
            if answer.isChecked() and answer.text() == self.true_answer:
                self.points += 1
            answer.setCheckable(False)
            answer.setCheckable(True)
        if self.hit_test and self.counter != 0:
            return
        self.resize(self.width_win, self.height_win)
        if self.counter_question > self.counter:
            quest = list(self.questions.keys())[self.counter]
            self.question.setText(quest)
            self.true_answer = self.questions[quest][0]
            answers = self.questions[quest]
            shuffle(answers)
            self.button_answer_one.setText(answers[0])
            self.button_answer_two.setText(answers[1])
            self.button_answer_three.setText(answers[2])
            self.button_answer_four.setText(answers[3])
            self.counter += 1
            self.resolved.setText("""{0}/{1}""".format(self.counter, self.counter_question))
            if self.counter_question <= self.counter:
                self.push_button.setText('Подвести итоги')
        else:
            self.close()
            self.messege_box = QMessageBox()
            self.messege_box.setText("""Вы прошли тест по знанию python
    вот ваши резаультаты!
    Правильных ответов: {0}/{1}
    Удачи вам!""".format(self.points, self.counter_question))
            self.messege_box.exec_()
    
    
def main():
    app = QApplication(sys.argv)
    quiz = Quiz()
    quiz.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()