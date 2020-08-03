import numpy as np
import pandas as pd
import datetime
from scipy import interpolate


# csvファイルからECGデータを取得し，時間データとともに配列に格納
def get_ecg_to_csv(filename):
    file = pd.read_csv(filename)
    data_time_pd = file["timestamp"]
    data_ecg = file["ecg"]

    # 時間表記をdatetimeオブジェクトに変換
    data_time = []
    for line in data_time_pd:
        data_time.append(datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f"))

    # プロットの開始時間を0sに設定
    init_time = 3600 * data_time[0].hour + 60 * data_time[0].minute + data_time[0].second + 0.000001 * float(
        data_time[0].microsecond)
    i = 0
    for line in data_time:
        nowtime = 3600 * line.hour + 60 * line.minute + line.second + 0.000001 * float(line.microsecond)
        data_time[i] = nowtime - init_time
        i += 1
    data_time = np.array(data_time)
    return data_time, data_ecg


# ECGの生データからRR間隔を取得
def get_rri(data_time, data_ecg):
    data_rri = []       # RRIのデータを格納
    data_time_x = []    # プロット時の横軸の時間データを格納
    windowsize = 0.5    # R波を認識するための窓幅
    rwave_th = 3500     # R波と認識する閾値
    t_slide = 0.4       # R波の後に無視する時間

    # 最初のR波の時間を算出
    id1 = 0
    data_time_tmp = data_time[data_time <= windowsize]
    id2 = len(data_time_tmp)
    rwave = max(data_ecg[id1:id2])
    ind = np.where(data_ecg[id1:id2] == rwave)
    ind = ind[0][0]
    t1 = data_time_tmp[ind]
    t = t1 + t_slide    # 窓をt_slideだけ移動（T波を無視するため）

    # 次のR波の時間およびRRIの算出
    while t < data_time[-1]:
        data_time_tmp = data_time[(data_time >= t) & (data_time <= t + windowsize)]
        id1 = np.where(data_time == data_time_tmp[0])[0][0]
        id2 = np.where(data_time == data_time_tmp[-1])[0][0]
        rwave = max(data_ecg[id1:id2])
        if rwave < rwave_th:    # 判定されたR波が閾値以下なら無視
            t += windowsize
            continue
        ind = np.where(data_ecg[id1:id2] == rwave)[0][0]
        t2 = data_time_tmp[ind]
        data_rri.append(t2 - t1)
        data_time_x.append(t1)
        t1 = t2
        t = t1 + t_slide
    data_time_x = np.array(data_time_x)

    # データをリサンプリングして間隔を一定にする
    t0 = 1
    tf = int(data_time_x[-1])
    dt = 1      # 時間間隔[s]
    data_time_resample = np.arange(t0, tf + dt, dt)
    f = interpolate.interp1d(data_time_x, data_rri, kind='cubic')   # 補完関数
    data_rri = f(data_time_resample)

    return data_time_resample, data_rri


# RRIのデータからmeanNNを算出
def get_meannn(data_time_resample, data_rri, windowsize):
    t1 = 1
    t2 = t1 + windowsize
    data_meannn = []
    data_time = []
    while t2 <= data_time_resample[-1]:
        ind1 = np.where(data_time_resample == t1)[0][0]
        ind2 = np.where(data_time_resample == t2)[0][0]
        data_rri_tmp = data_rri[ind1:ind2+1]
        data_meannn.append(np.mean(data_rri_tmp))
        data_time.append(np.mean(np.array([t1, t2])))
        t1 = t2
        t2 += windowsize
    data_meannn = np.array(data_meannn)
    data_time = np.array(data_time)

    return data_time, data_meannn


# RRIのデータからSDNNを算出
def get_sdnn(data_time_resample, data_rri, windowsize):
    t1 = 1
    t2 = t1 + windowsize
    data_sdnn = []
    data_time = []
    while t2 <= data_time_resample[-1]:
        ind1 = np.where(data_time_resample == t1)[0][0]
        ind2 = np.where(data_time_resample == t2)[0][0]
        data_rri_tmp = data_rri[ind1:ind2 + 1]
        data_sdnn.append(np.std(data_rri_tmp))
        data_time.append(np.mean(np.array([t1, t2])))
        t1 = t2
        t2 += windowsize
    data_sdnn = np.array(data_sdnn)
    data_time = np.array(data_time)

    return data_time, data_sdnn

