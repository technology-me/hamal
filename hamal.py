import json
import os
import base64
from tkinter import *
from json import JSONDecodeError

FILE_NOT_FOUND = '<FileNotFound Hamal>'
FILE_NO_TEXT = '<FileNoText Hamal>'
FILE_NO_SUB_KEY = '<FileNoSubKey Hamal>'


class HamalError(Exception):
    pass


def _linker(file_name, link_text):
    """内部函数，用于link双函数递归溯源"""
    read_text = ''
    link_text = link_text[1:]
    if ',' in link_text:
        link_text_split = link_text.split(',')
        if len(link_text_split) == 3:
            if link_text_split[1] == 'all':
                link_text_split[1] = all
            elif link_text_split[2] == 'all':
                link_text_split[2] = all
            read_text = read_sheet(
                file_name, link_text_split[0], link_text_split[1], link_text_split[2])
    else:
        read_text = read(file_name, link_text)
    if read_text[1:] == link_text:
        raise HamalError(
            'Do you want to refer to yourself and create infinite recursion?')
    return(read_text)


def view(file_name, value=False):
    """一个用于打开json的查看器"""
    """定义"""
    window = Tk()
    file_text = Text(window)
    """设置窗口"""
    window.title('Json Viewer  ：' + file_name)
    window.geometry('500x200')
    window['background'] = 'white'
    window.resizable(False, False)
    """设置文本框"""
    file_text.pack(side='left')
    json_text = json.dumps(read(file_name, all, 'python'),
                           indent=4, sort_keys=True)
    file_text.config(state=NORMAL)
    file_text.delete(1.0, END)
    if not json_text:
        file_text.insert(END, 'Confidential')
    else:
        for i in json_text:
            file_text.insert(END, i)
    file_text.config(state=DISABLED)
    """开始"""
    window.mainloop()
    if value:
        return(json_text)


def write(file_name, key, value):
    """写json文件"""
    add_file = False
    # 读取该文件，如果没有返回false
    python_text = read(file_name, all, 'python')
    if python_text == FILE_NOT_FOUND:
        del python_text
        python_text = {}
        add_file = True
    if python_text == FILE_NO_TEXT:
        python_text = {}
    with open(file_name, 'w', encoding='utf-8') as file:
        if key == all and isinstance(value, dict):
            file.write(str(json.dumps(value)))
        else:
            python_text[key] = value
            file.write(str(json.dumps(python_text)))
    return(add_file)


def read(file_name, key, language='python', link='@'):
    """读json文件"""
    try:
        file = open(file_name, 'r', encoding='utf-8')
    except FileNotFoundError:
        return(FILE_NOT_FOUND)
    if os.stat(file_name).st_size == 0:
        return(FILE_NO_TEXT)
    else:
        try:
            python_text = json.loads(file.read())
        except JSONDecodeError:
            raise HamalError('The file cannot be decoded. Check the file name or contents.')
    if key == all:
        if language == 'python':
            # 以python字典打印
            return(python_text)
        elif language == 'json':
            json_text_c = json.dumps(python_text, sort_keys=True)
            return(json_text_c)
        else:
            raise HamalError('Parameter value ' +
                             language + ' does not exist')
    else:
        if key in python_text.keys():
            if isinstance(python_text[key], str):
                # 如果str的值首字母是link首字母（必须是分开的，否则第二个if会并报错）
                if python_text[key][0] == link[0]:
                    # 运用递归算法，寻求最终值
                    return(_linker(file_name, python_text[key]))
            return(python_text[key])
        else:
            return(FILE_NO_SUB_KEY)


def change(file_name, key, in_key, in_value):
    """替换键内字典或列表的指定键或项的内容"""
    python_text = read(file_name, key)
    if isinstance(python_text, dict):
        python_text[str(in_key)] = in_value
    elif isinstance(python_text, list):
        python_text[int(in_key)] = in_value
    write(file_name, key, python_text)


def delete(file_name, key):
    """删除json指定键"""
    python_text = read(file_name, all)
    if key == all:
        python_text = {}
        return(True)
    if python_text == FILE_NOT_FOUND:
        raise HamalError("'"+key+"'"+' is not a correct file.')
    if key in python_text.keys():
        del python_text[key]
    else:
        raise HamalError(
            "'"+key+"'"+' is not in the key of the json file.')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(json.dumps(python_text)))


def write_sheet(file_name, key, row, col, value):
    """写json指定字典表"""
    row = str(row)
    col = str(col)
    python_text = read(file_name, key)
    if python_text == FILE_NO_TEXT:
        python_text = {}
    if python_text == FILE_NOT_FOUND:
        raise HamalError("'" + file_name + "'" +
                         ' is not a correct file.')
    else:
        if python_text == FILE_NO_SUB_KEY:
            python_text = read(file_name, all)
        if row in python_text:
            python_text[row].update(
                {col: value})
        else:
            python_text.update({row: {col: value}})
        write(file_name, key, python_text)


def read_sheet(file_name, key, row="", col="", link='@'):
    """读json指定字典表"""
    if row != all:
        row = str(row)
    if col != all:
        col = str(col)
    python_text = read(file_name, key, 'python')
    if python_text == FILE_NOT_FOUND:
        raise HamalError("'" + file_name + "'" +
                         ' is not a correct file.')
    elif python_text == FILE_NO_TEXT:
        python_text = {}
    else:
        if row == all and col == all:
            return(python_text)
        elif row == all:
            return(list(python_text[col].values()))
        elif col == all:
            col_list = []
            for i in python_text.keys():
                col_list.append(python_text[i][row])
            return(list(col_list))
        elif isinstance(python_text[row][col], str):
            if python_text[row][col][0] == link[0]:
                # 返回linker函数自动溯源
                return(_linker(file_name, python_text[row][col]))
        # 未被拦截则返回二维字典指定值
        return(python_text[row][col])


def size(file_name):
    """取文件字节大小"""
    return(os.stat(file_name).st_size)


def encode(file_name):
    """加密文件"""
    f = open(file_name, encoding='utf-8')
    content = f.read()
    content1 = content.encode(encoding='utf-8')
    content2 = base64.b64encode(content1)
    f.close()
    with open(file_name, 'wb+') as f:
        f.write(content2)


def decode(file_name):
    """解密文件"""
    f = open(file_name, encoding='utf-8')
    content = f.read()
    try:
        content1 = base64.b64decode(content)
    except:
        raise HamalError("File '"+file_name+"' can not decode.")
    with open(file_name, 'wb+') as f:
        f.write(content1)


class Hamal():
    """面向对象式调用"""

    def __init__(self, file_name):
        """用init属性初始化并赋值"""
        self.file_name = file_name

    def read(self, key, language='python', link='@'):
        """读json文件"""
        return(read(self.file_name, key, language, link))

    def write(self, key, value):
        """写json文件"""
        return(write(self.file_name, key, value))

    def change(self, key, in_key, in_value):
        """替换键内字典或列表的指定键或项的内容"""
        return(change(self.file_name, key, in_key, in_value))

    def delete(self, key):
        """删除json指定键"""
        return(delete(self.file_name, key))

    def read_sheet(self, key, row=all, col=all, link='@'):
        """读json指定字典表"""
        return(read_sheet(self.file_name, key, row, col))

    def write_sheet(self, key, row, col, value):
        """写json指定字典表"""
        return(write_sheet(self.file_name, key, row, col, value))

    def view(self, value=False):
        """一个用于打开json的查看器"""
        return(view(self.file_name, value))

    def size(self):
        """取文件字节大小"""
        return(os.stat(self.file_name).st_size)

    def encode(self):
        """加密文件"""
        return(encode(self.file_name))

    def decode(self):
        """解密文件"""
        return(decode(self.file_name))
