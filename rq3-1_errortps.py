import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16 ,32]

to_draw = []

for member_cnt in [4]:
    for shard_cnt in shards:
        to_draw.append([])
        account_cnt = shard_cnt * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        tps = util.get_tps(logdir)
        to_draw[-1].append(tps)
        print(shard_cnt, member_cnt, tps)

        for err in [10, 30, 50, 70, 90]:
            logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_error20_transfer8192*500of"+str(account_cnt)+"_"+str(err)
            tps = util.get_tps(logdir)
            to_draw[-1].append(tps)
            print(shard_cnt, member_cnt, tps)

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

x = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
width = 0.2  # the width of the bars

lines = ["r-o","g-p","b->","c-s","m-^"]

for i in range(len(shards)):
    plot = plt.plot(x, to_draw[i], lines[i], label=str(shards[i])+' shards',  markersize=10)

for i in range(len( to_draw[-1] )):
    thex = x[i]
    they = to_draw[-1][i]
    if i == 1:
        plt.annotate('{:.0f}'.format(they),
            xy=(thex, they),
            xytext=(0, -6),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='top', fontsize=15)
    else:
        plt.annotate('{:.0f}'.format(they),
                    xy=(thex, they),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=15)

def to_percent(temp, position):
  if temp == 0:
      return "0"
  return '%1.0f'%(100*temp) + '%'
plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Throughput (tx/s)', fontsize=20)
plt.xlabel('Error Transactions', fontsize=20)
plt.xticks([0, 0.1, 0.3, 0.5, 0.7, 0.9], rotation=15, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(loc=(0.3, 0.3), ncol=1, fontsize=15)
plt.xlim(-0.09, 1)
plt.ylim(0, 170000)
plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
