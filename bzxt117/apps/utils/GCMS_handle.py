# coding: utf-8

# In[ ]:


import numpy as np
import math
import os


# 该函数用于处理上传的GCMS文件
# 输入参数：
# sample_name:上传的文件名
# file_in:文件上传到的位置
# file_out_folder:存储处理后文件的文件夹，以.npy格式存入
# 输出：处理后的文件名
def GCMS_handle(sample_name, file_in, file_out_folder):
    file_name = os.path.split(file_in)[1]
    name = os.path.splitext(file_name)[0]
    file_length = len(sample_name)
    flag = file_name.find(sample_name)
    number = name[flag + file_length:]
    numberB = bytes(number, 'utf-8')

    file_out = file_out_folder + '/' + number + '.npy'
    if os.path.exists(file_out):
        os.remove(file_out)

    f = open(file_in, 'rb')
    line = f.readline()
    number_flag = False
    read_flag = False
    line_list = []
    while line:
        if line.find(b'm/z') != -1:
            if line.find(numberB) != -1:
                number_flag = True
        if number_flag and line.find(b'Chromatogram') != -1:
            number_flag = False
            read_flag = False
        if number_flag and line.find(b'Ret.Time') != -1:
            read_flag = True
            line = f.readline()
        if number_flag and read_flag:
            line_tmp = bytes.decode(line)
            if not line_tmp.isspace():
                line_tmp = [float(x) for x in line_tmp.split('\t')]
                line_list.append(line_tmp)
        line = f.readline()
    f.close()
    line_array = np.array(line_list)
    np.save(file_out, line_array)
    os.remove(file_in)
    done_file = number + '.npy'
    return done_file


##计算相似度的主函数
#返回形式：[[id_1,density_1,score_1],[id_2,density_2,score_2],...,[id_n,density_n,score_n]]
def similarity_count(wuzhenEg_folder, changjianEg_folder):

    #计算两个文件夹之间的相似度
    def GCMS_similarity(file1,file2):
        def cosine(signal_1,signal_2):
            n = len(signal_1)
            in_product = sum(signal_1*signal_2)
            square_1 = math.sqrt(sum(signal_1*signal_1))
            square_2 = math.sqrt(sum(signal_2*signal_2))
            cosine = in_product/(square_1*square_2)
            return cosine

        def get_epsilon(data):      #传入向量np.array
            n=len(data)
            data_ave=sum(data)/n
            tmp = sum(1/(data+data_ave))
            epsilon = n/tmp - data_ave
            return epsilon

        def get_signaldata(data, epsilon):
            for i in range(len(data)):
                if data[i] < epsilon:
                    data[i] = 0
                else:
                    data[i] = data[i]-epsilon
            return data

        data_1 = np.load(file1)
        data_x1 = data_1[:,0]
        data_y1 = data_1[:,2]
        epsilon_1 = get_epsilon(data_y1)
        data_y1 = get_signaldata(data_y1, epsilon_1)

        data_2 = np.load(file2)
        data_x2 = data_2[:,0]
        data_y2 = data_2[:,2]
        epsilon_2 = get_epsilon(data_y2)
        data_y2 = get_signaldata(data_y2, epsilon_2)

        if data_x1[0] < data_x2[0]:
            start = data_x2[0]
            startFlag = 1
        else:
            start = data_x1[0]
            startFlag = 2
        if data_x1[-1] < data_x2[-1]:
            over = data_x1[-1]
            overFlag = 2
        else:
            over = data_x2[-1]
            overFlag = 1

        data_tmp = (data_x1, data_x2)
        stIdx = np.where(data_tmp[startFlag-1]==start)[0][0]
        ovIdx = np.where(data_tmp[overFlag-1]==over)[0][0]

        stIdxTmp, ndIdxTmp = 0, len(data_y1)
        if(startFlag==1): stIdxTmp = stIdx
        if(overFlag==1): ndIdxTmp = ovIdx+1
        signal_1 = data_y1[stIdxTmp:ndIdxTmp]

        stIdxTmp, ndIdxTmp = 0, len(data_y2)
        if(startFlag==2): stIdxTmp = stIdx
        if(overFlag==2): ndIdxTmp = ovIdx+1
        signal_2 = data_y2[stIdxTmp:ndIdxTmp]

        similarity = cosine(signal_1, signal_2)

        return similarity

    # 管理特征离子与TIC的权值，可继续进行添加
    def feature_weight(newFeature='', newWeight=''):
        feature = [['91', '105', '119', '128', '134', '142', '85', '82', '83', 'TIC'], ['85', '82', '83', 'TIC'], ['178', '182', '91', 'TIC']]
        weight = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]]
        if newFeature and len(newFeature)==len(newWeight):
            feature.append(newFeature)
            weight.append(newWeight)
        return feature, weight

    # 获取特征离子与TIC的权值，如果查询不到则平均分配权值
    def get_weight(cur_feature):
        n = len(cur_feature)
        feature, weight = feature_weight()

        for i in range(len(feature)):
            if sorted(cur_feature)==sorted(feature[i]):
                return weight[i]
                break
        return [1/n]*n


    wuzheng_feature_list = os.listdir(wuzhenEg_folder)
    type_id_list = os.listdir(changjianEg_folder)

    similarity_result = []

    #分别计算每种助燃剂下的相似度
    for type_id in type_id_list:
        cur_type_dir = os.path.join(changjianEg_folder,type_id)
        if type_id != '.ipynb_checkpoints' and type_id != 'handled' and os.path.isdir(cur_type_dir):
            print(cur_type_dir)
            density_list = os.listdir(cur_type_dir)
            each_density_sim = []
            #分别计算该种类助燃剂在每个浓度下的相似度
            for density in density_list:
                cur_compare = os.path.join(cur_type_dir, density)
                cur_feature_list = os.listdir(cur_compare)
                feature = [os.path.splitext(x)[0] for x in cur_feature_list]
                if '.ipynb_checkpoints' in feature:
                    feature.remove('.ipynb_checkpoints')
                weight = get_weight(feature)
                cur_similarity = []
                #计算所有谱图（包括特征离子与TIC）之间的相似度
                for item in feature:
                    for cur_feature in cur_feature_list:
                        if os.path.splitext(cur_feature)[1]=='.npy' and os.path.splitext(cur_feature)[0] == item:
                            file2 = os.path.join(cur_compare,cur_feature)
                            for wuzheng_feature in wuzheng_feature_list:
                                if os.path.splitext(wuzheng_feature)[1] == '.npy' and os.path.splitext(wuzheng_feature)[0] == item:
                                    file1 = os.path.join(wuzhenEg_folder,wuzheng_feature)
                                    feature_similarity = GCMS_similarity(file1,file2)
                                    cur_similarity.append(feature_similarity)
                cur_similarity = np.array(cur_similarity)
                weight = np.array(weight)
                sum_similarity = sum(cur_similarity*weight)
                each_density_sim.append(sum_similarity)
                cur_result = [type_id, density, sum_similarity]
                similarity_result.append(cur_result)

            each_density_sim = np.array(each_density_sim)
            type_sim = sum(each_density_sim)/len(each_density_sim)
    similarity_result = sorted(similarity_result, key=lambda similarity_result: similarity_result[2], reverse=True)
    return similarity_result[:5]


