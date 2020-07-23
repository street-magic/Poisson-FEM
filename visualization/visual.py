import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class Window(QWidget):
        figure = None
        triangulation = None
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

                button_build_triangle = QPushButton('Triagle', self)
                button_build_triangle.setGeometry(340, 10, 100, 30)
                button_build_triangle.clicked.connect(self.build_triangle)

                self.show()

        def open_file(self):
                fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
                if fname == '':
                        return
                f = open(fname, 'r')
                self.figure = [[]]
                while True:
                        line = f.readline()
                        print(line, end='')
                        if line == '':
                                break
                        elif len(line) < 3:
                                self.figure.append([])
                        else:
                                # self.figure[-1].append([int(float(i) * 100 + 200) for i in line.split()])
                                self.figure[-1].append([int(float(i)) for i in line.split()])
                f.close()
                self.update()
        
        def build_polygon(self):
                print('hi')

        def clear_widget(self):
                self.figure = None
                self.triangulation = None
                self.update()
        
        def build_triangle(self):
                fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
                if fname == '':
                        return
                f = open(fname, 'r')
                self.triangulation = []
                while True:
                        line = f.readline()
                        if line == '':
                                break
                        else:
                                self.triangulation.append([int(float(i)) for i in line.strip().split()])


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
                
                if self.figure != None:
                        for contour in self.figure:
                                for i in range(-1, len(contour) - 1):
                                        painter.drawLine(
                                                30 + contour[i][0],
                                                720 - contour[i][1],
                                                30 + contour[i + 1][0],
                                                720 - contour[i + 1][1]
                                        )
                if self.triangulation != None:
                        for triangle in self.triangulation:
                                Ax, Ay, Bx, By, Cx, Cy = triangle
                                painter.setPen(Qt.red)
                                painter.drawPoint(30 + Ax, 720 - Ay)
                                painter.drawPoint(30 + Bx, 720 - By)
                                painter.drawPoint(30 + Cx, 720 - Cy)

                                painter.setPen(Qt.black)
                                painter.drawLine(30 + Ax, 720 - Ay, 30 + Bx, 720 - By)
                                painter.drawLine(30 + Bx, 720 - By, 30 + Cx, 720 - Cy)
                                painter.drawLine(30 + Cx, 720 - Cy, 30 + Ax, 720 - Ay)

        
if __name__ == '__main__':
        app = QApplication(sys.argv)

        window = Window()
        sys.exit(app.exec_())