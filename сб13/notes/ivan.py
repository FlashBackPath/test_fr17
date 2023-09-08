import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QInputDialog
from ui import Ui_MainWindow
import json


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open('file.json', 'r') as f:
            self.notes = json.load(f)
        self.ui.btn_create.clicked.connect(self.add_note)

    def add_note(self):
        text, result = QInputDialog.getText(self.ui.centralwidget, 'Додати замітку', "Введіть назву замітки:")

        if result:
            self.ui.lw_notes.addItem(text)
            self.notes[text] = {'text': '', 'tags': []}
            with open('file.json', 'w') as f:
                json.dump(self.notes, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())