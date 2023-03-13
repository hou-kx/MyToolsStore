import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

# root_path = r'D:\DeskTop\test-report'

def sava_file(x, y, fileName='data', fileType='.csv', plit=','):
    '''将两个数组保存为 CSV 文件'''
    np.savetxt(fileName + fileType, np.column_stack((x, y)), delimiter=plit)
    pass

def read_file(fileName, plit=','):
    '''读取 CSV 文件'''
    data = np.loadtxt(fileName, delimiter=plit)
    return data

def dir_file_list(rootPath):
    '''
    打印输出 path 文件夹下所有的文件名列表
    '''
    file_list = np.array(os.listdir(rootPath))
    for file_name in file_list:
        print(file_name)
    return file_list

def read_files_data(rootPath, files = []):
    '''
    从文件路径中读取数据,二维以 ',' 号隔开
    '''
    x_res = []
    y_res = []
    for file in files:
        data = read_file(os.path.join(rootPath, file))
        x_res.extend(data[:, 0])
        y_res.extend(data[:, 1])
    return x_res, y_res

def run_scat(x, y, title, xLable, yLable):
    '''
    绘散点图
    '''
    # 打印数组长度
    print(f'x-length:{len(x)}, y-length:{len(y)}')

    # 设置图中显示 中文
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 图例 字符串
    label_str = f'x-length:{len(x)}, y-length:{len(y)}'

    # 设置图表实例纵横比
    fig = plt.figure(figsize=(9, 4))
    # 指定这个画布上就一个图 1行 1列
    grid = gridspec.GridSpec(1, 1)
    # 多子图时可以修改
    ax = fig.add_subplot(grid[0, 0])

    # 设置横纵轴的极值 （xmin, xmax, ymin, ymax）
    # ax.set_xlim(0,85)
    # ax.set_ylim(0,65)

    # 标题
    ax.set_title(title)
    #设置坐标轴名称
    ax.set_xlabel(xLable)
    ax.set_ylabel(yLable)

    # 描点，放置图例, s：散点大小，Marker：散点样式，c：颜色，loc：图例位置
    ax.scatter(x, y,label=label_str, s=10, marker='o', c='k')
    ax.legend(loc='upper left')

    # 显示
    plt.show()
    pass

def run_scat_3d(x, y, z, title):
    '''
    3D 散点图
    '''
    # 创建一个 3D 图像
    fig = plt.figure()
    # 创建一个 1行1列的三维子图，标识1
    ax = fig.add_subplot(111, projection='3d')
    # 绘制散点图
    ax.scatter(x, y, z, c='k')
    # 设置坐标轴标签
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    # 标题
    ax.set_title(title)
    # 显示图像
    plt.show()

if __name__ == '__main__':
    # 随机生成数据
    x = np.random.rand(50)
    y = np.random.rand(50)

    run_scat(x, y, '测试', 'x-label', 'y-label')
    pass


# path = r'C:\Users\houkx\jupyterLaboratory'

# file_list = dir_file_list(path)
# >> .ipynb_checkpoints
# >> 6.png
# >> Concurrent.future.ipynb
# >> cuda Test.ipynb
# >> data1.csv
# >> data2.csv
# >> data3.csv

# indexs = [4,5] # data1.csv， data2.csv
# x, y = read_files_data(path, file_list[indexs]) # 合并 data1 和 data2 中数据

# run_scat(x,y,'ceshi', 'x-label', 'y-label')