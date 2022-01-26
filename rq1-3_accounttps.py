import util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.grid(True, color='#666666', linestyle = ":", linewidth = "2")

shards = [2,4,8,16,32,64,128]
bases = [2,4, 8,16,32]
all_tps_s = []
shard_cnt = 32
member_cnt = 4

for account_base in bases:
    account_cnt = account_base * 102400
    logdir = "meepo128/"+str(shard_cnt)+"x"+str(member_cnt)+"_erc20_transfer8192*500of"+str(account_cnt)
    all_tps = util.get_all_tps(logdir)
    all_tps_s.append(all_tps)
    print(shard_cnt, member_cnt, len(all_tps))

min_len = 9999
for all_tps in all_tps_s:
    if len(all_tps)< min_len:
        min_len = len(all_tps)

x = np.arange(min_len)

lines = ["r-","g--","b-","c-","m--"]

for i in range(len(bases)):
    account_base = bases[i]
    account_cnt = account_base * 102400
    plt.plot(x, all_tps_s[i][:min_len], lines[i], label=str(account_cnt)+' accounts',  markersize=20)

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Throughput (tx/s)', fontsize=20)
plt.xlabel('Time (s)', fontsize=20)
plt.xticks([120, 200,300,400,500,600],fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(120,)
plt.ylim(100000,200000)
plt.legend(fontsize=15)

plt.tight_layout()

import sys
plt.savefig(sys.argv[0][:-3]+".pdf")
plt.savefig("png/"+sys.argv[0][:-3]+".png")
