from modules.PreProcess测试 import preProcess
import os
import numpy as np
import math
from scipy.interpolate import interp1d

#相似度比对函数，物证与常见样本通用
'''
输入参数说明：
      file_type: 检测方法（字符串形式）
      evi_sample_dir: 物证样本路径（更新时为常见样本路径）
      common_database: 常见样本数据的路径列表     
'''
def CountSimilarity(file_type, evi_sample_dir, common_database):

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

    def simple_CountSimilarity(evi_sample_dir, common_database):
        score_dict = {}
        evi_sample = np.load(evi_sample_dir)
        for file in common_database:
            if os.path.splitext(file):
                common_sample = np.load(file)
                similarity = max(0,  pearson(evi_sample[1], common_sample[1]))
                if similarity >= threshold:
                    score_dict[os.path.splitext(file)[0]] = similarity
                
        return score_dict
    
    
#----------------------XRF比对算法--------------------------
    #两条数据计算相似度
    #eff_ele_1,eff_ele_2的形式均为[[ele_1,num_1],[ele_2,num_2]...[ele_n,num_n]]
    #遍历的算法之后再写
    def xrf_similarity(Sample_common, Sample_evidence): 

        eff_ele_1 = Sample_common.copy()
        eff_ele_2 = Sample_evidence.copy()
        if eff_ele_1==[] or eff_ele_2==[]:
            return 0

        common_ele = []
        common_differ = 0
        common_mutual = 0

        i = 0
        while i<len(eff_ele_1):
            cur_ele_1 = eff_ele_1[i][0]
            j=0
            flag_common = False
            while j<len(eff_ele_2):
                cur_ele_2 = eff_ele_2[j][0]
                if cur_ele_1 == cur_ele_2:
                    common_ele.append(cur_ele_1)
                    content_1 = float(eff_ele_1[i][1])
                    content_2 = float(eff_ele_2[j][1])
                    common_differ += (content_1-content_2)*(content_1-content_2)
                    common_mutual += content_1*content_1+content_2*content_2-content_1*content_2
                    eff_ele_1.pop(i)
                    eff_ele_2.pop(j)
                    flag_common = True
                else:
                    j = j+1
            if flag_common == False:
                i = i+1

        #计算不同元素的平方       
        differ_product = 0         
        for k in range(0,len(eff_ele_1)):
            differ_product += float(eff_ele_1[k][1])*float(eff_ele_1[k][1])
        for m in range(0,len(eff_ele_2)):
            differ_product += float(eff_ele_2[m][1])*float(eff_ele_2[m][1])

        #计算相似度
        similarity = 1-(common_differ+differ_product)/(common_mutual+differ_product)
        similarity = round(similarity*100,2)
        return similarity
    def xrf_CountSimilarity(evi_sample_dir,common_database):
        evi_sample = np.load(evi_sample_dir).item()
        sample_similarity = {}
        for file in common_database:
            if os.path.splitext(file)[1] == '.npy':
                common_sample = np.load(file).item()
                cur_similarity_dict = {}
                for key in evi_sample.keys():
                    if key in common_sample.keys():
                        similarity = xrf_similarity(evi_sample[key], common_sample[key])
                        cur_similarity_dict[key] = similarity
                if cur_similarity_dict != {}:     #匹配列表为空，则不需要记录
                    sample_similarity[os.path.splitext(file)[0]] = cur_similarity_dict
        return sample_similarity

#----------------------比对模式选择------------------------
    #更改各检测类型匹配度阈值的接口
    threshold_dict = {'XRD':20, 'RAMAN':50, 'FTIR':50, 'XRF': 20}
    
    if file_type == 'XRD' or file_type == 'RAMAN' or file_type == 'FTIR':
        threshold = threshold_dict[file_type]
        score_dict = simple_CountSimilarity(evi_sample_dir, common_database)
        return score_dict

    if file_type == 'XRF':
        threshold = threshold_dict[file_type]
        score_dict = xrf_CountSimilarity(evi_sample_dir, common_database)
        return score_dict
    
    return (print("您输入的数据检测方法有误"))
    

   

