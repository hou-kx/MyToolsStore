#!/bin/bash/python3
# -*- coding:UTF-8 -*-
# @houkx 2021-05-31
# Draw a graph according to the corresponding files
import time

import tkinter.filedialog
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # NavigationToolbar2TkAgg

def browse_path(frame_plot, root):
    # for widget in frame_plot.winfo_children():
    #     widget.destroy(tk.ALL)
    #     widget.delete(tk.ALL)
    # # frame_plot.destroy()
    # 框架2放置图片
    # frame_e_l = tk.Frame(root, bg='red')
    frame_plot = tk.Frame(root)
    frame_plot.pack(fill='both', expand=True, padx=10)

    # file_path = tk.filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('H:/')))
    file_path = tk.filedialog.askopenfilename(title=u'选择文件')
    # \\转换为/
    # file_path = file_path.replace('/', '\\\\')
    if file_path is not None:
        try:
            with open(file_path, 'r', encoding='utf-8') as fp:
                # file_data = fp.readlines()
                file_data = fp.read()
                fp.close()
                pass
        except (UnboundLocalError, FileNotFoundError):
            pass
    # print(file_data)
    file_data_arry = file_data.split(' ')
    # file_data_arry = [x.strip() for x in file_data_arry if x.strip() != '']
    file_data_arry_int = []
    for d in file_data_arry:
        if d is None or d == '':
            continue
        file_data_arry_int.append(int(d, 16))
        pass
    file_data_arry_int = np.array(file_data_arry_int).reshape((-1, 15))

    weight_16 = [0, 2, 4, 6]
    file_data_arry_int[:, 8] &= 3
    file_data_arry_int[:, 12] &= 3

    for i in range(4):
        file_data_arry_int[:, i + 5] *= 16 ** weight_16[i]
        file_data_arry_int[:, i + 9] *= 16 ** weight_16[i]
    biss1 = file_data_arry_int[:, 5] + file_data_arry_int[:, 6] + file_data_arry_int[:, 7] + file_data_arry_int[:, 8]
    biss2 = file_data_arry_int[:, 9] + file_data_arry_int[:, 10] + file_data_arry_int[:, 11] + file_data_arry_int[:, 12]

    figure = create_matplotlib(biss1, biss2)

    canvas = FigureCanvasTkAgg(figure, frame_plot)

    # canvas.delete(tk.ALL)
    canvas.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
    toolbar = NavigationToolbar2Tk(canvas, frame_plot)
    # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    pass


def create_matplotlib(biss1, biss2):
    fig = plt.figure()

    fig.clf()

    ax1 = fig.add_subplot(311)
    ax1.plot(biss1, color='red', linewidth=3, linestyle='-')
    ax1.grid(True)
    # ax1.axhline(0, color='black', lw=2)
    ax1.set_title("BISS1", loc='center', pad=20, fontsize='xx-large', color='red')  # 设置标题

    ax2 = fig.add_subplot(313, sharex=ax1)
    ax2.plot(biss2, color='red', linewidth=3, linestyle='-')
    ax2.grid(True)
    # ax2.axhline(0, color='black', lw=2)
    ax2.set_title("BISS2", loc='center', pad=20, fontsize='xx-large', color='red')  # 设置标题
    return fig


def quit_root(root):
    root.destroy()
    pass


def main():
    fram_bg = 'Aliceblue'
    button_bg = 'lightcyan'
    button_active_bg = 'DarkCyan'

    # 创建窗口对象
    root = tk.Tk()

    # 设置初始窗口大小，这里没有设置，+X+Y设置启动出现的位置
    root.geometry('800x700+200+130')
    root["background"] = fram_bg

    # 设定窗口不能拉伸
    # root.resizable(0, 0)
    root.title('Houkx‘s plot tools')

    # 放置一个框架,放置文本、按钮
    # frame_e_l = tk.Frame(root, bg=fram_bg, highlightthickness=3)
    frame_e_l = tk.Frame(root, bg=fram_bg)
    frame_e_l.pack(anchor='nw', expand=True, padx=13, pady=50)

    # 框架2放置图片
    # frame_e_l = tk.Frame(root, bg='red')
    frame_plot = tk.Frame(root)
    frame_plot.pack(fill='both', expand=True, padx=10)

    # lable
    lable_1 = tk.Label(frame_e_l, text='文件地址', bg=fram_bg)
    lable_1.pack(side='left', fill='both', expand=True)
    # tkinter.Entry文本输入框控件
    entry_file_address = tk.Entry(frame_e_l, textvariable=tk.StringVar(value='请选择文档……'), font=('微软雅黑', 10),
                                  justify='center', bg=button_bg, width=45)
    entry_file_address.pack(side='left', fill='both', expand=True)
    # button1
    # btn_file_adress = tk.Button(frame_e_l, text='浏览', command=browse_path(), bg=fram_bg, width=8)
    btn_file_adress = tk.Button(frame_e_l, text='浏览', command=lambda: browse_path(frame_plot, root), bg=fram_bg,
                                width=8)
    btn_file_adress.pack(side='left', fill='both', expand=True, padx=10)
    # button2
    btn_file_cancel = tk.Button(frame_e_l, text='取消', command=lambda: quit_root(root), bg=fram_bg, width=8)
    btn_file_cancel.pack(side='left', fill='both', expand=True, padx=10)

    root.mainloop()
    pass


if __name__ == '__main__':
    main()
    pass
