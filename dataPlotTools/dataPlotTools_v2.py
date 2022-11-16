#!/bin/bash/python3
# -*- coding:UTF-8 -*-
# @houkx 2021-05-31
# Draw a graph according to the corresponding files
import tkinter.filedialog
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # NavigationToolbar2TkAgg


def select_path(root):
    """
    选择数据文件，并读取文件数据，解析后存储数组转换为numpy，传两个BISS的数据数组以及文件地址到画图类
    :param root: 为RootWindows对象
    :return: None
    """
    file_path = tk.filedialog.askopenfilename(title=u'选择文件')
    # \\转换为/
    # file_path = file_path.replace('/', '\\\\')
    # 若地址不为空，打开并读取
    if file_path is not None:
        try:
            with open(file_path, 'r', encoding='utf-8') as fp:
                # file_data = fp.readlines()
                file_data = fp.read()
                fp.close()
                pass
        except (UnboundLocalError, FileNotFoundError):
            pass
        pass

    # 字符串分组转换为list
    file_data_arry = file_data.split(' ')
    # 将所有的数据读出来，抛去list列表中的空字符串，将代表16进制的字符串转换为整数存起来
    file_data_arry_int = []
    for d in file_data_arry:
        if d is None or d == '':
            continue
        file_data_arry_int.append(int(d, 16))
        pass

    # 把数据按照15个元素一维进行切分
    file_data_arry_int = np.array(file_data_arry_int).reshape((-1, 15))

    # 数据权重因为数据是高位在后，低位在前；两个16进制数一组
    weight_16 = [0, 2, 4, 6]
    file_data_arry_int[:, 8] &= 3
    file_data_arry_int[:, 12] &= 3
    # 加权
    for i in range(4):
        file_data_arry_int[:, i + 5] *= 16 ** weight_16[i]
        file_data_arry_int[:, i + 9] *= 16 ** weight_16[i]
    biss1 = file_data_arry_int[:, 5] + file_data_arry_int[:, 6] + file_data_arry_int[:, 7] + file_data_arry_int[:, 8]
    biss2 = file_data_arry_int[:, 9] + file_data_arry_int[:, 10] + file_data_arry_int[:, 11] + file_data_arry_int[:, 12]

    # 调用显示类，将计算后的两个BISS的值和文件的地址传出
    show_plot = ShowPlot(root)
    show_plot.show_statistics(biss1, biss2, file_path)
    pass


def quit_root(root):
    """
    关闭主窗口，即退出程序
    :param root: 传入的是主窗口Tk()对象
    :return: None
    """
    root.destroy()
    pass


class ShowPlot(object):
    """
    描点画图显示类，接收从文件来的数据画图显示到canvas上，
    """
    def __init__(self, root):
        """
        初始话
        :param root:  为RootWindows对象
        """
        self.root = root

    def show_statistics(self, biss1, biss2, file_path):
        """
        画图
        :param biss1: 数据1
        :param biss2:
        :param file_path:
        :return:
        """
        # 先清空这两个子图
        self.root.fig_plot.ax1.cla()
        self.root.fig_plot.ax2.cla()
        # 将文件的绝对地址填充到Entry上展示
        self.root.entry_file_address.delete(0, tk.END)
        self.root.entry_file_address.insert(0, file_path)
        # 绘图
        self.root.fig_plot.ax1.plot(biss1, color='red', linewidth=3, linestyle='-')
        # self.root.fig_plot.ax1.axhline(0, color='black', lw=2)
        self.root.fig_plot.ax1.set_title("BISS1", loc='center', pad=20, fontsize='xx-large', color='red')  # 设置标题

        self.root.fig_plot.ax2.plot(biss2, color='red', linewidth=3, linestyle='-')
        # self.root.fig_plot.ax2.axhline(0, color='black', lw=2)
        self.root.fig_plot.ax2.set_title("BISS2", loc='center', pad=20, fontsize='xx-large', color='red')  # 设置标题
        # 画布展示
        self.root.fig_plot.canvas.draw()
        self.root.fig_plot.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # 更新整个界面
        self.root.root_update()
        pass
    pass


class FigurePlot(object):
    """
    点图类，定义了图标容器框架frame： plot——frame，以及显示点图的画布canvas、子图ax1、ax2
    """
    def __init__(self, frame_fig_plot, shape):
        """
        :param frame_fig_plot: 传入的是绘图的容器
        :param shape: 绘图容易一起消失
        """
        self.root = frame_fig_plot

        self.fig = plt.Figure()
        # --------------------------------------------------------------
        plot_frame = tk.Frame(self.root, width=shape[0], height=shape[1], bg='green')
        plot_frame.propagate(0)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH)
        # --------------------------------------------------------------
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # --------------------------------------------------------------
        # 设置位置，311表示总共有三行一列，当前为第一行，313即三行一列当前在第三行
        self.ax1 = self.fig.add_subplot(311)
        self.ax1.grid(True)
        self.ax2 = self.fig.add_subplot(313, sharex=self.ax1)
        self.ax1.grid(True)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        pass
    pass


class RootWindow(object):
    """主窗体"""
    def __init__(self, shape, locate):
        self.root = tk.Tk()
        # 不可拉伸
        # self.root.resizable(width=False, height=False)
        self.root.withdraw()
        # 窗口大小、初始位置
        s_shape = str(shape[0]) + 'x' + str(shape[1])
        s_locate = '+' + str(locate[0] - shape[0]) + '+' + str(locate[1])
        self.root.geometry(s_shape + s_locate)
        # 标题
        self.root.title("Data plot tools")

        fram_bg = 'Aliceblue'
        button_bg = 'lightcyan'

        # 设置框架2的大小
        fig_frame_shape = (shape[0], shape[1] - 200)

        # 放置一个框架1,放置文本、按钮
        frame_file_path = tk.Frame(self.root, bg=fram_bg)
        frame_file_path.pack(anchor='nw', expand=True, padx=13, pady=50)
        # 框架2放置图片
        self.frame_fig_plot = tk.Frame(self.root, width=fig_frame_shape[1], height=fig_frame_shape[1])
        self.frame_fig_plot.pack(fill='both', expand=True, padx=10)

        # lable
        lable_1 = tk.Label(frame_file_path, text='文件地址', bg=fram_bg)
        lable_1.pack(side='left', fill='both', expand=True)
        # tkinter.Entry文本输入框控件
        self.entry_file_address = tk.Entry(frame_file_path, textvariable=tk.StringVar(value='请选择文档……'),
                                           font=('微软雅黑', 10),
                                           justify='center', bg=button_bg, width=45)
        self.entry_file_address.pack(side='left', fill='both', expand=True)

        # button1
        tk.Button(frame_file_path, text='浏览', command=lambda: select_path(self),
                  bg=fram_bg, width=8).pack(side='left', fill='both', expand=True, padx=10)
        # button2
        tk.Button(frame_file_path, text='取消', command=lambda: quit_root(self.root),
                  bg=fram_bg, width=8).pack(side='left', fill='both', expand=True, padx=10)
        self.fig_plot = FigurePlot(self.frame_fig_plot, fig_frame_shape)
        pass

    def root_update(self):
        self.root.update()
        self.root.deiconify()
        pass

    def refresh(self):
        self.fig_plot.fig.clf()

        pass
    pass


def main():
    root = RootWindow((800, 800), (1200, 130))
    # 初始化一个RootWindow对象，初始化界面显示。
    root.root_update()
    root.root.mainloop()
    pass


if __name__ == '__main__':
    main()
    pass
