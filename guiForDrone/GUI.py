import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont


class Example(QWidget):

    def hello(self):
        print("Hello is pressed")
    def hi(self):
        print("Hi is pressed")

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Hello', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        btn.clicked[bool].connect(self.hello)

        btn2 = QPushButton('Hi', self)
        btn2.setToolTip('This is a <b>QPushButton</b> widget')
        btn2.resize(btn.sizeHint())
        btn2.move(150, 50)
        btn2.clicked[bool].connect(self.hi)
        

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()