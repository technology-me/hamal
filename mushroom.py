import json
import os
from tkinter import *

class MushroomError(Exception):                                     # 参数错误类
    pass                                                            # 过


def view(file_name):
    """一个用于打开json的查看器"""
    # 定义
    window = Tk()                                                   # 定义窗口
    file_text = Text(window)                                        # 定义文本框
    scroll = Scrollbar()                                            # 定义滚动条
    # 设置窗口
    window.title('Json Viewer  ：' + file_name)                     # 窗口标题：Json Viewer
    window.geometry('500x200')                                      # 窗口大小：500x200
    window['background'] = 'white'                                  # 窗口背景色：white
    window.resizable(False, False)                                  # 窗口调整：锁定
    # 设置文本框
    file_text.pack(side='left')                                     # 文本框对齐：左
    file_text.config(yscrollcommand=scroll.set)                     # 文本框关联，滚动条
    json_text = json.dumps(read(file_name, all, 'python'),
                           indent=4, sort_keys=True)                # 获取json
    file_text.config(state=NORMAL)                                  # 禁止编辑1
    file_text.delete(1.0, END)                                      # 禁止编辑2
    if not json_text:                                               # 如果无文件
        file_text.insert(END, 'Confidential')                       # 显示找不到
    else:                                                           # 如果正常
        for i in json_text:                                         # 逐行读取json内容
            file_text.insert(END, i)                                # 在最后添加该条信息
    file_text.config(state=DISABLED)                                # 禁止编辑3
    # 设置滚动条
    scroll.pack(side='right', fill=Y)                               # 滚动条对齐：右；滚动条填充：Y轴
    scroll.config(command=file_text.yview)                          # 滚动条关联：文本框
    # 开始
    window.mainloop()                                               # 启用窗口
    return(json_text)                                               # 返回json内容


def write(file_name, key, value):
    """写json文件"""
    add_file = False                                                # 是否增加文件：否
    python_text = read(file_name, all, 'python')                    # 读取该文件，如果没有返回false
    if python_text == False:                                        # 如果返回false
        if isinstance(value, tuple):                                # 禁用元组增改法
            raise MushroomError(
                'the file was not found, so the quick addition and subtraction of tuples cannot be used.')  # 抛出异常
        del python_text                                             # 删掉false
        python_text = {}                                            # 变成字典
        add_file = True                                             # 增加了文件，改为真
    with open(file_name, 'w', encoding='utf-8') as file:            # 打开文件
        if key == all:                                              # 如果写入全部（将会覆盖）
            file.write(str(json.dumps(value)))                      # 覆盖写入
        else:                                                       # 如果不是all
            if python_text == {}:                                   # 如果啥东西都没有
                python_text[key] = value                            # 将字典普通赋值
            else:                                                   # 否则
                if isinstance(value, tuple):                        # 检测是否为元组赋值型
                    if isinstance(python_text[key], dict):          # 检验key是否字典
                        python_text[key][value[0]] = value[-1]      # 元组赋值
                    else:                                           # key不是字典要报错
                        raise MushroomError(
                            'the key was not dict, so the quick addition and subtraction of tuples cannot be used.')  # 抛出错误
                else:                                               # 如果不是
                    python_text[key] = value                        # 将字典普通赋值
                file.write(str(json.dumps(python_text)))            # 写整洁化的文件
    return(add_file)                                                # 返回是否增加了文件


def read(file_name, key, language='python', link='@'):
    """读json文件"""
    try:                                                            # 检测
        file = open(file_name, 'r', encoding='utf-8')               # 打开json文件
    except FileNotFoundError:                                       # 错误
        return(False)                                               # 不返回
    if os.stat(file_name).st_size == 0:                             # 检测文件是否为空
        return(False)                                               # 不返回
    python_text = json.loads(file.read())                           # python化
    if key == all:                                                  # 如果读取全部
        if language == 'python':                                    # 如果是python风格
            return(python_text)                                     # 以python字典打印
        elif language == 'json':                                    # 如果是json
            json_text_c = json.dumps(python_text, sort_keys=True)   # json压缩化
            return(json_text_c)                                     # 返回压缩化
        else:                                                       # 如果都不是
            raise MushroomError('Parameter value ' +
                                  language + ' does not exist')     # 抛出错误
    else:                                                           # 如果不是all
        if key in python_text.keys():                               # 如果键在json的键中
            if isinstance(python_text[key], str):                   # 如果值是str
                if python_text[key][0] == link:                     # 如果str的值首字母是‘@’（必须是分开的，否则第二个if会并报错）
                    return(read(file_name, python_text[key][1:], 'python', link))# 运用递归算法，寻求最终值
            return(python_text[key])                                # 返回这个键的值
        else:                                                       # 如果键不在json的键中
            raise MushroomError(
                "'" + key + "'" + ' is not in the json file')       # 抛出错误


def delete(file_name, key):
    """删除json指定键"""
    python_text = read(file_name, all)                              # 读取json信息
    if python_text == False:                                        # 读取错误
        raise MushroomError("'"+key+"'"+' is not in the key of the json file.')# 抛出错误
    if key in python_text.keys():                                   # 如果key在
        del python_text[key]                                        # 删除
    else:                                                           # 如果key不在
        raise MushroomError("'"+key+"'"+' is not in the key of the json file.')# 抛出错误
    with open(file_name, 'w', encoding='utf-8') as file:            # 打开文件
        file.write(str(json.dumps(python_text)))                    # 写整洁化的文件


def mushroom():
    print('The mushroom library for python')
    print('Version： 1.0.0.0')
    print('Producer: Smith Lee')
    print('Made In China')
