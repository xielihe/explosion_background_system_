import os
import numpy as np
import math
from scipy.interpolate import interp1d


'''
*********************************************************************
文件名称: CalculateSim.py
所属系统名称: 爆炸系统
功能: 计算各种检测模式下，物证样本与数据库中标准样本的相似度
引入函数方式：from modules.CalculateSim import CalculateSimilarity
基本思想: 利用相关系数以及直方图比对等思想来计算各谱图之间的相似度
执行条件: 文件格式传入无误
输入参数: file_type -- 检测方法（‘GCMS’，‘XRD’，‘XRF’，‘FTIR’，‘RAMAN’）
		 evi_sample_dir -- 物证样本路径（更新时为常见样本路径）
		 common_database -- 标准样本数据库的路径列表，List类型  
		 score_dict -- 空字典，以存储结果   
输出参数: score_dict
返回值:0 —— 成功，其他数值 —— 失败 
说明:无
设计者 : 易籽彤
日期: 20181220
*********************************************************************
'''

#主函数
def CalculateSimilarity(file_type, evi_sample_dir, common_database, score_dict):

    def pearson(signal_1,signal_2):
        n = len(signal_1)
        mean1 = signal_1.mean()
        mean2 = signal_2.mean()
        standvalue1 = math.sqrt(sum((signal_1-mean1)*(signal_1-mean1)))
        standvalue2 = math.sqrt(sum((signal_2-mean2)*(signal_2-mean2)))
        cov = sum((signal_1-mean1)*(signal_2-mean2))
        pearson = cov/(standvalue1*standvalue2)
        pearson = round(pearson*100,2)
        return pearson

    def simple_CalculateSimilarity(evi_sample_dir, common_database, score_dict):
        evi_sample = np.load(evi_sample_dir)
        for file in common_database:
            if os.path.splitext(file):
                common_sample = np.load(file)
                similarity = max(0,  pearson(evi_sample[1], common_sample[1]))
                if similarity >= threshold:
                    sample_id = os.path.splitext(os.path.split(file)[1])[0]
                    sampleFile_id = sample_id[sample_id.index('-')+1:]
                    score_dict[int(sampleFile_id)] = similarity
    
    
#----------------------XRF比对算法--------------------------
    def xrf_similarity(data_common, data_evidence):

        if data_common == {} or data_evidence == {}:
            return 0
        
        hist_1 = []
        hist_2 = []

        for key in data_common.keys():
            hist_1.append(float(data_common[key]))
            if key in data_evidence.keys():
                hist_2.append(float(data_evidence[key]))
            else:
                hist_2.append(0)

        for key in data_evidence.keys():
            if key not in data_common.keys():
                hist_2.append(float(data_evidence[key]))
                hist_1.append(0)

        hist_1 = np.array(hist_1)
        hist_2 = np.array(hist_2)

        hist_1 = hist_1 / sum(hist_1) * 100
        hist_2 = hist_2 / sum(hist_2) * 100

        N = len(hist_1)

        numerator = sum(np.sqrt(hist_1 * hist_2))
        denominator = math.sqrt(hist_1.mean() * hist_2.mean() * N**2)
        
        similarity = 1 - math.sqrt(abs(1 - (numerator/denominator)))
        similarity = round(similarity * 100, 2)
        
        return similarity

    def xrf_CalculateSimilarity(evi_sample_dir,common_database, score_dict):
        weight_dict = {'General Metals':0.2, 'Plastics PVC':0.1, 'Soil':0.2, 'Mining':0.2, 'Mining1':0.2, 'TestAll Geo':0.1}
        evi_sample = np.load(evi_sample_dir).item()
        for file in common_database:
            if os.path.splitext(file)[1] == '.npy':
                weight_sum = 0
                similarity_sum = 0
                common_sample = np.load(file).item()
                cur_similarity_dict = {}
                for key in evi_sample.keys():
                    if key in common_sample.keys():
                        similarity = xrf_similarity(evi_sample[key], common_sample[key])
                        cur_similarity_dict[key] = similarity
                        cur_weight = weight_dict[key]
                        weight_sum += cur_weight
                        similarity_sum += similarity * cur_weight
                if cur_similarity_dict != {}:     #匹配列表为空，则不需要记录
                    sample_id = os.path.splitext(os.path.split(file)[1])[0]
                    sampleFile_id = sample_id[sample_id.index('-')+1:]
                    score_dict[int(sampleFile_id)] = similarity_sum/weight_sum
                    
   #---------------------GCMS比对方法------------------------------  
        #截取比对范围，以便内插
    def cutSearchRange(data_x, data_y, searchRange_l, searchRange_r):
        data_x = list(data_x)
        data_x_view = list(filter(lambda x : x >= searchRange_l and x <= searchRange_r, data_x))
        index_l = data_x.index(data_x_view[0])
        index_r = data_x.index(data_x_view[-1])
        data_y_view = data_y[index_l:index_r+1]  
        return data_x_view, data_y_view

    #计算相似度
    def cosine(signal_1,signal_2):
        n = len(signal_1) 
        in_product = sum(signal_1*signal_2)
        square_1 = math.sqrt(sum(signal_1*signal_1))
        square_2 = math.sqrt(sum(signal_2*signal_2))
        cosine = in_product/(square_1*square_2)
        return cosine

    def GCMS_similarity(data_C, data_M):

        vs_l = max(data_C[0][0], data_M[0][0])     #比对范围的左右边界
        vs_r = min(data_C[0][-1], data_M[0][-1])   

        if data_C[0][0]>data_M[0][0]:     
            reference_x,  reference_y = data_C[0], data_C[1]   
            inter_x, inter_y = data_M[0], data_M[1] 
        else:
            reference_x, reference_y = data_M[0], data_M[1] 
            inter_x, inter_y = data_C[0], data_C[1] 

        reference_x, reference_y = cutSearchRange(reference_x, reference_y, vs_l, vs_r)

        y = interp1d(inter_x, inter_y)
        inter_y = y(reference_x)    #获得内插后的数据

        similarity = cosine(reference_y,inter_y)
        similarity = round(similarity*100,2)
        return similarity

    def gcms_CalculateSimilarity(evi_sample_dir,common_database, score_dict):
        evi_sample = np.load(evi_sample_dir).item()
        evi_retention_time = evi_sample.pop('RetentionTime')


        for file in common_database:
            sample_id = os.path.splitext(os.path.split(file)[1])[0]
            common_data = np.load(file).item()
            retention_time = common_data.pop('RetentionTime')
            for common_key in common_data:
                common_data = common_data[common_key]
            max_sim = 0
            for key in evi_sample:                 
                cur_evi_data = evi_sample[key]
                cur_similarity = GCMS_similarity(cur_evi_data, common_data)
                if cur_similarity > max_sim:
                    max_key = key
                    max_sim = cur_similarity
            sampleFile_id = sample_id[sample_id.index('-')+1:]
            score_dict[int(sampleFile_id)] = {'evi_MS': max_key, 'score': max_sim}
    
#----------------------比对模式选择------------------------
    #更改各检测类型匹配度阈值的接口
    threshold_dict = {'XRD':0, 'RAMAN':0, 'FTIR':0, 'XRF':0, 'GCMS':0}
    
    if file_type == 'XRD' or file_type == 'RAMAN' or file_type == 'FTIR':
        threshold = threshold_dict[file_type]
        simple_CalculateSimilarity(evi_sample_dir, common_database, score_dict)
        return '0'

    if file_type == 'XRF':
        threshold = threshold_dict[file_type]
        xrf_CalculateSimilarity(evi_sample_dir, common_database, score_dict)
        return '0'
    
    if file_type == 'GCMS':
        threshold = threshold_dict[file_type]
        gcms_CalculateSimilarity(evi_sample_dir, common_database, score_dict)
        return '0'
    
    return (print("您输入的数据检测方法有误"))
    

   

