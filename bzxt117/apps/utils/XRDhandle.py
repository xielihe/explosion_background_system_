# coding: utf-8

# In[55]:


import numpy as np
import matplotlib.pyplot as plt
import math
import os


# xrd谱图预处理，并存入./handled文件夹
# data_id:原始谱图id
# data_file:原始谱图路径
# return:预处理后谱图存入的路径
def preprocess(data_id, data_file,handled_dir,handled111):
    # print(os.getcwd())#F:\毕设\bishe430
    def Gaussian_smooth(data):
        smooth = []
        odata = data[:]
        n = len(data)
        for i in range(2):
            odata.insert(0, odata[0])
            odata.insert(n, odata[n - 1])

        gaussian_kernel = np.mat([1, 4, 6, 4, 1]).T

        for i in range(n):
            data_tmp = [odata[i - 2], odata[i - 1], odata[i], odata[i + 1], odata[i + 2]]
            data_mat = np.mat(data_tmp)
            data_smooth = data_mat * gaussian_kernel
            data_smooth = float(data_smooth) / 16
            smooth.append(data_smooth)
        return smooth

    def get_epsilon(data):  # 传入向量np.array
        n = len(data)
        data_ave = sum(data) / n
        tmp = sum(1 / (data + data_ave))
        epsilon = n / tmp - data_ave
        return epsilon

    def get_signaldata(data, epsilon):
        for i in range(len(data)):
            if data[i] < epsilon:
                data[i] = 0
            else:
                data[i] = data[i] - epsilon
        return data

    f = open(data_file,'r')  # 读取txt文件
    data = np.loadtxt(f)
    data_x = data[:, 0]
    data_y = data[:, 1]

    y = data_y[:].tolist()  # 5点高斯平滑2次
    smooth_1 = Gaussian_smooth(y)
    smooth_2 = Gaussian_smooth(smooth_1)

    data = np.array(smooth_2)  # 忽略噪声点
    epsilon = get_epsilon(data)
    main_signal = get_signaldata(data, epsilon)

    data_id = str(data_id)
    handled_dir = os.path.join(handled_dir, data_id + '.txt')
    np.savetxt(handled_dir, [data_x, main_signal])
    return os.path.join(handled111,"handled", data_id + '.txt')


# 计算相似度
# test_txt:待测谱图在handled下的路径
# sample_file:样本谱图的handled文件夹
# return:返回前十的[id,score]
def similarity_rank(test_txt, sample_file):
    def pearson(txt_1, txt_2):
        signal_1 = np.loadtxt(txt_1)[1]
        print(signal_1)
        signal_2 = np.loadtxt(txt_2)[1]
        print(signal_2)
        n = len(signal_1)
        mean1 = signal_1.mean()
        mean2 = signal_2.mean()
        standvalue1 = math.sqrt(sum((signal_1 - mean1) * (signal_1 - mean1)))
        standvalue2 = math.sqrt(sum((signal_2 - mean2) * (signal_2 - mean2)))
        cov = sum((signal_1 - mean1) * (signal_2 - mean2))
        pearson = cov / (standvalue1 * standvalue2)
        return pearson

    score = []
    all_file = os.listdir(sample_file)
    for i in range(0, len(all_file)):
        if os.path.splitext(all_file[i])[1] == '.txt':
            cur_path = os.path.join(sample_file, all_file[i])
            cur_txt = all_file[i]
            txt_id = os.path.splitext(cur_txt)[0]
            cur_score = pearson(test_txt, cur_path)
            score.append([txt_id, cur_score])
    score = sorted(score, key=lambda score: score[1], reverse=True)
    return score[:10]

