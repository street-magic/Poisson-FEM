import numpy as np


point_dict = {}
edge_dict = {}
contour_list = []
triagle_dict = {}
cell_dict = {}

class Point:
        x = None
        y = None

        def __init__(self, coor):
                self.x = coor[0]
                self.y = coor[1]

        def __str__(self):
                return '{%s %s}' % (self.x, self.y)


class Cell:
        center = None
        neighbors = None
        vertices = None
        is_contour = None
        value = 0
        new_value = 0

        def __init__(self, center):
                self.center = center
                self.neighbors = []
                self.vertices = []

                edge_list = list(triagle_dict[center])
                
                new_list = []
                if is_on_right_side(center, edge_list[0][0], edge_list[0][1]):
                        new_list.append((edge_list[0][1], edge_list[0][0]))
                else:
                        new_list.append(edge_list[0])
                tmp = set(edge_list[1:])

                while len(tmp) != 0:
                        # print(tmp)
                        # print(new_list)
                        for elem in list(tmp):
                                if new_list[-1][1] == elem[0]:
                                        new_list.append(elem)
                                        tmp.remove(elem)
                                elif new_list[-1][1] == elem[1]:
                                        new_list.append((elem[1], elem[0]))
                                        tmp.remove(elem)
                                elif new_list[0][0] == elem[0]:
                                        new_list = [(elem[1], elem[0])] + new_list
                                        tmp.remove(elem)
                                elif new_list[0][0] == elem[1]:
                                        new_list = [elem] + new_list
                                        tmp.remove(elem)
                edge_list = new_list
        
                for (A, B) in edge_list:
                        self.neighbors.append(A)

                if center in contour_list:
                        self.neighbors.append(edge_list[-1][1])
                        self.is_contour = True
                        return
                else:
                        self.is_contour = False

                for (A, B) in edge_list:
                        x = (point_dict[A].x + point_dict[B].x + point_dict[center].x) / 3
                        y = (point_dict[A].y + point_dict[B].y + point_dict[center].y) / 3
                        self.vertices.append((x, y))
        
        def update_value(self):
                if self.is_contour:
                        return
                outside_value = 0
                inside_value = 0
                # print('center %s:' % self.center)
                for i, neig in enumerate(self.neighbors):
                        l = ((point_dict[self.center].x - point_dict[neig].x) ** 2 + \
                             (point_dict[self.center].y - point_dict[neig].y) ** 2) ** 0.5
                        c = ((self.vertices[i][0] - self.vertices[i - 1][0]) ** 2 + \
                             (self.vertices[i][1] - self.vertices[i - 1][1]) ** 2) ** 0.5
                        # print(neig, c / l)
                        
                        outside_value += cell_dict[neig].value * c / l
                        inside_value += c / l
                inside_value *= self.value
                self.new_value = self.value + 0.3 * (outside_value - inside_value)

                if self.new_value < 0:
                        self.new_value = 0

        def make_step(self):
                self.value = self.new_value
                


def pair(A, B):
        if A < B:
                return B, A
        return A, B

def trio(A, B, C):
        return tuple(sorted([A, B, C]))

def is_on_right_side(vertex, point_begin, point_end):
        A = point_dict[point_begin]
        B = point_dict[point_end]
        P = point_dict[vertex]
        return (B.x - A.x) * (P.y - A.y) - (P.x - A.x) * (B.y - A.y) < 0



if __name__ == '__main__':
        f = open('output/points.txt', 'r')
        while True:
                line = f.readline()
                if line == '':
                        break
                idx, x, y = [float(i) for i in line.strip().split()]
                point_dict[int(idx)] = Point([x, y])
        f.close()

        f = open('output/edges.txt', 'r')
        while True:
                line = f.readline()
                if line == '':
                        break
                x, y = [int(i) for i in line.strip().split()]
                if x in edge_dict:
                        edge_dict[x].add(y)
                else:
                        edge_dict[x] = set([y])
                if y in edge_dict:
                        edge_dict[y].add(x)
                else:
                        edge_dict[y] = set([x])
        f.close()
        
        contour_list = [int(i) for i in open('output/contour.txt', 'r').readline().strip().split()]

        f = open('output/triangles.txt', 'r')
        while True:
                line = f.readline()
                if line == '':
                        break
                a, b, c = [int(i) for i in line.strip().split()]
                if not a in triagle_dict:
                        triagle_dict[a] = set()
                if not b in triagle_dict:
                        triagle_dict[b] = set()
                if not c in triagle_dict:
                        triagle_dict[c] = set()

                triagle_dict[a].add((b, c))
                triagle_dict[b].add((a, c))
                triagle_dict[c].add((a, b))
        f.close()     
        
        for point in point_dict:
                cell_dict[point] = Cell(point)

        

        # print(len(point_dict))
        # print(point_dict.keys())
        source = np.random.randint(0, len(point_dict))
        print(source)
        cell_dict[source].value = 1000

        

        for i in range(100):
                # print('i:', i)
                # for key in cell_dict:
                #         print(key, cell_dict[key].value)
                # print()
                for key in cell_dict:
                        cell_dict[key].update_value()
                cell_dict[source].new_value = 100
                for key in cell_dict:
                        cell_dict[key].make_step()

        f = open('output/cells.txt', 'w')
        for key in cell_dict:
                if not cell_dict[key].is_contour:
                        f.write('%s %s ' % (point_dict[key].x, point_dict[key].y))
                        for p in cell_dict[key].vertices:
                                f.write('%s %s ' % (p[0], p[1]))
                        f.write('%s\n' % cell_dict[key].value)
        f.close()

        # for key in cell_dict:
        #         print(cell_dict[key].value)

        