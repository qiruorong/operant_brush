import matplotlib.pyplot as plt

Date = ['25/10', '26/10', '28/10', '29/10', '31/10', '01/11', '04/11', '07/11', '08/11']
y11 = [None, None, 180, 81, 75, None, 213, 163, 145]
y12 = [98, None, 95, 140, None, 60, 141, 138, 157]
y13 = [250, 302, 89, 95, None, 77, 127, 193, 127]
y14 = [255, 158, 88, None, None, None, 185, 166, 157]
y21 = [None, 26, 9, 7, 9, None, 24, 17, 9]
y22 = [36, 19, 7, 37, None, 8, 14, 23, 22]
y23 = [24, 19, 9, 9, None, 6, 15, 17, 8]
y24 = [30, 19, 16, 4, None, None, 15, 8, 11]
y3 = 8
x = range(len(Date))

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
legend_labels = ['BAX1', 'BAZ2', 'BAX3', 'BBB2']
ax1.plot(x, y11, linestyle='-', label=legend_labels[0], color='g')
ax1.plot(x, y12, linestyle='--', label=legend_labels[1], color='g')
ax1.plot(x, y13, linestyle='-.', label=legend_labels[2], color='g')
ax1.plot(x, y14, linestyle=':', label=legend_labels[3], color='g')
ax1.legend()
ax1.plot(x, y21, linestyle='-', label=legend_labels[0], color='b')
ax1.plot(x, y22, linestyle='--', label=legend_labels[1], color='b')
ax1.plot(x, y23, linestyle='-.', label=legend_labels[2], color='b')
ax1.plot(x, y24, linestyle=':', label=legend_labels[3], color='b')
ax2.legend()
ax2.axhline(y=y3, linestyle=':', color='r')
fig.set_size_inches(6, 4)

ax1.set_xlabel('Date')
ax1.set_ylabel('Lick in first minutes', color='g')
ax2.set_ylabel('reward in first minutes', color='b')
ax1.set_title('Number of Licks per 10 minutes progress across animals')  # Use ax1 to set the title

plt.show()

