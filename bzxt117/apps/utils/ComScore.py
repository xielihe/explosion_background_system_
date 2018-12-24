'''
*********************************************************************
文件名称: ComScore.py
所属系统名称: 爆炸系统
功能: 计算物证与各个样本的综合得分
引入函数方式：from modules.ComScore import ComScore
基本思想: 各种模式下只记录匹配程度最高的样本文件，再对各种模式下的得分进行加权求和
执行条件: 得分字典格式无误
输入参数: result -- 得分字典
         格式如{FTIR: [[id, score], [id, score], ...],
                XRD: [[id, score], [id, score], ...],
                XRF:[[id, score], [id, score], ...], ...
                }
返回值: [ 结果代码, score ]   0 —— 成功，其他数值 —— 失败 
                            score -- 综合得分
说明:无
设计者 : 易籽彤
日期: 20181220

*********************************************************************
'''

#主函数
def ComScore(result, score_dict):
    result_one = {}     #仅保留匹配程度最高的样本文件记录

    for key in result:
        if result[key] != []:
            cur_type = result[key]
            cur_type = sorted(cur_type, key = lambda x: x[0])
            max_list = []

        record = cur_type[0]
        for i in cur_type:
            if i[0] == record[0]:
                if i[1] > record[1]:
                    record[1] = i[1]
            else:
                max_list.append(record)
                record = i
        max_list.append(record)
        result_one[key] = max_list

    id_list = []      #提取所有涉及到的id
    for item in result_one.values():
        for i in item:
            id_list.append(i[0])
    id_list = set(id_list)

    for cur_id in id_list:           #计算综合得分，写入score_dict
        FTIR, RAMAN, XRD, XRF, GCMS = [[] for i in range(5)]
        for key in result_one:
            score_list = result_one[key]
            for i in score_list:
                if i[0] == cur_id:
                    if key == 'FTIR':
                        FTIR = i[1]
                    elif key == 'RAMAN':
                        RAMAN = i[1]
                    elif key == 'XRD':
                        XRD = i[1]
                    elif key == 'XRF':
                        XRF = i[1]
                    elif key == 'GCMS':
                        GCMS = i[1]
                    break
        cur_score = ComprehensiveScore(FTIR, RAMAN, XRD, XRF, GCMS)
        score_dict[cur_id] = cur_score
    return '0'


def ComprehensiveScore(FTIR, RAMAN, XRD, XRF, GCMS):
    score_weight = {'FTIR':0.3, 'RAMAN':0.3, 'GCMS': 0.2, 'XRD':0.1, 'XRF':0.1}
    exist_keys = []
    sum_weight = 0
    weight = {}
    if FTIR != []:
        exist_keys.append('FTIR')
        sum_weight += score_weight['FTIR']
    else:
        weight['FTIR'] = 0
        FTIR = 0
        
    if RAMAN != []:
        exist_keys.append('RAMAN')
        sum_weight += score_weight['RAMAN']
    else:
        weight['RAMAN'] = 0
        RAMAN = 0
        
    if GCMS != []:
        exist_keys.append('GCMS')
        sum_weight += score_weight['GCMS']
    else:
        weight['GCMS'] = 0
        GCMS = 0
        
    if XRD != []:
        exist_keys.append('XRD')
        sum_weight += score_weight['XRD']
    else:
        weight['XRD'] = 0
        XRD = 0
        
    if XRF != []:
        exist_keys.append('XRF')
        sum_weight += score_weight['XRF']
    else:
        weight['XRF'] = 0
        XRF = 0
    
    for key in exist_keys:
        weight[key] = score_weight[key]/sum_weight
    score = FTIR*weight['FTIR'] + XRD*weight['XRD'] + RAMAN*weight['RAMAN'] + GCMS*weight['GCMS'] + XRF*weight['XRF']
    return score

