import json
import os
import base64
from tkinter import *

FILE_NOT_FOUND = '<FileNotFound Mushroom>'
FILE_NO_TEXT = '<FileNoText Mushroom>'
FILE_NO_SUB_KEY = '<FileNoSubKey Mushroom>'

class MushroomError(Exception):                                     # 参数错误类
    pass                                                            # 过

def linker(file_name,link_text):
    """内部函数，用于link双函数递归溯源"""
    read_text = ''
    link_text = link_text[1:]                                       # 截取第二个字符及以后的字符
    if ',' in link_text:                                            # 如果有“，”分隔符
        link_text_split = link_text.split(',')                      # 分开
        if len(link_text_split) == 3:                               # 如果有三项
            read_text = read_sheet(file_name,link_text_split[0],link_text_split[1],link_text_split[2])# 用表读取函数
    else:                                                           # 如果没有“，”分隔符
        read_text = read(file_name,link_text)                       # 用字读取函数
    if read_text[1:] == link_text:                                  # 如果引用自己
        raise MushroomError('Do you want to refer to yourself and create infinite recursion?')# 抛出错误

def view(file_name, value=False):
    """一个用于打开json的查看器"""
    """定义"""
    window = Tk()                                                   # 定义窗口
    file_text = Text(window)                                        # 定义文本框
    scroll = Scrollbar()                                            # 定义滚动条
    """设置窗口"""
    window.title('Json Viewer  ：' + file_name)                     # 窗口标题：Json Viewer
    window.geometry('500x200')                                      # 窗口大小：500x200
    window['background'] = 'white'                                  # 窗口背景色：white
    window.resizable(False, False)                                  # 窗口调整：锁定
    """设置文本框"""
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
    """设置滚动条"""
    scroll.pack(side='right', fill=Y)                               # 滚动条对齐：右；滚动条填充：Y轴
    scroll.config(command=file_text.yview)                          # 滚动条关联：文本框
    """开始"""
    window.mainloop()                                               # 启用窗口
    if value:                                                       # 如果确认返回
        return(json_text)                                           # 返回json内容

def write(file_name, key, value):
    """写json文件"""
    add_file = False                                                # 是否增加文件：否
    python_text = read(file_name, all, 'python')                    # 读取该文件，如果没有返回false
    if python_text == FILE_NOT_FOUND:                               # 如果返回false
        del python_text                                             # 删掉false
        python_text = {}                                            # 变成字典
        add_file = True                                             # 增加了文件，改为真
    if python_text ==FILE_NO_TEXT:                                  # 如果json无内容
        python_text = {}                                            # 创建字典
    with open(file_name, 'w', encoding='utf-8') as file:            # 打开文件
        if key == all and isinstance(value,dict):                   # 如果写入全部（将会覆盖）
            file.write(str(json.dumps(value)))                      # 覆盖写入
        else:                                                       # 如果不是all
            python_text[key] = value                                # 将字典普通赋值
            file.write(str(json.dumps(python_text)))                # 写整洁化的文件
    return(add_file)                                                # 返回是否增加了文件

def read(file_name, key, language='python', link='@'):
    """读json文件"""
    try:                                                            # 检测
        file = open(file_name, 'r', encoding='utf-8')               # 打开json文件
    except FileNotFoundError:                                       # 错误
        return(FILE_NOT_FOUND)                                      # 返回错误信息
    if os.stat(file_name).st_size == 0:                             # 检测文件是否为空
        return(FILE_NO_TEXT)                                        # 错误
    else:                                                           # 不为空
        python_text = json.loads(file.read())                       # python化
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
                if python_text[key][0] == link[0]:                  # 如果str的值首字母是link首字母（必须是分开的，否则第二个if会并报错）
                    return(linker(file_name,python_text[key]))      # 运用递归算法，寻求最终值
            return(python_text[key])                                # 返回这个键的值
        else:                                                       # 如果键不在json的键中
            return(FILE_NO_SUB_KEY)                                 # 返回空字典

def replace(file_name, key, in_key, in_value):
    """替换键内字典或列表的指定键或项的内容"""
    python_text = read(file_name,key)                               # 读取键的值
    if isinstance(python_text,dict):                                # 如果为字典
        python_text[str(in_key)] = in_value                         # 改变键的值
    elif isinstance(python_text,list):                              # 如果为列表
        python_text[int(in_key)] = in_value                         # 改变项的值
    write(file_name,key,python_text)                                # 写入改变值

def delete(file_name, key):
    """删除json指定键"""
    python_text = read(file_name, all)                              # 读取json信息
    if key == all:                                                  # 如果删除全部
        python_text = {}                                            # 那么就都删了
        return(True)                                                # 退出
    if python_text == FILE_NOT_FOUND:                               # 读取错误
        raise MushroomError("'"+key+"'"+' is not a correct file.')  # 抛出错误
    if key in python_text.keys():                                   # 如果key在
        del python_text[key]                                        # 删除
    else:                                                           # 如果key不在
        raise MushroomError(
            "'"+key+"'"+' is not in the key of the json file.')     # 抛出错误
    with open(file_name, 'w', encoding='utf-8') as file:            # 打开文件
        file.write(str(json.dumps(python_text)))                    # 写整洁化的文件

def write_sheet(file_name, key, row, col, value):
    """写json指定字典表"""
    row = str(row)                                                  # 化成字符串
    col = str(col)                                                  # 化成字符串
    python_text = read(file_name, key)                              # 读取json内容
    if python_text == FILE_NO_TEXT:                                 # 如果json无内容
        python_text = {}                                            # 创建字典
    if python_text == FILE_NOT_FOUND:                               # 如果返回false
        raise MushroomError("'" + file_name + "'" +
                            ' is not a correct file.')              # 报错
    else:                                                           # 如果不返回false
        if python_text == FILE_NO_SUB_KEY:
            python_text = read(file_name,all)
        if row in python_text:                                      # 如果行在dict_中
            python_text[row].update({col: value})                   # 直接在行里加列的字典
        else:                                                       # 否则
            python_text.update({row: {col: value}})                 # 同时加行与列
        write(file_name, key, python_text)                          # 写成品

def read_sheet(file_name, key, row="", col="", link='@'):
    """读json指定字典表"""
    if row != all:                                                  # 如果不是all
        row = str(row)                                              # 化成字符串
    if col != all:                                                  # 如果不是all
        col = str(col)                                              # 化成字符串
    python_text = read(file_name, key, 'python')                    # 读取指定键内容
    if python_text == FILE_NOT_FOUND:                               # 如果文件读取错误
        raise MushroomError("'" + file_name + "'" +
                            ' is not a correct file.')              # 报错
    elif python_text == FILE_NO_TEXT:                               # 如果json无内容
        python_text = {}                                            # 创建字典
    else:                                                           # 如果正常
        if row == all and col == all:                               # 如果读取全部
            return(python_text)                                     # 直接返回
        elif row == all:                                            # 如果读取全部row
            return(list(python_text[col].values()))                 # 返回所有列
        elif col == all:                                            # 如果读取全部col
            col_list = []                                           # 初始化列表
            for i in python_text.keys():                            # 循环所有键
                col_list.append(python_text[i][row])                # 增加对应值
            return(list(col_list))                                  # 返回列表
        elif isinstance(python_text[row][col], str):                # 如果是str类型
            if python_text[row][col][0] == link[0]:                 # 如果link匹配
                return(linker(file_name, python_text[row][col]))    # 返回linker函数自动溯源
        return(python_text[row][col])                               # 未被拦截则返回二维字典指定值

def size(file_name):
    """取文件字节大小"""
    return(os.stat(file_name).st_size)                              # 调用库文件

def encode(file_name):
    """加密文件"""
    f=open(file_name,encoding='utf-8')                              # 读取文件
    content=f.read()                                                # 取出数据
    content1=content.encode(encoding='utf-8')                       # 转化格式
    content2=base64.b64encode(content1)                             # 开始编码
    f.close()                                                       # 关闭文件
    with open(file_name, 'wb+') as f:                               # 打开文件
       f.write(content2)                                            # 写回文件

def decode(file_name):
    """解密文件"""
    f=open(file_name,encoding='utf-8')                              # 读取文件
    content=f.read()                                                # 取出数据
    try:                                                            # 准备测试
        content1=base64.b64decode(content)                          # 开始解码
    except:                                                         # 如果错误
        raise MushroomError("File '"+file_name+"' can not decode.") # 抛出定义
    with open(file_name, 'wb+') as f:                               # 打开文件
        f.write(content1)                                           # 写回文件

class mushroom():
    """面向对象式调用"""
    def __init__(self, file_name):
        """用init属性初始化并赋值"""
        self.file_name = file_name                                  # 赋值

    def read(self, key, language='python', link='@'):
        """读json文件"""
        return(read(self.file_name, key, language, link))           # 调用函数

    def write(self, key, value):
        """写json文件"""
        return(write(self.file_name, key, value))                   # 调用函数

    def replace(self, key, in_key, in_value):
        """替换键内字典或列表的指定键或项的内容"""
        return(replace(self.file_name, key, in_key, in_value))      # 调用函数

    def delete(self, key):
        """删除json指定键"""
        return(delete(self.file_name, key))                         # 调用函数

    def read_sheet(self, key, row=all, col=all, link='@'):
        """读json指定字典表"""
        return(read_sheet(self.file_name, key, row, col))           # 调用函数

    def write_sheet(self, key, row, col, value):
        """写json指定字典表"""
        return(write_sheet(self.file_name, key, row, col, value))   # 调用函数

    def view(self, value=False):
        """一个用于打开json的查看器"""
        return(self.file_name, value)                               # 调用函数

    def size(self):
        """取文件字节大小"""
        return(os.stat(self.file_name).st_size)                     # 直接用库

    def encode(self):
        """加密文件"""
        return(encode(self.file_name))

    def decode(self):
        """解密文件"""
        return(decode(self.file_name))