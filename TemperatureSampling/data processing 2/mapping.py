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
    temp_bucket_size = 5
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

def groundTrueTemp(time):
    if(math.isnan(time)): return float('NaN')
    if(time == 0): return 69
    return max(26,min(60,114.992 * (time ** (-0.3055))))

valuesInBucket ={}
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
            if(temp_degrees >= 35 and temp_degrees < 40):
                valuesInBucket[temp_degrees] = groundTrueTemp(time_minutes)


with open('histogram.csv',mode='w') as csv_file:
    writer = csv.writer(csv_file)
    headers=("measuredTemp", "trueTemp")
    writer.writerow(headers)
    for i in valuesInBucket:
        content = (i,valuesInBucket[i])
        writer.writerow(content)


