# ECGデータの解析

import matplotlib.pyplot as plt
from function import get_ecg_to_csv, get_rri

# ファイルから心拍データを読み込む(Pandas使用)
# filename = input('データファイルの名前を入力してください: ')
filename = '20200505_130107_379_HB_PW.csv'
data_time, data_ecg = get_ecg_to_csv(filename)

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
j = 3
for i in range(j):
    plt.figure(i)
    plt.plot(data_plot_split[i][0], data_plot_split[i][1])
    plt.title("Raw ECG")
    plt.xlabel("Time [s]")
    plt.ylabel("ECG")
plt.show()
'''

# RR Interval
data_time_x, data_rri = get_rri(data_time, data_ecg)

plt.figure()
plt.plot(data_time_x, data_rri)
plt.title("RR Interval")
plt.xlabel('Time [s]')
plt.ylabel("RRI [s]")
plt.show()
