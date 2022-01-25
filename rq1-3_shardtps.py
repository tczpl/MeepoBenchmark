import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16,32,64,128]

tps1 = []
tps2 = []
for member_cnt in [1]:
    for shard_cnt in shards:
        account_cnt = 2 * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        tps = util.get_tps(logdir)
        tps1.append(tps)
        print(shard_cnt, member_cnt, tps)

        account_cnt = 32 * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        tps = util.get_tps(logdir)
        tps2.append(tps)
        print(shard_cnt, member_cnt, tps)

#plt.plot(shards, tps1, "b--", label='204800 accounts',  markersize=20)
#plt.plot(shards, tps2, "g-", label='3276800 accounts',  markersize=20)

y = np.arange(len(shards))  # the label locations
width = 0.4  # the width of the bars

rects1 = plt.barh(y - 0.5*width,   tps1, width, label='204800 accounts')
rects2 = plt.barh(y + 0.5*width,   tps2, width, label='3276800 accounts')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        width = rect.get_width()
        plt.annotate('{:.2f}'.format(width),
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='left', va='center', fontsize=10)
autolabel(rects1)
autolabel(rects2)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.xlabel('Throughput (tx/s)', fontsize=20)
plt.ylabel('Number of Shards', fontsize=20)
plt.yticks( ticks=y, labels=shards,fontsize=20)
plt.xticks([0, 200000, 400000, 600000, 800000], fontsize=20)
# plt.yscale('symlog')
plt.legend(loc=4, fontsize=20)#图例及位置： 1右上角，2 左上角 loc函数可不写 0为最优 ncol为标签有几列

plt.tight_layout()

plt.savefig("rq1-3_shardtps.pdf")
