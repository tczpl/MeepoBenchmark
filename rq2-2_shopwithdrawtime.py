import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16,32]

to1 = []
to2 = []
for member_cnt in [4]:
    for shard_cnt in shards:
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_shop_"
        avg_withdraw_time = util.get_withdrawtime(logdir)
        to1.append(avg_withdraw_time)
        print(shard_cnt, member_cnt, avg_withdraw_time)

        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_shop2_"
        avg_withdraw_time = util.get_withdrawtime(logdir)
        to2.append(avg_withdraw_time)
        print(shard_cnt, member_cnt, avg_withdraw_time)


labels = ['2', '4', '8', '16', '32']

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.0f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    # weight="semibold",
                    ha='center', va='bottom', fontsize=15)


x = np.arange(len(labels))  # the label locations
width = 0.4  # the width of the bars


rects1 = plt.bar(x - 0.5*width, to1, width, label='With Partial\'')
rects2 = plt.bar(x + 0.5*width, to2, width, label='Without Partial\'')

autolabel(rects1)
autolabel(rects2)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Communication Time (ms)', fontsize=20)
plt.xlabel('Number of Shards', fontsize=20)
plt.xticks(ticks=x, labels=labels, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(0, 800)
plt.legend(loc=2, ncol=1, fontsize=18)#图例及位置： 1右上角，2 左上角 loc函数可不写 0为最优 ncol为标签有几列

plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
