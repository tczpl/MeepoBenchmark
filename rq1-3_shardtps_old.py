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

x = np.arange(len(shards))  # the label locations
width = 0.4  # the width of the bars

rects1 = plt.bar(x - 0.5*width,   tps1, width, label='204800 accounts')
rects2 = plt.bar(x + 0.5*width,   tps2, width, label='3276800 accounts')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)
autolabel(rects1)
autolabel(rects2)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Throughput (tx/s)', fontsize=20)
plt.xlabel('Number of Shards', fontsize=20)
plt.xticks( ticks=x, labels=shards,fontsize=20)
plt.yticks(fontsize=20)
# plt.yscale('symlog')
plt.legend(fontsize=20)

plt.tight_layout()

plt.savefig("rq1-3_shardtps.pdf")
