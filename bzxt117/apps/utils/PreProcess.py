import os
import math
import numpy as np
from scipy.interpolate import interp1d
from scipy import sparse
from scipy.sparse.linalg import spsolve
import xlrd
import csv 

'''
*********************************************************************
文件名称: PreProcess.py
所属系统名称: 爆炸系统
功能: 对各种检测模式下上传的样本进行预处理
引入函数方式：from modules.PreProcess import preProcess
基本思想: 利用相关系数以及直方图比对等思想来计算各谱图之间的相似度
执行条件: 文件格式传入无误
输入参数: file_type -- 检测方法（‘GCMS’，‘XRD’，‘XRF’，‘FTIR’，‘RAMAN’）
         sample_id -- 样本id
         sampleFile_id -- 样本文件id
         file -- 文件路径 
返回值: [ 错误代码, file_out ]       错误代码：0 —— 成功，其他数值 —— 失败 
                                   file_out -- 处理后的文件存储路径
说明:无
设计者 : 易籽彤
日期: 20181220

修改日期：20181222
修改内容：加入XRF类型TestAll   (待定)
修改人：易籽彤
*********************************************************************
'''

#主函数
def preProcess(file_type, sample_id, sampleFile_id, file):
       
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
            effective_element = {}
            element = cur_data[1::2]
            error = cur_data[2::2]

            for i in range(0,len(element)):
                if element[i]!='<LOD' and element[i]>3*error[i]:
                    effective_element[element_name[i]] = element[i]
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
            if (cur_type.find('Metal')!=-1) or (cur_type.find('Plastics')!=-1) or (cur_type.find('Soil')!=-1) or (cur_type.find('Mining')!=-1) or (cur_type.find('TestAll')!=-1):
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

    #----------GCMS预处理----------------
    def gcmsPreProcess(data_folder):
        result_dict = {}
        file_list = os.listdir(data_folder)
        for file in file_list:
            if os.path.splitext(file)[1]:
                file_name = os.path.splitext(file)[0]
                cur_file = os.path.join(data_folder, file)
                try:
                    data = np.loadtxt(cur_file, skiprows=2)
                    data_x = data[:,0]
                    data_y = data[:,1]
                except ValueError as e:       #如果文件中有‘正无穷大’， 则改变读取文件的方式，处理方式：忽略该点
                    if str(e).find('正无穷大'):
                        data_x = []
                        data_y = []
                        f = open(cur_file,'rb')
                        line = f.readline()
                        line = f.readline()
                        line = f.readline()
                        while line:
                            line_tmp = bytes.decode(line)
                            line_tmp = line_tmp.split('\t')
                            data_x.append(float(line_tmp[0]))
                            if line_tmp[1].find('正无穷大') != -1:        
                                pass
                                data_y.append(0)
                            else:
                                pass
                                data_y.append(float(line_tmp[1]))
                            line = f.readline()
                        data_x = np.array(data_x)  
                        data_y = np.array(data_y)
                    else:
                        print('文件内容的格式有误')

                if file_name.find('TIC') != -1:
                    max_index = np.argwhere(data_y == np.max(data_y))
                    result_dict['RetentionTime'] = max_index
                elif file_name.find('MS') != -1:
                    data_y = data_y.tolist()
                    #平滑
                    data_smooth = Gaussian_smooth(data_y)
                    #去基线
                    baseline = baseline_als(data_smooth, 100000, 0.06)
                    data_y_nobaseline = np.maximum(0,data_smooth-baseline)
                    result_dict[file_name] = [data_x, data_y_nobaseline]
        return result_dict   
    

    out_folder = os.path.split(file)[0]+'/handled'
    file_out = out_folder + '/' + str(sample_id) + '-' + str(sampleFile_id)+ '.npy'
    
    
    if file_type == 'FTIR':
        handledResult = ftirPreProcess(file)
        np.save(file_out, handledResult)
        return ['0', file_out]
    elif file_type =='RAMAN':
        handledResult = ramanPreProcess(file)
        np.save(file_out, handledResult)
        return ['0', file_out]
    elif file_type == 'XRD':
        handledResult = xrdPreProcess(file)
        np.save(file_out, handledResult)
        return ['0', file_out]
    elif file_type == 'XRF':
        handledResult = xrfPreProcess(file)
        np.save(file_out, handledResult)
        return ['0', file_out]
    elif file_type == 'GCMS':
        out_folder = os.path.split(file)[0]
        out_folder = os.path.split(out_folder)[0] + '/handled'
        file_out = out_folder + '/' + str(sample_id) + '-' + str(sampleFile_id) + '.npy'
        handledResult = gcmsPreProcess(file)
        np.save(file_out, handledResult)
        return ['0', file_out]

        
    return (print("您输入的数据检测方法有误"))
    

