import argparse
import numpy as np

point_dict  = {}
contor_list = []

class Point:
        coor = None
        def __init__(self, coor):
                self.coor = np.array(coor, dtype=float)

        def __str__(self):
                return '{%s, %s}' % (self.coor[0], self.coor[1])

        def __repr__(self):
                return self.coor.__repr__()

class Elem:
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
        count = 0
        while True:
                line = file_figure.readline()
                if line == '':
                        contor_list.append(points)
                        break
                elif len(line) >= 4:
                        point = Point([float(i) for i in line.split()])
                        point_dict[count] = point
                        points.append(count)
                        count += 1
                else:
                        contor_list.append(points)
                        points = []

        file_figure.close()
        return list(range(count))

if __name__ == '__main__':
        points = get_points()
        for p in points:
                print(p, point_dict[p])
        print(contor_list)
        