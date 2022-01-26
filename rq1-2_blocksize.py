import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

to_draw = []
for member_cnt in [1]:
    to_draw.append([])
    for shard_cnt in [2, 4, 8, 16, 32]:
        account_cnt = shard_cnt * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        avg_blockkb = util.get_blockkb(logdir)
        to_draw[-1].append(avg_blockkb)
        print(shard_cnt, member_cnt, avg_blockkb)



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=15)

labels = ['2', '4', '8', '16', '32']

x = np.arange(len(labels))  # the label locations
width = 0.8  # the width of the bars

rects1 = plt.bar(x,  to_draw[0], width, label='1 member')
autolabel(rects1)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Average Size of Blocks (kb)', fontsize=20)
plt.xlabel('Number of Shards', fontsize=20)
plt.xticks(ticks=x, labels=labels, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(0,35000)

plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
