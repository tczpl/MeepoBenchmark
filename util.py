import glob
from os import ctermid
import time

from numpy import allclose

def get_tps(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_timestamps = []

    for log in logs:
        txs = []
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)


        all_txs.append(txs)
        all_timestamps.append(timestamps)
    
    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        for txs in all_txs:
            sum_of_txs += txs[i]
        #if duration!=0:
            #print(logdir, end, sum_of_txs, duration, sum_of_txs/duration)
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)
    tps = sum_of_txs/duration
    
    return tps



def get_all_tps(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_timestamps = []

    print(logdir, len(logs))

    for log in logs:
        txs = []
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)


        all_txs.append(txs)
        all_timestamps.append(timestamps)
    
    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    all_tps = []
    sum_of_txs = 0
    for i in range(begin, 9999):
        duration_window = 120
        end = i
        for txs in all_txs:
            sum_of_txs += txs[i]
            
        
        ## all_tps
        this_sum_of_txs = 0
        for this_begin in range(i, -1 ,-1):
            duration = timestamps[end] - timestamps[this_begin]
            for txs in all_txs:
                this_sum_of_txs += txs[this_begin]
            if duration > duration_window:
                tps = this_sum_of_txs/duration
                all_tps.append(tps)
                break

        #finish
        if sum_of_txs > sum_target:
            break
        
    """
    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        for txs in all_txs:
            sum_of_txs += txs[i]
        #if duration!=0:
            #print(logdir, end, sum_of_txs, duration, sum_of_txs/duration)
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)
        if duration>0:
            tps = sum_of_txs/duration
            all_tps.append(tps)
    """
    
    return all_tps


def get_avg_latency(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_timestamps = []

    for log in logs:
        txs = []
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)


        all_txs.append(txs)
        all_timestamps.append(timestamps)
    


    logs = glob.glob(logdir+"/peerC_*.log")

    all_C_timestamps = []

    for log in logs:
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            # 2022-01-23 22:28:36 "" Block #48(0x3c5b…5201) commited
            if len(array)==6 and array[5]=="commited":
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)
        all_C_timestamps.append(timestamps)

    # print(all_C_timestamps)

    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    sum_of_delay = 0
    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        
        confirmed_timestamps = timestamps[i]    
        for C_timestamps in all_C_timestamps:
            if C_timestamps[i]>confirmed_timestamps:
                confirmed_timestamps = C_timestamps[i]

        for txs in all_txs:
            sum_of_txs += txs[i]
            sum_of_delay += txs[i]*(confirmed_timestamps-timestamps[i-1])/2

        #if duration!=0:
            #print(logdir, end, sum_of_txs, duration, sum_of_txs/duration)
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)
    avg_latency = sum_of_delay/sum_of_txs
    
    return avg_latency


def get_all_latency(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_timestamps = []

    for log in logs:
        txs = []
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)


        all_txs.append(txs)
        all_timestamps.append(timestamps)
    


    logs = glob.glob(logdir+"/peerC_*.log")

    all_C_timestamps = []

    for log in logs:
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            # 2022-01-23 22:28:36 "" Block #48(0x3c5b…5201) commited
            if len(array)==6 and array[5]=="commited":
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)
        all_C_timestamps.append(timestamps)

    # print(all_C_timestamps)

    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    all_latency = []
    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        
        confirmed_timestamps = timestamps[i]    
        for C_timestamps in all_C_timestamps:
            if C_timestamps[i]>confirmed_timestamps:
                confirmed_timestamps = C_timestamps[i]

        for txs in all_txs:
            sum_of_txs += txs[i]
            all_latency.append( (confirmed_timestamps-timestamps[i-1])/2 )

        #if duration!=0:
            #print(logdir, end, sum_of_txs, duration, sum_of_txs/duration)
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)
    return all_latency





def get_blockkb(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_blockkbs = []
    all_timestamps = []

    for log in logs:
        txs = []
        blockkbs = []
        timestamps = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))

                blockkbs.append(float(array[-2]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)


        all_txs.append(txs)
        all_blockkbs.append(blockkbs)
        all_timestamps.append(timestamps)
    
    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    sum_of_blockkbs = 0
    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        for txs in all_txs:
            sum_of_txs += txs[i]
        for blockkbs in all_blockkbs:
            sum_of_blockkbs += blockkbs[i]
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)
    avg_blockkb = sum_of_blockkbs/end
    
    return avg_blockkb




def get_crosstime(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_blockkbs = []
    all_timestamps = []
    all_crosstimes = []

    for log in logs:
        txs = []
        blockkbs = []
        timestamps = []
        crosstimes = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))

                blockkbs.append(float(array[-2]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)
                
            # 2022-01-23 22:29:32 "" block=0x5c9f…5e81, stat_root=0x2f12…67dc, cross_time_ms=401 epoch_number=1
            if len(array)==7 and array[5][:13] == "cross_time_ms":
                crosstime = int(array[5][14:])
                crosstimes.append(crosstime)


        all_txs.append(txs)
        all_blockkbs.append(blockkbs)
        all_timestamps.append(timestamps)
        all_crosstimes.append(crosstimes)
    

    logs = glob.glob(logdir+"/peerC_*.log")

    all_C_crosstimes = []

    for log in logs:
        crosstimes = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)==7 and array[5][:13] == "cross_time_ms":
                crosstime = int(array[5][14:])
                crosstimes.append(crosstime)
        all_C_crosstimes.append(crosstimes)


    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    sum_of_crosstimes = 0
    timestamps = all_timestamps[0]

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        for txs in all_txs:
            sum_of_txs += txs[i]
        for crosstimes in all_crosstimes:
            sum_of_crosstimes += crosstimes[i]
        for crosstimes in all_C_crosstimes:
            sum_of_crosstimes += crosstimes[i]
             
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)

    print(sum_of_crosstimes, )
    avg_crosstime = (sum_of_crosstimes/end) / (len(all_crosstimes)+len(all_C_crosstimes))
    
    return avg_crosstime




def get_all_crosstime(logdir):

    logs = glob.glob(logdir+"/peer_*.log")

    all_txs = []
    all_blockkbs = []
    all_timestamps = []
    all_crosstimes = []

    for log in logs:
        txs = []
        blockkbs = []
        timestamps = []
        crosstimes = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)>4 and array[3]=="Imported" and array[4] !="sealed":
                txs.append(int(array[6][1:]))

                blockkbs.append(float(array[-2]))
                
                time_array = time.strptime(array[0]+" "+array[1] , "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(time_array))
                timestamps.append(timestamp)
                
            # 2022-01-23 22:29:32 "" block=0x5c9f…5e81, stat_root=0x2f12…67dc, cross_time_ms=401 epoch_number=1
            if len(array)==7 and array[5][:13] == "cross_time_ms":
                crosstime = int(array[5][14:])
                crosstimes.append(crosstime)


        all_txs.append(txs)
        all_blockkbs.append(blockkbs)
        all_timestamps.append(timestamps)
        all_crosstimes.append(crosstimes)
    

    logs = glob.glob(logdir+"/peerC_*.log")

    all_C_crosstimes = []

    for log in logs:
        crosstimes = []
        lines = open(log).readlines()
        for line in lines:
            array = line.strip().split(" ")
            if len(array)==7 and array[5][:13] == "cross_time_ms":
                crosstime = int(array[5][14:])
                crosstimes.append(crosstime)
        all_C_crosstimes.append(crosstimes)


    begin = 9999
    end = 9999
    for txs in all_txs:
        for i in range(len(txs)):
            if txs[i] > 10:
                if i < begin:
                    begin = i

    sum_of_txs = 0
    all_crosstime = []

    sum_target = int(logdir.split("/")[1].split("x")[0]) * 100000000 / 32
    if "shop" in logdir:
        sum_target = int(logdir.split("/")[1].split("x")[0]) * 8000*50
    
    duration = 0

    for i in range(begin, 9999):
        end = i
        duration = timestamps[end] - timestamps[begin]
        for txs in all_txs:
            sum_of_txs += txs[i]
        for crosstimes in all_crosstimes:
            all_crosstime.append(crosstimes[i])
        for crosstimes in all_C_crosstimes:
            all_crosstime.append(crosstimes[i])
             
        if sum_of_txs > sum_target:
            break
        # print(sum_of_txs, sum_target)

    return all_crosstime