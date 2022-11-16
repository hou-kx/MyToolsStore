#  ^-^ coding:utf8  Hou k x
import tkinter as tk
from functools import partial


def get_button_value(entry, value):
    # 获取entry中的内容
    entry_value = entry.get()

    # 出现连续+，则第二个+为无效输入，不做任何处理
    if (entry_value[-1:] == '+') and (value == '+'):
        return
    # 出现连续+--，则第三个-为无效输入，不做任何处理, +-加上一个负数
    if (entry_value[-2:] == '+-') and (value == '-'):
        return
    # 窗口已经有--后面字符不能为+或-，减上一负数
    if (entry_value[-2:] == '--') and (value in ['-', '+']):
        return
    # 窗口已经有 ** 后面字符不能为 * 或 /，幂
    if (entry_value[-2:] == '**') and (value in ['*', '/']):
        return

    # 输入合法将字符插入到entry窗口结尾
    entry.insert("end", value)


def back_space(entry):
    __len = len(entry.get())
    entry.delete(__len - 1)


def clear(entry):
    # entry.select_clear()
    entry.delete(0, tk.END)
    # clear(entry)


def computation(entry):
    entry_value = entry.get()
    # 判断是否为空
    if not entry_value:
        return

    clear(entry)

    try:
        result_value = str(eval(entry_value))
    except Exception:
        entry.insert('end', 'Calculator ERROR!')
    if len(entry_value) > 20:
        entry.insert('end', 'Value overflow')
    else:
        entry.insert('end', result_value)




if __name__ == '__main__':
    # 设定颜色

    fram_bg = 'Aliceblue'
    button_bg = 'lightcyan'
    # button_activebackground = 'PaleTurquoise'
    button_active_bg = 'DarkCyan'

    # 创建窗口对象
    calculator = tk.Tk()
    # 设置初始窗口大小，这里没有设置，+X+Y设置启动出现的位置
    calculator.geometry('+200+230')
    calculator["background"] = fram_bg
    # 设定窗口不能拉伸
    calculator.resizable(0, 0)
    calculator.title('Houkx‘s 计算器')



    # 放置一个框架

    frame = tk.Frame(calculator, bg=fram_bg)
    frame.pack(padx=13, pady=13)

    # tkinter.Entry文本输入框控件
    v = tk.StringVar(frame, value='0')
    entry = tk.Entry(frame, textvariable=v, font=('Arial', 14), justify='right', bg=button_bg)
    # 以表格的方式放置控件
    entry.grid(row=0, rowspan=2, columnspan=4, padx=5, pady=5, stick=tk.N+tk.S+tk.W+tk.E)


    def grid_button(text, command_func, func_params, bg=button_bg, **grid_params):
        """
        functools.partial(func[,*args][, **kwargs])
        偏函数partial，可以理解为定义了一个模板，后续的按钮在模板基础上进行修改或添加特性;
        也可以理解为把一个函数的某些参数给固定住，返回一个新的函数。
        :param text: 按键显示的内容
        :param command_func: 点击事件
        :param func_params: 传入参数
        :param bg: 背景色
        :param grid_params: 放置控件的参数
        :return:
        """
        # 偏函数partial，可以理解为定义了一个模板，后续的按钮在模板基础上进行修改或添加特性
        my_button = partial(tk.Button, frame, bg=button_bg, padx=16, pady=9, state='normal', activebackground=button_active_bg)

        # 重新调用自定义后的tk.Button() 函数（my_button()）, *func_params 分配关键字参数
        button = my_button(text=text, bg=bg, command=lambda: command_func(*func_params))
        # 放置按钮，传入 row column rowspan columnspan参数，**grid_params 字典值分配关键字参数,设定默认控件内外边距，上下左右对其，自定义在行列显示
        button.grid(padx=5, pady=5, ipadx=2, ipady=1, stick=tk.N+tk.S+tk.W+tk.E, **grid_params)

    # 放置数字按键←，C，*，÷
    grid_button('←', back_space, (entry, ), row=2, column=0)
    grid_button('C', clear, (entry, ), row=2, column=1)
    grid_button('+', get_button_value, (entry, '+'), row=2, column=2)
    grid_button('-', get_button_value, (entry, '-'), row=2, column=3)
    grid_button('*', get_button_value, (entry, '*'), row=3, column=3)
    grid_button('÷', get_button_value, (entry, '/'), row=4, column=3)
    grid_button('=', computation, (entry, ), row=5, column=3, rowspan=2)
    # 放置数字按键789，456，123
    grid_button('7', get_button_value, (entry, '7'), row=3, column=0)
    grid_button('8', get_button_value, (entry, '8'), row=3, column=1)
    grid_button('9', get_button_value, (entry, '9'), row=3, column=2)
    grid_button('4', get_button_value, (entry, '4'), row=4, column=0)
    grid_button('5', get_button_value, (entry, '5'), row=4, column=1)
    grid_button('6', get_button_value, (entry, '6'), row=4, column=2)
    grid_button('1', get_button_value, (entry, '1'), row=5, column=0)
    grid_button('2', get_button_value, (entry, '2'), row=5, column=1)
    grid_button('3', get_button_value, (entry, '3'), row=5, column=2)
    #放置0，.
    grid_button('0', get_button_value, (entry, '0'), row=6, column=0, columnspan=2)
    grid_button('.', get_button_value, (entry, '.'), row=6, column=2)
    calculator.mainloop()

