from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox
import sys
from spammer import Spammer
from email.message import EmailMessage
import mysql.connector

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spammer')
        layout = QGridLayout()

        layout.addWidget(QLabel('Sender email'), 0, 0)
        self.emailEdit = QLineEdit()
        self.emailEdit.setText('sendermail@gmail.com')
        layout.addWidget(self.emailEdit, 0, 1)

        layout.addWidget(QLabel('Sender password'), 1, 0)
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordEdit.setText('senderpass')
        layout.addWidget(self.passwordEdit, 1, 1)

        layout.addWidget(QLabel('Subject'), 2, 0)
        self.subjectEdit = QLineEdit()
        self.subjectEdit.setText('Promo')
        layout.addWidget(self.subjectEdit, 2, 1)

        layout.addWidget(QLabel('Message'), 3, 0)
        self.messageEdit = QTextEdit()
        self.messageEdit.setText('Message')
        layout.addWidget(self.messageEdit, 3, 1)

        layout.addWidget(QLabel('Choose message'), 4, 0)
        self.messageChoose = QComboBox()
        self.messageChoose.currentIndexChanged.connect(self.onMessageChoose)
        layout.addWidget(self.messageChoose, 4, 1)

        startSendingBtn = QPushButton('Start')
        startSendingBtn.clicked.connect(lambda: self.startSending())
        layout.addWidget(startSendingBtn, 5, 1)

        self.setLayout(layout)

        self.connection = mysql.connector.connect(host='localhost', database='spammer', user='root', password='pass')
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute('SELECT email FROM subscribers')
            self.receivers = cursor.fetchall()
            cursor.execute('SELECT * FROM messages')
            self.messages = cursor.fetchall()
            self.subjectEdit.setText(self.messages[0][1])
            self.messageEdit.setText(self.messages[0][2])
            print(self.messages)
            for i in self.messages:
                self.messageChoose.addItem(i[1])

    def onMessageChoose(self):
        self.subjectEdit.setText(self.messages[self.messageChoose.currentIndex()][1])
        self.messageEdit.setText(self.messages[self.messageChoose.currentIndex()][2])

    def startSending(self):
        try:
            spammer = Spammer(self.emailEdit.text(), self.passwordEdit.text(), self.receivers)
            message = EmailMessage()
            message.set_content(self.messageEdit.toPlainText())
            message['Subject'] = self.subjectEdit.text()
            print(self.messageEdit.toPlainText())
            spammer.run(message)
        except:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
