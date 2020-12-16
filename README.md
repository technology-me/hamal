# 搬运工·Hamal

一个用来读写json数据的库。

A library for reading and writing JSON data.

### 安装方法·Install Method

#### 下载·Download

```git
git clone https://github.com/technology-me/hamal.git
```

#### 引入·Introduce

1

  将`hamal.py`复制到您的项目中。

  Put` hamal.py `Copy to your project.

2

  ```python
  import hamal
  ```

### 使用·Use

#### 实例化·Instantiate

```python
object = Hamal(file_name)
```

`file_name` 为 文件名或其路径。

实例化一个文件对象。

`file_name` is the file name or its path.

Instantiate a file object.

------

#### read()

```python
object.read(key,language='python',link='@')
```

`key`为json文件中的键（类似于`dict`）。（如果为`All`则表示全部）

`language`为返回的类型，如果为`'python'`，则是返回一个字典，如果为`'json'`，则是返回一个str，为json的内容。

`link`为链接器识别符，用于跳转。

`key` is the key in the JSON file (similar to ` dict`).(if `All` means all)

`language` is the returned type. If it is`'Python'`, it will return a dictionary. If it is`'json'`, it will return a str, which is the content of JSON.

`link` is the linker identifier, which is used to jump.

------
#### write()

```python
object.write(key,value)
```

`key`为欲写入的键。（如果为`All`则表示全部）

`value`为写入的值。

`key` is the key to be written.(if `All` means all)

`value` is the value written.

------
#### change()

```python
object.change(key,in_key,in_value)
```

`key`为欲更改的键。（如果为`All`则表示全部）

`in_key`为该键内欲替换的键。

`in_value`为为该键内欲替换的键的值。

`key` is the key to be changed.(if `All` means all)

`in_key` is the key to be replaced in the key.

`in_value` is the value of the key to be replaced in the key.

------
#### delete()

```python
object.delete(key)
```

`key`为欲删除的键。（如果为`All`则表示全部）

`key` is the key to be deleted.(if `All` means all)

------

#### view()

```python
object.view(value=False)
```

运行本函数，则可以打开一个简陋的Tkinter窗口来显示该JSON文件的内容。

`value[=False]`为是否返回值，如果为`True`，则在控制台返回文件内容。如果为`False`或不填，则不返回。

If you run this function, you can open a crude Tkinter window to display the contents of the JSON file.

`Value [= false]` is whether to return the value. If it is `True`, the file content will be returned in the console. If it is`False` or not filled in, it will not be returned.

------

#### 链接器·Linker

链接器是Hamal引入的一个概念。

你可以在JSON文件中储存一个以`@`或已定义的以其他文字开头的值，来指向本JSON文件的其他键。

```json
{
"a":"@b",
"b":"Hello World"
}
```

则使`a`的值为`b`的值。

你还可以用来表示一个JSON表内的值，其格式为`@KeyName,row,col `。



Linker is a concept introduced by Hamal.
You can store a value in a JSON file that starts with `@` or has been defined to point to other keys in this JSON file.

```json
{
"a": "@b",
"b": "Hello World"
}
```
Make the value of `a` the value of `b`.

You can also use it to represent values in a JSON table in the format `@KeyName,row,col`.