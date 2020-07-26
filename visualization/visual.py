import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt

class Window(QWidget):
        point_dict = None
        contour = None
        points = None
        figure = None
        triangulation = None
        cells = None

        def __init__(self):
                super().__init__()
                self.initUI()

        def initUI(self):
                
                self.setFixedSize(700, 750)
                
                self.setWindowTitle('Triangulation')
                self.setWindowIcon(QIcon('visualization/icon.png'))

                button_build = QPushButton('Points', self)
                button_build.setGeometry(10, 10, 100, 30)
                button_build.clicked.connect(self.draw_points)

                button_open = QPushButton('Contour', self)
                button_open.setGeometry(120, 10, 100, 30)
                button_open.clicked.connect(self.draw_contour)

                button_clear = QPushButton('Clear', self)
                button_clear.setGeometry(230, 10, 100, 30)
                button_clear.clicked.connect(self.clear_widget)

                button_build_triangle = QPushButton('Triagle', self)
                button_build_triangle.setGeometry(340, 10, 100, 30)
                button_build_triangle.clicked.connect(self.build_triangle)

                button_build_triangle = QPushButton('Cells', self)
                button_build_triangle.setGeometry(450, 10, 100, 30)
                button_build_triangle.clicked.connect(self.build_cells)

                self.show()

        def draw_contour(self):
                self.point_dict = {}

                f = open('output/points.txt', 'r')
                while True:
                        line = f.readline()
                        if len(line) <= 2:
                                break
                        v, x, y = [float(i) for i in line.strip().split()]
                        v = int(v)
                        self.point_dict[v] = (x, y)
                f.close()
                f = open('output/contour.txt', 'r')
                self.contour = [int(i) for i in f.readline().strip().split()]
                f.close()
                
                self.update()
        
        def draw_points(self):
                self.points = []
                f = open(os.getcwd() + '/output/points.txt', 'r')
                while True:
                        line = f.readline()
                        if len(line) <= 3:
                                break
                        _, x, y = [float(i) for i in line.strip().split()]
                        # self.points.append([int(x), int(y)])
                        self.points.append([x, y])
                f.close()
                self.update()


        def clear_widget(self):
                self.point_dict = None
                self.points = None
                self.contour = None
                self.figure = None
                self.triangulation = None
                self.cells = None
                self.update()
        
        def build_triangle(self):
                # fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
                # if fname == '':
                        # return
                # f = open(fname, 'r')
                f = open(os.getcwd() + '/output/triangulation.txt', 'r')
                self.triangulation = []
                while True:
                        line = f.readline()
                        if line == '':
                                break
                        else:
                                # self.triangulation.append([int(float(i)) for i in line.strip().split()])
                                self.triangulation.append([float(i) for i in line.strip().split()])
                f.close()
                self.update()

        def build_cells(self):
                f = open('output/cells.txt', 'r')
                self.cells = []
                while True:
                        line = f.readline()
                        if len(line) <= 2:
                                break
                        # self.cells.append([int(float(i)) for i in line.strip().split()])
                        self.cells.append([float(i) for i in line.strip().split()])
                f.close()
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
                
                if self.points != None:
                        for p in self.points:
                                pen = QPen()
                                pen.setColor(Qt.red)
                                pen.setWidth(5)
                                painter.setPen(pen)
                                painter.drawPoint(30 + p[0], 720 - p[1])

                if self.contour != None:
                        pen = QPen()
                        pen.setColor(Qt.black)
                        painter.setPen(pen)
                        for i in range(-1, len(self.contour) - 1):
                                painter.drawLine(30 + self.point_dict[self.contour[i]][0],
                                                 720 - self.point_dict[self.contour[i]][1],
                                                 30 + self.point_dict[self.contour[i + 1]][0],
                                                 720 - self.point_dict[self.contour[i + 1]][1])
                        path = QPainterPath()
                        path.moveTo(30 + self.point_dict[self.contour[-1]][0], 720 - self.point_dict[self.contour[-1]][1])
                        for i in range(len(self.contour)):
                                path.lineTo(30 + self.point_dict[self.contour[i]][0], 720 - self.point_dict[self.contour[i]][1])
                        
                        path.closeSubpath()
                        
                        painter.fillPath(path, QColor(0, 0, 255))


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

                if self.cells != None:
                        pen = QPen()
                        max_value = max(self.cells, key=lambda x: x[-1])[-1]
                        # print(max_value)
                        for cell in self.cells:
                                pen.setColor(Qt.blue)
                                pen.setWidth(5)
                                painter.setPen(pen)
                                painter.drawPoint(30 + cell[0], 720 - cell[1])
                                
                                value = cell[-1]
                                cell = cell[2:-1]
                                # pen.setColor(Qt.red)
                                # pen.setWidth(1)
                                # painter.setPen(pen)

                                path = QPainterPath()
                                path.moveTo(30 + cell[-2], 720 - cell[-1])
                                for i in range(0, len(cell), 2):
                                        path.lineTo(30 + cell[i], 720 - cell[i + 1])
                                
                                path.closeSubpath()
                                
                                painter.fillPath(path, QColor(min(255, int(4 * 255 * value / max_value)), 0, 255 - min(255, int(1 * 255 * value / max_value))))

                                pen.setColor(Qt.black)
                                pen.setWidth(1)
                                painter.setPen(pen)
                                painter.drawPath(path)
                                # for i in range(-2, len(cell) - 2, 2):
                                #         painter.drawLine(30 + cell[i], 720 - cell[i + 1], 30 + cell[i + 2], 720 - cell[i + 3])

                                pen.setColor(Qt.green)
                                pen.setWidth(5)
                                painter.setPen(pen)
                                for i in range(0, len(cell), 2):
                                        painter.drawPoint(30 + cell[i], 720 - cell[i + 1])

                # path = QPainterPath()
                # path.moveTo(30 + 0, 720 - 0)
                # path.lineTo(30 + 100, 720 - 100)
                # path.lineTo(30 + 200, 720 - 300)
                # path.lineTo(30 + 0, 720 - 0)
                # path.closeSubpath()
        

                # # painter.drawPath(path)
                # painter.fillPath(path, QColor(25, 12, 25))
                                         
                                
        
if __name__ == '__main__':
        app = QApplication(sys.argv)

        window = Window()
        sys.exit(app.exec_())