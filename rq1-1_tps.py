import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

to_draw = []
for member_cnt in [1, 2, 3, 4]:
    to_draw.append([])
    for shard_cnt in [2, 4, 8, 16, 32]:
        account_cnt = shard_cnt * 102400
        logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
        tps = util.get_tps(logdir)
        to_draw[-1].append(tps)
        print(shard_cnt, member_cnt, tps)



labels = ['2', '4', '8', '16', '32']


x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars


rects1 = plt.bar(x - 1.5*width,   to_draw[0], width, label='1 member')
rects2 = plt.bar(x - 0.5*width,           to_draw[1], width, label='2 members')
rects3 = plt.bar(x + 0.5*width,            to_draw[2], width, label='3 members')
rects4 = plt.bar(x + 1.5*width,  to_draw[3], width, label='4 members')

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Throughput (tx/s)', fontsize=20)
plt.xlabel('Number of Shards', fontsize=20)
plt.xticks(ticks=x, labels=labels, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)

plt.tight_layout()

plt.savefig("rq1-1_tps.pdf")
