import numpy as np
from shapely.geometry import Point, Polygon

f = open('file.txt', 'w')
# for angle in np.linspace(0, 2 * np.pi - 0.01 , 100):
#         f.write('%s %s\n' % (0.5 * np.cos(angle) * 200 + 300, 0.5 * np.sin(angle) * 200 + 300))

# for i in np.linspace(100, 600, 10):
#         f.write('%s %s\n' % (i, 100))
# for i in np.linspace(100, 600, 10):
#         f.write('%s %s\n' % (600, i))
# for i in np.linspace(600, 100, 10):
#         f.write('%s %s\n' % (i, 600))
# for i in np.linspace(600, 100, 10):
#         f.write('%s %s\n' % (100, i))

X = np.random.randint(100, 600, (10000, 2))
for line in X:
        f.write('%s %s\n' % (line[0], line[1] / 3))
f.close()