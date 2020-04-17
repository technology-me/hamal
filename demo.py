import mushroom
import time
from numba import jit

path = 'demo.json'

mushroom.write(path, 'user', {'name': 'Smith Lee', 'age': 14})
print(mushroom.read(path, 'user')['name'])
mushroom.write(path, 'user', ('name', 'technology-me'))
print(mushroom.read(path, 'user')['name'])
mushroom.write(path, 'puts', '$play')
mushroom.write(path, 'play', '$just')
mushroom.write(path, 'just', '$user')
print(mushroom.read(path, 'puts', link='$'))
mushroom.delete(path, 'play')
mushroom.delete(path, 'just')

mushroom.view(path)

mushroom.write(path, all, {'all': 'null', 'path': path})

mushroom.view(path)

mushroom.mushroom()
