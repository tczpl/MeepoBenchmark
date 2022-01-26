import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16 ,32]

to_draw = []

for member_cnt in [4]:
    for shard_cnt in shards:
        to_draw.append([])
        account_cnt = shard_cnt * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        replay_time = util.get_replaytime(logdir)
        to_draw[-1].append(replay_time)
        print(shard_cnt, member_cnt, replay_time)

        for err in [10, 30, 50, 70, 90]:
            logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_error20_transfer8192*500of"+str(account_cnt)+"_"+str(err)
            replay_time = util.get_replaytime(logdir)
            to_draw[-1].append(replay_time)
            print(shard_cnt, member_cnt, replay_time)



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


x = np.arange(6)  # the label locations
width = 0.18  # the width of the bars


rects1 = plt.bar(x - 2*width, to_draw[0], width, label=labels[0]+" shard")
rects2 = plt.bar(x - 1*width, to_draw[1], width, label=labels[1]+" shard")
rects3 = plt.bar(x - 0*width, to_draw[2], width, label=labels[2]+" shard")
rects4 = plt.bar(x + 1*width, to_draw[3], width, label=labels[3]+" shard")
rects5 = plt.bar(x + 2*width, to_draw[4], width, label=labels[4]+" shard")

#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
#autolabel(rects4)
#autolabel(rects5)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Replay-epoch Time (ms)', fontsize=20)
plt.xlabel('Error Transactions', fontsize=20)
plt.xticks(ticks=x, labels=["0","10%","30%","50%","70%","90%"], rotation=15, fontsize=20)
plt.yticks(fontsize=20)
# plt.ylim(0, 210)
plt.legend(loc=1, ncol=1, fontsize=18)#图例及位置： 1右上角，2 左上角 loc函数可不写 0为最优 ncol为标签有几列

plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
