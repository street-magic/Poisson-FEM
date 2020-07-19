import argparse
import numpy as np

class Point:
        coor = None
        def __init__(self, coor):
                self.coor = np.array(coor, dtype=float)

        def __str__(self):
                return '{%s, %s}' % (self.coor[0], self.coor[1])

        def __repr__(self):
                return self.coor.__repr__()

class Edge:
        edge = None
        ivertex = None
        overtex = None

        def __init__(self, edge, ivertex, overtex):
                self.egde = edge
                self.ivertex = ivertex
                self.overtex = overtex
        

def get_points():
        parser = argparse.ArgumentParser()
        parser.add_argument('--figure_path', help='path to figure')
        args = parser.parse_args()
        file_figure = open(args.figure_path, 'r')
        
        points = []
        while True:
                line = file_figure.readline()
                print(line, end='')
                if line == '':
                        break
                elif len(line) >= 3:
                        points.append(Point([float(i) for i in line.split()]))
        file_figure.close()
        return points

if __name__ == '__main__':
        points = get_points()
        print(points, points[0])
        