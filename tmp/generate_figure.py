import numpy as np
from shapely.geometry import Point, Polygon

f = open('file.txt', 'w')
# for angle in np.linspace(0, 2 * np.pi, 100):
#         v = np.random.uniform(0.98, 1.05)
#         f.write('%s %s\n' % (v * np.cos(angle) * 200 + 300, v * np.sin(angle) * 200 + 300))
M = np.random.randint(100, 500, (50, 2))
for l in M:
        f.write('%s %s\n' % (l[0], l[1]))
f.close()