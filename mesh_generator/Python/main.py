import argparse
import queue
import numpy as np

point_dict  = {}
contor_list = []
triagle_dict = {}
edge_dict = {}

class Point:
        x = None
        y = None

        def __init__(self, coor):
                self.x = coor[0]
                self.y = coor[1]


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

def is_on_right_side(vertex, point_begin, point_end):
        A = point_dict[point_begin]
        B = point_dict[point_end]
        P = point_dict[vertex]
        return (B.x - A.x) * (P.y - A.y) - (P.x - A.x) * (B.y - A.y) < 0       

def delaunay_condition(A, B, C, vertex):
        A = point_dict[A]
        B = point_dict[B]
        C = point_dict[C]
        D = point_dict[vertex]

        return np.linalg.det(np.array([
                [A.x, A.y, A.x ** 2 + A.y ** 2, 1],
                [B.x, B.y, B.x ** 2 + B.y ** 2, 1],
                [C.x, C.y, C.x ** 2 + C.y ** 2, 1],
                [D.x, D.y, D.x ** 2 + D.y ** 2, 1]
        ], dtype=float)) <= 0

def qwe():
        for key in edge_dict:
                print(key, edge_dict[key])

def flip(A, B, vertex):
        if len(edge_dict[pair(A, B)]) == 0:
                edge_dict[pair(A, B)] = set([vertex])
                if not pair(A, vertex) in edge_dict:
                        edge_dict[pair(A, vertex)] = set([B])
                else:
                        edge_dict[pair(A, vertex)] |= set([B])
                if not pair(B, vertex) in edge_dict:
                        edge_dict[pair(B, vertex)] = set([A])
                else:
                        edge_dict[pair(B, vertex)] |= set([A])
                return

        C = list(edge_dict[pair(A, B)])[0]         

        is_good = delaunay_condition(B, C, A, vertex)
        if is_good:
                edge_dict[pair(A, B)] |= set([vertex])
                if not pair(A, vertex) in edge_dict:
                        edge_dict[pair(A, vertex)] = set([B])
                else:
                        edge_dict[pair(A, vertex)] |= set([B])
                if not pair(B, vertex) in edge_dict:
                        edge_dict[pair(B, vertex)] = set([A])
                else:
                        edge_dict[pair(B, vertex)] |= set([A])
                
        else:
                del edge_dict[pair(A, B)]
                edge_dict[pair(A, C)] ^= set([B])
                edge_dict[pair(C, B)] ^= set([A])
                flip(A, C, vertex)
                flip(C, B, vertex)


 
def pair(A, B):
        if A < B:
                return B, A
        return A, B

def trio(A, B, C):
        return tuple(sorted([A, B, C]))

def alg(points):
        tmp = sorted(points, key=lambda elem: point_dict[elem].x)
        tmp = sorted(tmp, key=lambda elem: point_dict[elem].y, reverse=True)

        A, B = tmp[0], tmp[1]
        if point_dict[A].y != point_dict[B].y:
                C = tmp[2]
        else:
                i = 0
                while point_dict[tmp[i]].y == point_dict[A].y:
                        i += 1
                C = tmp[i]
        
        tmp.remove(A)
        tmp.remove(B)
        tmp.remove(C)

        edge_dict[pair(A, B)] = set([C])
        edge_dict[pair(A, C)] = set([B])
        edge_dict[pair(B, C)] = set([A])

        hull = []
        if point_dict[A].y == point_dict[B].y:
                hull = [A, C, B]
        else:
                hull = [A, B, C]
        
        for vertex in tmp:
                index = None
                bas = []
                new_hull = list(hull)
                for i in range(-1, len(hull) - 1):
                        if is_on_right_side(vertex, hull[i], hull[i + 1]):
                                flip(hull[i], hull[i + 1], vertex)
                                if index == None:
                                        if i == -1:
                                                new_hull.append(vertex)
                                        else:
                                                new_hull = new_hull[:i + 1] + [vertex] + new_hull[i + 1:]
                                        index = i
                                else:
                                        if hull[i] in bas:
                                                new_hull.remove(hull[i])
                                        if hull[i + 1] in bas:
                                                new_hull.remove(hull[i + 1])

                                bas += [hull[i], hull[i + 1]]
                hull = new_hull

if __name__ == '__main__':
        points = get_points()
        alg(points)
        
        count = 0
        for key in edge_dict:
                for v in list(edge_dict[key]):
                        tmp = trio(key[0], key[1], v)
                        if not tmp in triagle_dict:
                                triagle_dict[tmp] = count
                                count += 1
        f = open('tmp/result.txt', 'w')
        for key in triagle_dict:
                A = point_dict[key[0]]
                B = point_dict[key[1]]
                C = point_dict[key[2]]
                f.write('%s %s %s %s %s %s\n' % (A.x, A.y, B.x, B.y, C.x, C.y))
        f.close()



        