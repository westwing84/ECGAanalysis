# ECGデータの解析

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

# ファイルから心拍データを読み込む(Pandas使用)
filename = input('データファイルの名前を入力してください: ')
file = pd.read_csv(filename)
data_time_pd = file["timestamp"]
data_ecg = file["ecg"]

# 時間表記をdatetimeオブジェクトに変換
data_time = []
for line in data_time_pd:
    data_time.append(datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f"))

# プロットの開始時間を0sに設定
init_time = 3600 * data_time[0].hour + 60 * data_time[0].minute + data_time[0].second + 0.000001 * float(data_time[0].microsecond)
i = 0
for line in data_time:
    nowtime = 3600 * line.hour + 60 * line.minute + line.second + 0.000001 * float(line.microsecond)
    data_time[i] = nowtime - init_time
    i += 1

# グラフにプロットするためのNumPy配列を用意
data_plot = np.array([data_time, data_ecg])
# データを10秒ごとに分割
j = 0
split_id = []   # 分割する境界のインデックス
for i, line in enumerate(data_plot[0]):
    if int(line) / (j + 1) == 10:
        split_id.append(i)
        j += 1
data_plot_split = np.split(data_plot, split_id, axis=1)

# グラフにプロット
j = 1
for i in range(j):
    plt.figure(i)
    plt.plot(data_plot_split[i][0], data_plot_split[i][1])
    plt.title("Raw ECG")
    plt.xlabel("Time [s]")
    plt.ylabel("ECG")
plt.show()

# RR Interval
data_rri = []
windowsize = 0.5
id1 = 0
data_time_tmp = data_time[data_time <= windowsize]
id2 = len(data_time_tmp)
rwave = max(data_ecg[id1:id2])
ind = np.where(data_ecg[id1:id2] == rwave)
t1 = data_time_tmp[ind]
t = t1 + 0.2
data_time_tmp = data_time[(data_time >= t) and (data_time <= t + windowsize)]
id1 = np.where(data_time == data_time_tmp[0])
id2 = np.where(data_time == data_time_tmp[-1])
rwave = max(data_ecg[id1:id2])
ind = np.where(data_ecg[id1:id2] == rwave)
t2 = data_time_tmp[ind]
data_rri.append(t2 - t1)
t1 = t2
