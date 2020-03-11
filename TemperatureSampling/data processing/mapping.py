import csv
import math
import numpy as np 
import matplotlib.pyplot as plt


with open('log.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')


    line_count = 0
    timeZero = 1583312437858870000
    minTime = 999
    maxTime = 0
    minTemp = 0
    maxTemp = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count +=1
        else:
            time_minutes = (int(row[2]) - timeZero)/(1000000000*60)
            temp_reading = (int(row[0][2:6]))
            temp_degrees = ((temp_reading/4095)*1.1-0.5)/0.01
            if( time_minutes< minTime):
                minTime = time_minutes
            if(time_minutes > maxTime):
                maxTime = time_minutes
            if(temp_degrees < minTemp):
                minTemp = temp_degrees
            if(temp_degrees > maxTemp):
                maxTemp = temp_degrees
    
    time_bucket_size = 1
    temp_bucket_size = 1
    number_of_buckets = (maxTime-minTime)/time_bucket_size
    number_of_buckets_temp = (maxTemp-minTemp)/temp_bucket_size
    tempBuckets = [0] * math.ceil(number_of_buckets_temp)
    timeBuckets =[]
    for i in range(0, math.ceil(number_of_buckets)):
        timeBuckets += [tempBuckets.copy()]
    print(f'Times: {minTime} {maxTime}')
    print(f'Temps: {minTemp} {maxTemp}')
    print(len(timeBuckets))
    print(len(tempBuckets))

with open('log.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count +=1
        else:
            time_minutes = (int(row[2]) - timeZero)/(1000000000*60)
            temp_reading = (int(row[0][2:6]))
            temp_degrees = ((temp_reading/4095)*1.1-0.5)/0.01
            index =  math.floor((time_minutes/maxTime)*number_of_buckets)
            index_t =  math.floor((temp_degrees/maxTemp)*number_of_buckets_temp)
            timeBuckets[index][index_t] = timeBuckets[index][index_t] +1

    #print(timeBuckets)

def groundTrueTemp(somethingthatisnotkeyword):
    if(somethingthatisnotkeyword == 0 ): return 69
    return 114.992 * (somethingthatisnotkeyword ** (-0.3055))

rowTempStatistics = {}
rowTimeStatistics = {}

for row in range(0,len(timeBuckets[0])):
    mini = 99999
    maxi = 0
    total = 0
    count = 0
    avg = 0
    for i in range(0,len(timeBuckets)):
        numberOfObservationsInBucket = timeBuckets[i][row]
        if numberOfObservationsInBucket > 0:
            if i < mini:
                mini = i
            if i > maxi:
                maxi = i
            total = total + i * numberOfObservationsInBucket
            count = count + numberOfObservationsInBucket
    if count > 0:
        avg = total / count
    rowTimeStatistics[row]= (mini,maxi,avg)
    rowTempStatistics[row]= (groundTrueTemp(maxi),groundTrueTemp(mini),groundTrueTemp(avg))
    
index_t =  math.floor((37/maxTemp)*number_of_buckets_temp)  
print("stats for 37 degrees: %s", rowTimeStatistics[index_t])
print("stats for 37 degrees: %s", rowTempStatistics[index_t])



H = np.array(timeBuckets).T

H = np.ma.masked_where(H ==0, H)

cmap = plt.cm.get_cmap("viridis")
cmap.set_bad(color='black')

print(temp_bucket_size)
print(number_of_buckets_temp)
fig = plt.imshow(H, extent = [0,120,0,math.ceil(number_of_buckets_temp)*temp_bucket_size], origin="lower")
plt.colorbar()
plt.show()
