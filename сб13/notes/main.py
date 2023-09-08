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
        for note in self.notes:
            self.ui.lw_notes.addItem(note)

        self.ui.btn_create.clicked.connect(self.add_note)
        self.ui.btn_del.clicked.connect(self.del_note)
        self.ui.btn_save.clicked.connect(self.save_note)
        self.ui.lw_notes.itemClicked.connect(self.show_note)
        self.ui.tag_create.clicked.connect(self.add_tag)
        self.ui.tag_del.clicked.connect(self.del_tag)

        self.ui.tag_search.clicked.connect(self.search_tag)

    def search_tag(self):
        if self.ui.tag_search.text() == 'Пошук по замітках':
            text = self.ui.lineEdit.text()
            if text != '':
                self.ui.lw_notes.clear()
                for note in self.notes:
                    if text in self.notes[note]['tags']:
                        self.ui.lw_notes.addItem(note)
            self.ui.tag_search.setText('Скинути пошук')
        else:
            self.ui.lineEdit.clear()
            self.ui.lw_tags.clear()
            self.ui.lw_notes.clear()
            for note in self.notes:
                self.ui.lw_notes.addItem(note)

            self.ui.tag_search.setText('Пошук по замітках')

    def del_tag(self):
        if self.ui.lw_tags.currentItem():
            note = self.ui.lw_notes.currentItem().text()
            tag = self.ui.lw_tags.currentItem().text()
            self.notes[note]['tags'].remove(tag)

            with open('file.json', 'w') as f:
                json.dump(self.notes, f)

            self.ui.lw_tags.clear()
            for tag in self.notes[note]['tags']:
                self.ui.lw_tags.addItem(tag)

    def add_tag(self):
        if self.ui.lw_notes.currentItem():
            text = self.ui.lineEdit.text()
            if text == '':
                return

            self.ui.lineEdit.clear()
            name = self.ui.lw_notes.currentItem().text()
            self.notes[name]['tags'].append(text)
            self.ui.lw_tags.addItem(text)

            with open('file.json', 'w') as f:
                json.dump(self.notes, f)

    def show_note(self):
        name = self.ui.lw_notes.currentItem().text()
        text = self.notes[name]['text']
        self.ui.textEdit.setText(text)

        self.ui.lw_tags.clear()
        for tag in self.notes[name]['tags']:
            self.ui.lw_tags.addItem(tag)

    def save_note(self):
        if self.ui.lw_notes.currentItem():
            text = self.ui.textEdit.toPlainText()
            name = self.ui.lw_notes.currentItem().text()
            self.notes[name]['text'] = text

            with open('file.json', 'w') as f:
                json.dump(self.notes, f)

    def del_note(self):
        if self.ui.lw_notes.currentItem():
            name = self.ui.lw_notes.currentItem().text()
            del self.notes[name]

            with open('file.json', 'w') as f:
                json.dump(self.notes, f)

            self.ui.lw_notes.clear()
            for note in self.notes:
                self.ui.lw_notes.addItem(note)

            self.ui.lw_tags.clear()
            self.ui.textEdit.clear()

    def add_note(self):
        text, result = QInputDialog.getText(self.ui.centralwidget, 'Додати замітку',
                                            "Введіть назву замітки:")
        if result:
            self.ui.lw_notes.addItem(text)
            self.notes[text] = {'tags': [], 'text': ''}
            with open('file.json', 'w') as f:
                json.dump(self.notes, f)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())