import pandas as pd
import os
import numpy as np
import shutil
import time

dir_path = r'D:\DeskTop\附件下载_反诈中心五张截图'
excel_path = r'D:\DeskTop\2020.xlsx'
    
def dir_file_list(rootPath):
    '''
    打印输出 path 文件夹下所有的文件名列表
    '''
    file_list = np.array(os.listdir(rootPath))
    # for file_name in file_list:
    # print(file_name)
    return file_list


def read_excel_nickName2name(excelPath):
    '''
    excel 中存在 两列，其中姓名为收集表中，导入的真是姓名，提交者为qq昵称，生成一个字典，根据qq昵称存储真实姓名

        姓名      提交者（自动）
        周**      炖汤
    '''
    # 读取 Excel 文件
    df = pd.read_excel(excelPath)

    # # 选择需要读取的列
    # column_data = df['姓名']
    # # 打印列数据
    # print(column_data[0])

    # 两个对照列
    col_name = '姓名'
    col_nickname = '提交者（自动）'
        
    nickname2name = {}
    for i in range(len(df[col_name])):
        name = df[col_name][i]
        nickname = df[col_nickname][i]
        nickname2name[nickname] = name
        pass
    return nickname2name

def run_a_folder(excelPath, filePath=''):
    '''
    one person a folder
    '''
    start_time  = time.time()
    name = read_excel_nickName2name(excelPath)
    file_list = dir_file_list(filePath)
    
    root_path = os.path.join(filePath, 'man a folder')
    if not os.path.exists(root_path):
            os.makedirs(root_path)
    for file in file_list:
        file_name = os.path.join(filePath, file)
        print(file_name, name[file.split('-')[1]])
        folder_name = os.path.join(root_path, name[file.split('-')[1]])  # 替换为你想要的文件夹名称
        # 创建文件夹
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # 将对应文件 copy 到对应文件中去
        shutil.copy(file_name, folder_name)
    end_time  = time.time()
    print(f"\n完成!!!\n共计生成 {len(dir_file_list(root_path))} 个文件夹，耗时 {end_time - start_time:.2f} 秒！")
    pass

# run_a_folder(excel_path, dir_path)