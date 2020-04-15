import numpy
import csv
import matplotlib.pyplot as plt

with open('fixed100ms.csv', 'r') as file_object:
    csv_reader = csv.reader(file_object, delimiter=',')

    line_count = 0
    prev_tim = 0
    prev_cunt = 0.0
    totaldiff = 0
    diffCount = 0
    total_avg = 0
    avg_cunt = 0
    time_diffs = []
    prunedCount = 0
    for row in csv_reader:
        line_count +=1
        if line_count == 1:
            print(f'Column names are {", ".join(row)}')
        elif line_count < 442:
            pass
        elif prev_tim == 0:
            if(row[0].isnumeric()):
                temp = float(row[0])
                lite = float(row[1])
                cunt = float(row[2])
                ptim = float(row[3])
                ltim = float(row[4])
                prev_tim = ltim
                prev_cunt = cunt
        else:
            if(row[0].isnumeric() and len(row) > 4 and row[4].isnumeric()):
                temp = float(row[0])
                lite = float(row[1])
                cunt = float(row[2])
                ptim = float(row[3])
                ltim = float(row[4])
                dif = ltim-prev_tim
                prev_tim = ltim
                if cunt == 0:
                    print(str(line_count) + " -  avg diff: " + str((totaldiff / diffCount)/1000000000))
                    total_avg += totaldiff / diffCount
                    avg_cunt += 1
                    totaldiff = 0
                    diffCount = 0
                else:
                    totaldiff += dif
                    diffCount += 1
                   # if dif/1000000000 < 0.2:
                    time_diffs.append(dif/1000000000)
                    #else:
                     #   prunedCount += 1
                prev_cunt = cunt
        
    
    total_avg += totaldiff / diffCount
    avg_cunt += 1
    print(str(line_count) + " -  avg diff: " + str((totaldiff / diffCount)/1000000000))
    print("avg avg: " + str((total_avg / avg_cunt)/1000000000)) 
 
    font = {'family' : 'normal',
        'size'   : 20}

    plt.rc('font', **font)

    plt.hist(time_diffs, bins = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2])
     #, bins=[0,0.75,0.80,0.85,0.9,0.95,1,1.05,1.1,1.15,1.20,1.25,1.30,1.5])
    plt.xlabel("Time difference [s]")
    plt.ylabel("Count")


    # plt.boxplot(time_diffs, vert=False, whis=[1, 99])
    # plt.yticks([1], [''])
    # plt.xlabel("Time difference [s]")
    plt.show() 
    variance  = numpy.var(time_diffs)
    print(variance)
    print(prunedCount)
    print(prunedCount/(len(time_diffs)+prunedCount))
            
    # list.sort(time_diffs)
    # print(time_diffs[:10])
         