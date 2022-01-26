import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16,32]

tps1 = []
tps2 = []
for member_cnt in [4]:
    for shard_cnt in shards:
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_shop_"
        tps = util.get_tps(logdir)
        tps1.append(tps)
        print(shard_cnt, member_cnt, tps)

        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_shop2_"
        tps = util.get_tps(logdir)
        tps2.append(tps)
        print(shard_cnt, member_cnt, tps)


labels = ['2', '4', '8', '16', '32']


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.0f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    weight="semibold",
                    ha='center', va='bottom', fontsize=10)

x = np.arange(len(labels))  # the label locations
width = 0.4  # the width of the bars

rects1 = plt.bar(x - 0.5*width, tps1, width, label='With Partial\'')
rects2 = plt.bar(x + 0.5*width, tps2, width, label='Without Partial\'')
autolabel(rects1)
autolabel(rects2)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Throughput (tx/s)', fontsize=20)
plt.xlabel('Number of Shards', fontsize=20)
plt.xticks(ticks=x, labels=labels, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(ncol=1, fontsize=20)
plt.ylim(0,55000)
plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
