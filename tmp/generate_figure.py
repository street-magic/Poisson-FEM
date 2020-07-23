import numpy as np

f = open('file.txt', 'w')
for angle in np.linspace(0, 2 * np.pi, 100):
        f.write('%s %s\n' % (np.cos(angle) * 200 + 300, np.sin(angle) * 200 + 300))
f.write('\n')
for angle in np.linspace(0, 2 * np.pi, 100):
        f.write('%s %s\n' % (np.cos(angle) * 100 + 300, np.sin(angle) * 100 + 300))
f.close()