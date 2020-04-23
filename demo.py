import mushroom
import time
import numpy

path = 'demo.json'
time1 = time.time()
time2 = time.time()
times = []

mushroom.delete(path,all)
for i in range(50):
    for j in range(50):
        time1 = time.time()
        mushroom.write_sheet(path, 'put', i, j, i*2+j*2)
        time2 = time.time()
        times.append(time2-time1)
print('表平均写入时间：'+str(numpy.mean(times)))
times = []
for i in range(50):
    for j in range(50):
        time1 = time.time()
        mushroom.read_sheet(path, 'put', i,j)
        time2 = time.time()
        times.append(time2-time1)
print('表平均读取时间：'+str(numpy.mean(times)))
times = []
for i in range(2500):
    time1 = time.time()
    mushroom.write(path,'me',i)
    time2 = time.time()
    times.append(time2-time1)
print('字平均写入时间：'+str(numpy.mean(times)))
times = []
for i in range(2500):
    time1 = time.time()
    mushroom.write(path,'me',i)
    time2 = time.time()
    times.append(time2-time1)
print('字平均读取时间：'+str(numpy.mean(times)))