import matplotlib.pyplot as plt

x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
y1 = [30, 31, 31, 32, 33, 35, 35, 40, 47, 62, 99, 186, 480]

x2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
y2 = [32, 32, 32, 33, 34, 34, 34, 34, 38, 43, 54, 69, 116, 271]

x3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y3 = [30, 31, 31, 32, 33, 35, 35, 40, 47, 62]

x4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y4 = [32, 32, 32, 33, 34, 34, 34, 34, 38, 43]
group_labels = ['64k', '128k', '256k', '512k', '1024k', '2048k', '4096k', '8M', '16M', '32M', '64M', '128M', '256M',
                '512M']
plt.title('broadcast(b) vs join(r)')
plt.xlabel('data size')
plt.ylabel('time(s)')

# plt.plot(x1, y1,'r', label='broadcast')
# plt.plot(x2, y2,'b',label='join')
# plt.xticks(x1, group_labels, rotation=0)

plt.plot(x3, y3, 'r', label='broadcast')
plt.plot(x4, y4, 'b', label='join')
plt.xticks(x3, group_labels, rotation=0)

#plt.fill_between(x3, y3, y4, where=y4 > y3, facecolor='blue')
#plt.fill_between(x3, y3, y4, where=y4 <= y3, facecolor='red')

plt.legend(bbox_to_anchor=[0.3, 1])
plt.grid()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.0, 2, 0.01)
y1 = np.sin(2 * np.pi * x)
y2 = 1.2 * np.sin(4 * np.pi * x)

fig, ax = plt.subplots()
ax.plot(x, y1, x, y2, color='black')
# ax.plot(x, y1, 'C1', label='Metaverse')
# ax.plot(x, y2, 'C2', label='Ethereum')
ax.fill_between(x, y1, y2, where=y2 > y1, facecolor='blue')
ax.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red')
ax.set_title('fill between where')

plt.show()