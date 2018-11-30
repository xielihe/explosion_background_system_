# coding: utf-8

# In[1]:


import xlrd
import numpy as np


def xls_process(xls_file):
    # xls_file：原始excel表格路径
    # 将上传的excel表格提取出来
    # 返回[[type1,[ele1_1,num1_1],[ele1_2,num1_2]...[ele1_n,num1_n]],[type2,[ele2_1,num2_1],[ele2_2,num2_2]...[ele2_n,num2_n]]]...
    # 分type存储下来
    def read(file, sheet_index=0):
        workbook = xlrd.open_workbook(file)

        sheet = workbook.sheet_by_index(sheet_index)
        print("工作表名称:", sheet.name)
        print("行数:", sheet.nrows)
        print("列数:", sheet.ncols)

        data = []
        for i in range(0, sheet.nrows):
            data.append(sheet.row_values(i))
        return data

    def extract_element(data, element_name):
        cur_data = data

        model = cur_data[0]
        effective_element = [model]
        element = cur_data[1::2]
        error = cur_data[2::2]

        for i in range(0, len(element)):
            if element[i] != '<LOD' and element[i] > 3 * error[i]:
                effective_element.append([element_name[i], element[i]])
        return effective_element

    all_data = read(xls_file)
    record = []
    # 去掉不需要的数据
    for i in range(0, len(all_data[0])):
        cur_data = all_data[0][i]
        if cur_data == 'Type':
            record.append(i)
        if cur_data.find('Error') != -1:
            record.append(i - 1)
            record.append(i)
    data_array = np.array(all_data)
    data_inneed = data_array[:, record]
    # 去掉不用考虑的模式
    j = 0
    record = [0]
    while j < len(data_inneed):
        cur_type = data_inneed[j][0]
        if (cur_type.find('Metal') != -1) or (cur_type.find('Plastics') != -1) or (cur_type.find('Soil') != -1) or (
                cur_type.find('Mining') != -1):
            record.append(j)
        j = j + 4
    data_final = data_inneed[record, :]
    element_name = data_final[0][1::2]
    effective_ele_set = []
    for k in range(1, len(data_final)):
        cur = data_final[k]
        cur_effective_ele = extract_element(cur, element_name)
        effective_ele_set.append(cur_effective_ele)

    return effective_ele_set


# xrf_test:待测物证数据
# [type,[ele_1,num_1],[ele_2,num_2]...[ele_n,num_n]]
# xrf_sample_list:遍历某一模式下的所有样本
# [[[ele_1,num_1],[ele_2,num_2]...[ele_n,num_n],id],[[ele_1,num_1],[ele_2,num_2]...[ele_n,num_n],id],...,[[ele_1,num_1],[ele_2,num_2]...[ele_n,num_n],id]]
# return score_top10:返回前十的id以及相似度score
# [[id_top1,score_top1],[id_top2,score_top2],...,[id_top10,score_top10]]
def xrf_rank(xrf_test, xrf_sample_list):
    def xrf_similarity(eff_ele_1, eff_ele_2):
        if eff_ele_1 == [] or eff_ele_2 == []:
            return 0

        common_ele = []
        common_differ = 0
        common_mutual = 0

        i = 0
        while i < len(eff_ele_1):
            cur_ele_1 = eff_ele_1[i][0]
            j = 0
            flag_common = False
            while j < len(eff_ele_2):
                cur_ele_2 = eff_ele_2[j][0]
                if cur_ele_1 == cur_ele_2:
                    common_ele.append(cur_ele_1)
                    content_1 = float(eff_ele_1[i][1])
                    content_2 = float(eff_ele_2[j][1])
                    common_differ += (content_1 - content_2) * (content_1 - content_2)
                    common_mutual += content_1 * content_1 + content_2 * content_2 - content_1 * content_2
                    eff_ele_1.pop(i)
                    eff_ele_2.pop(j)
                    flag_common = True
                else:
                    j = j + 1
            if flag_common == False:
                i = i + 1

        # 计算不同元素的平方
        differ_product = 0
        for k in range(0, len(eff_ele_1)):
            differ_product += float(eff_ele_1[k][1]) * float(eff_ele_1[k][1])
        for m in range(0, len(eff_ele_2)):
            differ_product += float(eff_ele_2[m][1]) * float(eff_ele_2[m][1])

        # 计算相似度
        similarity = 1 - (common_differ + differ_product) / (common_mutual + differ_product)
        return similarity

    def xrf_top10(score):
        score_sort = sorted(score, key=lambda score: score[1], reverse=True)
        score_top10 = score_sort[:10]
        return score_top10

    score_list = []
    cur_type = xrf_test[0]

    for i in range(0, len(xrf_sample_list)):
        cur_test_value = xrf_test[1:].copy()
        cur_sample = xrf_sample_list[i]
        cur_sample_id = cur_sample[-1]
        cur_sample_value = cur_sample[0:-1]

        cur_score = xrf_similarity(cur_test_value, cur_sample_value)
        score_list.append([cur_sample_id, cur_score])

    score_top10 = xrf_top10(score_list)
    return score_top10

