import imp
import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

to_draw = []
to_draw.append([])
labels = []

for shard_cnt in [2, 4, 8, 16, 32]:
    for member_cnt in [1, 2, 3, 4]:
        labels.append(str(shard_cnt)+"$\\times$"+str(member_cnt))
        account_cnt = shard_cnt * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        all_crosstime = util.get_all_crosstime(logdir)
        to_draw[0].append(pd.array(all_crosstime))
        print(shard_cnt, member_cnt, len(all_crosstime))



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=15)

rects1 = plt.boxplot(to_draw[0], labels=labels)

# autolabel(rects1)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Cross Time (ms)', fontsize=20)
plt.xlabel('#Shards $\\times$ #Members', fontsize=20)
plt.xticks(rotation=45, fontsize=15)
plt.yticks(fontsize=20)
# plt.ylim(0,35000)

plt.tight_layout()

plt.savefig("rq1-2_crosstime.pdf")
