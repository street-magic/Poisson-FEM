import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class Window(QWidget):
        figure = None

        def __init__(self):
                super().__init__()
                self.initUI()

        def initUI(self):
                
                self.setFixedSize(700, 750)
                
                self.setWindowTitle('Triangulation')
                self.setWindowIcon(QIcon('visualization/icon.png'))

                button_build = QPushButton('New polygon', self)
                button_build.setGeometry(10, 10, 100, 30)
                button_build.clicked.connect(self.build_polygon)

                button_open = QPushButton('Open file', self)
                button_open.setGeometry(120, 10, 100, 30)
                button_open.clicked.connect(self.open_file)

                button_clear = QPushButton('Clear', self)
                button_clear.setGeometry(230, 10, 100, 30)
                button_clear.clicked.connect(self.clear_widget)

                self.show()

        def open_file(self):
                fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
                if fname == '':
                        return
                f = open(fname, 'r')
                self.figure = [[]]
                while True:
                        line = f.readline()
                        if line == '':
                                break
                        elif len(line) < 3:
                                self.figure.append([])
                        else:
                                self.figure[-1].append([int(i) for i in line.split()])
                f.close()
                self.update()
        
        def build_polygon(self):
                print('hi')

        def clear_widget(self):
                self.figure = None
                self.update()
        
        def paintEvent(self, event):
                painter = QPainter(self)
                painter.setPen(Qt.black)
                painter.drawLine(  0,  50, 700,  50) # dividing line

                painter.drawLine( 30, 720, 670, 720) # Ox axis
                painter.drawLine( 30, 720,  30,  80) # Oy axis

                painter.drawLine(670, 720, 665, 715) # arrow Ox
                painter.drawLine(670, 720, 665, 725) # arrow Ox
                painter.drawLine( 30,  80,  25,  85) # arrow Oy
                painter.drawLine( 30,  80,  35,  85) # arrow Oy
                
                if self.figure == None:
                        return
                for contour in self.figure:
                        for i in range(-1, len(contour) - 1):
                                painter.drawLine(
                                        30 + contour[i][0],
                                        720 - contour[i][1],
                                        30 +contour[i + 1][0],
                                        720 - contour[i + 1][1]
                                )

        
if __name__ == '__main__':
        app = QApplication(sys.argv)

        window = Window()
        sys.exit(app.exec_())