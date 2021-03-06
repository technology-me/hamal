import hamal
import time
#import numpy
path = 'demo.json'
time1 = time.time()
time2 = time.time()

def average(l):
    return float(sum(l))/len(l)

file = hamal.Hamal(path)
test = hamal.Hamal('test.json')
def main():
    times = []
    print(file.size())

    print(file)
    file.delete(all)

    hamal.delete(path,all)
    for i in range(50):
        for j in range(50):
            time1 = time.time()
            file.write_sheet('put', i, j, i*2+j*2)
            time2 = time.time()
            times.append(time2-time1)
    print('表平均写入时间：'+str(average(times)))
    times[0] = average(times)
    times.append(test.read('sheet_write'))
    test.write('sheet_write',average(times))
    times = []
    for i in range(50):
        for j in range(50):
            time1 = time.time()
            file.read_sheet('put', i,j)
            time2 = time.time()
            times.append(time2-time1)
    print('表平均读取时间：'+str(average(times)))
    times[0] = average(times)
    times.append(test.read('sheet_read'))
    test.write('sheet_read',average(times))
    times = []
    for i in range(2500):
        time1 = time.time()
        file.write('me',i)
        time2 = time.time()
        times.append(time2-time1)
    print('字平均写入时间：'+str(average(times)))
    times[0] = average(times)
    times.append(test.read('write'))
    test.write('write',average(times))
    times = []
    for i in range(2500):
        time1 = time.time()
        file.read('me')
        time2 = time.time()
        times.append(time2-time1)
    print('字平均读取时间：'+str(average(times)))
    times[0] = average(times)
    times.append(test.read('read'))
    test.write('read',average(times))
    times = []
    """
    for i in range(2500):
        time1 = time.time()
        file.replace('me','a',2500)
        time2 = time.time()
        times.append(time2-time1)
    print('字平均替换时间：'+str(average(times)))
    times[0] = average(times)
    times.append(test.read('replace'))
    test.write('replace',average(times))
    """


main()