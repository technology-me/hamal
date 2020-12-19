

# Hamal

[Chinese](https://github.com/technology-me/hamal/blob/master/README.md)

A library for reading and writing JSON data.

### Install Method

#### Download

```git
git clone https://github.com/technology-me/hamal.git
```

#### Introduce

1. Put `Hamal.py` Copy to your project.

2. Introduce.

   ```python
   import hamal
   ```

### Characteristic

#### Linker

Linker is a concept introduced by Hamal.
You can store a value in a JSON file that starts with `@` or has been defined to point to other keys in this JSON file.

```json
{
"a": "@b",
"b": "Hello World"
}
```

Make the value of `a` the value of `b`.

You can also use it to represent values in a JSON table in the format `@KeyName,Row,Col`.

### Use

#### Instantiate

```python
object = Hamal(file_name)
```

`file_name` is the file name or its path.

Instantiate a file object.

------

#### read()

```python
object.read(key,language='python',link='@')
```

`key` is the key in the JSON file (similar to ` dict`).(if `All` means all)

`language` is the returned type. If it is`'Python'`, it will return a dictionary. If it is`'json'`, it will return a str, which is the content of JSON.

`link` is the linker identifier, which is used to jump.

------
#### write()

```python
object.change(key,in_key,in_value)
```

`key` is the key to be written.(if `All` means all)

`value` is the value written.

------

#### change()

```python
object.change(key,in_key,in_value)
```

`key` is the key to be changed.(if `All` means all)

`in_key` is the key to be replaced in the key.

`in_value` is the value of the key to be replaced in the key.

------

#### delete()

```python
object.delete(key)
```

`key` is the key to be deleted.(if `All` means all)

------

#### view()

```python
object.view(value=False)
```

If you run this function, you can open a crude Tkinter window to display the contents of the JSON file.

`value [= false]` is whether to return the value. If it is `True`, the file content will be returned in the console. If it is`False` or not filled in, it will not be returned.