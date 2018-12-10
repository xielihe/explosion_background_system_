#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import math
import numpy as np
from scipy.interpolate import interp1d
from scipy import sparse
from scipy.sparse.linalg import spsolve
import xlrd
import csv 

#该模块为谱图预处理模块
#输入参数：检测方法file_type，文件路径file，处理后文件存储位置out_folder，
#               如果是GCMS，file为文件夹路径，且还需输入该样本名称sample_name和burning_degree
#示例输入：preProcess('GCMS', '2#万煤油83.txt', './handled/GCMS_handled', '2#万煤油')
#错误检测：若输入的检测方法有误则报错
#输出：处理后的文件路径

def preProcess(file_type, file, out_folder, sample_name='', burning_degree=''):
       
    #去除基线
    def baseline_als(y, lam, p, niter=10):    #计算基线
        s  = len(y)                                                                                               
        # assemble difference matrix                                                                              
        D0 = sparse.eye( s )                                                                                     
        d1 = [np.ones( s-1 ) * -2]                                                                             
        D1 = sparse.diags( d1, [-1] )                                                                             
        d2 = [ np.ones( s-2 ) * 1]                                                                             
        D2 = sparse.diags( d2, [-2] )                                                                             

        D  = D0 + D2 + D1                                                                                         
        w  = np.ones( s )                                                                                         
        for i in range( niter ):                                                                                  
            W = sparse.diags( [w], [0] )                                                                          
            Z =  W + lam*D.dot( D.transpose() )                                                                   
            z = spsolve( Z, w*y )                                                                                 
            w = p * (y > z) + (1-p) * (y < z)   
        return z

    #平滑操作
    def Gaussian_smooth(data):    
        smooth = []
        odata = data[:]
        n = len(data)
        for i in range(2):
            odata.insert(0,odata[0])
            odata.insert(n,odata[n-1])

        gaussian_kernel = np.mat([1,4,6,4,1]).T

        for i in range(n):
            data_tmp = [odata[i], odata[i+1], odata[i+2], odata[i+3], odata[i+4]]
            data_mat = np.mat(data_tmp)
            data_smooth = data_mat * gaussian_kernel
            data_smooth = float(data_smooth)/16
            smooth.append(data_smooth)
        return smooth
        
    #线性内插模块
    def interpolation(x ,y ,xbegin, xend):   
        f = interp1d(x, y)
        xnew = np.linspace(xbegin, xend, num=(xend-xbegin+1), endpoint=True)   
        return xnew, f(xnew)
    
        #读取特征离子色谱图csv
    def ReadFeatureFile(infile): 
        GCMS_file = open(infile, encoding='gbk')
        lines = csv.reader(GCMS_file)

        feature_list = {}
        cur_feature = []
        data_flag = False

        for line in lines:
            if '离子' in line[0]:
                data_flag = True
                if cur_feature:
                    cur_feature = np.array(cur_feature)
                    cur_feature = np.array(cur_feature)
                    data_x = cur_feature[:,0]
                    data_y = cur_feature[:,1]
                    feature_list[feature_id] = [data_x,data_y]
                cur_feature = []
                index_b = line[0].index('离子')
                index_e = line[0].index('(')      
                feature_id = line[0][index_b+2:index_e-1]
                feature_id = str(int(float(feature_id)))   #去掉后面的小数点
                continue
            if data_flag: 
                line = [float(x) for x in line]
                cur_feature.append(line)

        GCMS_file.close()
        return feature_list

    #读取总离子色谱图csv
    def ReadTICFile(infile):    
        GCMS_file = open(infile, encoding='gbk')

        data_flag = False
        TIC = []

        lines = csv.reader(GCMS_file)
        for line in lines:
            if 'TIC' in line[0]: 
                data_flag = True
                continue
            if data_flag:
                line = [float(x) for x in line if x]
                TIC.append(line)

        TIC = np.array(TIC)
        TIC_x = TIC[:,0]
        TIC_y = TIC[:,1]
        TIC = {'TIC':[TIC_x, TIC_y]}
        GCMS_file.close()
        return TIC

    #----------XRD预处理------------
    def xrdPreProcess(file):
        data = np.loadtxt(file)
        data_x = data[:,0]
        data_y = data[:,1]
        data_y = data_y.tolist()
        #平滑
        data_smooth = Gaussian_smooth(data_y)
        #去基线
        baseline = baseline_als(data_smooth, 100000, 0.06)
        data_y_nobaseline = np.maximum(0,data_smooth-baseline)
        return [data_x,data_y_nobaseline]

 #--------XRF预处理-------------
    def xrfPreProcess(file):

        def read(file, sheet_index=0):
            workbook = xlrd.open_workbook(file)

            sheet = workbook.sheet_by_index(sheet_index)
            data = []
            for i in range(0, sheet.nrows):
                data.append(sheet.row_values(i))
            return data

        def extract_element(data, element_name):
            cur_data = data

            model = cur_data[0]
            effective_element = []
            element = cur_data[1::2]
            error = cur_data[2::2]

            for i in range(0,len(element)):
                if element[i]!='<LOD' and element[i]>3*error[i]:
                    effective_element.append([element_name[i],element[i]])
            return model, effective_element


        all_data = read(file)
        record = []
        #去掉不需要的数据
        for i in range(0,len(all_data[0])):       
            cur_data = all_data[0][i]
            if cur_data == 'Type':
                record.append(i)
            if cur_data.find('Error') != -1:
                record.append(i-1)
                record.append(i)
        data_array = np.array(all_data)
        data_inneed = data_array[:,record]
        #去掉不用考虑的模式
        j = 0
        record = [0]
        while j < len(data_inneed):    
            cur_type = data_inneed[j][0]
            if (cur_type.find('Metal')!=-1) or (cur_type.find('Plastics')!=-1) or (cur_type.find('Soil')!=-1) or (cur_type.find('Mining')!=-1):
                record.append(j)
            j = j+4
        data_final = data_inneed[record,:]
        element_name = data_final[0][1::2]
        effective_ele_set = {}
        for k in range(1,len(data_final)):
            cur = data_final[k] 
            model, cur_effective_ele = extract_element(cur, element_name)
            if model in effective_ele_set.keys():
                model = model + '1'
            effective_ele_set[model] = cur_effective_ele

        return effective_ele_set


    #--------------FTIR预处理-------------------
    def ftirPreProcess(file):
        xbegin, xend = 650, 4000
        f = open(file,'rb')
        line = f.readline()
        read_flag = False
        line_list = []

        while(line):

            #找到有效数据结束的地方
            if line.find(b'spectrumdark') != -1:
                read_flag = False
                break   
            #处理有效数据
            if read_flag:
                line_tmp = bytes.decode(line)
                line_tmp = [float(x) for x in line_tmp.split()]
                line_list.append(line_tmp)

            #找到有效数据开始的地方  
            if line.find(b'spectrum') != -1:
                read_flag = True
            line = f.readline()
        f.close()
        lineArray = np.array(line_list)
        data_x = lineArray[:,0]
        data_y = lineArray[:,1]
        data_y = data_y.tolist()
        #平滑
        data_smooth = Gaussian_smooth(data_y)
        #去基线
        baseline = baseline_als(data_smooth, 100000, 0.06)
        data_y_nobaseline = np.maximum(0,data_smooth-baseline)
        #内插
        data_x, data_y = interpolation(data_x, data_y_nobaseline, xbegin, xend)
        return [data_x,data_y]

    #------------RAMAN预处理--------------
    def ramanPreProcess(file):
        xbegin, xend = 250, 2875
        f = open(file,'rb')
        line = f.readline()
        read_flag = False
        line_list = []

        while(line):

            #找到有效数据结束的地方
            if line.find(b'spectrumdark') != -1:
                read_flag = False
                break   
            #处理有效数据
            if read_flag:
                line_tmp = bytes.decode(line)
                line_tmp = [float(x) for x in line_tmp.split()]
                line_list.append(line_tmp)

            #找到有效数据开始的地方  
            if line.find(b'spectrum') != -1:
                read_flag = True
            line = f.readline()
        f.close()
        lineArray = np.array(line_list)
        data_x = lineArray[:,0]
        data_y = lineArray[:,1]
        data_y = data_y.tolist()
        #平滑
        data_smooth = Gaussian_smooth(data_y)
        #去基线
        baseline = baseline_als(data_smooth, 100000, 0.06)
        data_y_nobaseline = np.maximum(0,data_smooth-baseline)
        #内插
        data_x, data_y = interpolation(data_x, data_y_nobaseline, xbegin, xend)
        return [data_x,data_y]


    file_name = os.path.splitext(os.path.split(file)[1])[0]
    file_out = out_folder + '/' +file_name + '.npy'
    
    
    if file_type == 'FTIR':
        handledResult = ftirPreProcess(file)
        np.save(file_out, handledResult)
        return file_out
    elif file_type =='RAMAN':
        handledResult = ramanPreProcess(file)
        np.save(file_out, handledResult)
        return file_out
    elif file_type == 'XRD':
        handledResult = xrdPreProcess(file)
        np.save(file_out, handledResult)
        return file_out
    elif file_type == 'XRF':
        handledResult = xrfPreProcess(file)
        np.save(file_out, handledResult)
        return file_out

        
    return (print("您输入的数据检测方法有误"))
    

