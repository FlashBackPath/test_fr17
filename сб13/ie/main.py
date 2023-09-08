from PIL import Image, ImageFilter


class ImageProcessor():
    def __init__(self):
        self.name = ''
        self.original = None
        self.changes = []

    def open(self, name):
        self.name = name
        self.original = Image.open(name)
        self.changes.append(self.original)

    def do_BW(self):
        self.original = self.original.convert('L')
        self.changes.append(self.original)
        self.original.show()


IP = ImageProcessor()
IP.open('bright.png')
IP.do_BW()


