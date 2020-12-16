# 搬运工·Hamal

一个用来读写json数据的库。

A library for reading and writing JSON data.

### 使用方法·Usage Method
#### 下载·Download

```
git clone https://github.com/technology-me/hamal.git
```

#### 引入·Introduce
1

  将`hamal.py`复制到您的项目中。
  
  Put` hamal.py `Copy to your project.
   
2
  ```
  import hamal
  ```
  
#### 使用·Use
------
```
object = Hamal(file_name)
```

`file_name` 为 文件名或其路径。

`file_name` is the file name or its path.

实例化一个文件对象。

Instantiate a file object.

------
```
object.read(key,language='python',link='@')
```

`key`为json文件中的键（类似于`dict`）。

`language`为返回的类型，如果为`'python'`，则是返回一个字典，如果为`'json'`，则是返回一个str，为json的内容。

`link`为链接器识别符，用于跳转。

`key` is the key in the JSON file (similar to ` dict`).

`language` is the returned type. If it is`'Python'`, it will return a dictionary. If it is`'json'`, it will return a str, which is the content of JSON.

`link` is the linker identifier, which is used to jump.

------
```
object.write(key,value)
```

`key`为欲写入的键。

`value`为写入的值。

`key` is the key to be written.

`value` is the value written.

------
```
object.change(key,in_key,in_value)
```

