# ECGデータの解析

import numpy as np
import matplotlib.pyplot as plt
import function

# ファイルから心拍データを読み込む(Pandas使用)
# filename = input('データファイルの名前を入力してください: ')
filename = '20200505_130107_379_HB_PW.csv'
data_time, data_ecg = function.get_ecg_to_csv(filename)

'''
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
    plt.ylabel("ECG [μV]")
plt.show()
'''

# RR Interval
data_time_resample, data_rri = function.get_rri(data_time, data_ecg)
'''
plt.figure()
plt.plot(data_time_resample, data_rri)
# plt.xlim(0, 1000)
plt.title("RR Interval")
plt.xlabel('Time [s]')
plt.ylabel("RRI [s]")
plt.show()
'''
# meanNN
data_time_x, data_meannn = function.get_meannn(data_time_resample, data_rri, windowsize=180, slide=5)
plt.figure()
plt.subplot(4, 1, 1)
plt.plot(data_time_x, data_meannn)
# plt.xlim(0, 1000)
plt.ylim(0.6, 1.2)
plt.title("meanNN")
plt.xlabel('Time [s]')
plt.ylabel("meanNN [s]")

# SDNN
data_time_x, data_sdnn = function.get_sdnn(data_time_resample, data_rri, windowsize=180, slide=5)
plt.subplot(4, 1, 2)
plt.plot(data_time_x, data_sdnn)
# plt.xlim(0, 1000)
plt.ylim(0, 0.2)
plt.title("SDNN")
plt.xlabel('Time [s]')
plt.ylabel("SDNN [s]")

# RMSSD
data_time_x, data_rmssd = function.get_rmssd(data_time_resample, data_rri, windowsize=180, slide=5)
plt.subplot(4, 1, 3)
plt.plot(data_time_x, data_rmssd)
# plt.xlim(0, 1000)
plt.ylim(0, 0.2)
plt.title("RMSSD")
plt.xlabel('Time [s]')
plt.ylabel("RMSSD [s]")

# NN50
data_time_x, data_nn50 = function.get_nn50(data_time_resample, data_rri, windowsize=180, slide=5)
plt.subplot(4, 1, 4)
plt.plot(data_time_x, data_nn50)
# plt.xlim(0, 1000)
# plt.ylim(0, 0.2)
plt.title("NN50")
plt.xlabel('Time [s]')
plt.ylabel("NN50")

plt.tight_layout()
plt.show()

