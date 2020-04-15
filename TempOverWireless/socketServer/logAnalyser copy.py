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
    times = []
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
                prev_tim = ptim
                prev_cunt = cunt
                times.append(ptim)
        else:
            if(row[0].isnumeric() and len(row) > 4 and row[4].isnumeric()):
                temp = float(row[0])
                lite = float(row[1])
                cunt = float(row[2])
                ptim = float(row[3])
                ltim = float(row[4])
                dif = ptim-prev_tim
                prev_tim = ptim
                times.append(ptim)

                if cunt == 0:
                    list.sort(times)
                    prevtime = times[3]
                    for time in times[4:]:
                        totaldiff += time-prevtime
                        diffCount += 1
                        prevtime = time

                    print(str(line_count) + " -  avg diff: " + str((totaldiff / diffCount)/1000000000))
                    total_avg += totaldiff / diffCount
                    avg_cunt += 1
                    totaldiff = 0
                    diffCount = 0
                    times = []
                else:
                   pass
                prev_cunt = cunt
        
    
    list.sort(times)
    prevtime = times[3]
    for time in times[4:]:
        totaldiff += time-prevtime
        diffCount += 1
        prevtime = time

    print(str(line_count) + " -  avg diff: " + str((totaldiff / diffCount)/1000000000))
    total_avg += totaldiff / diffCount
    avg_cunt += 1
    totaldiff = 0
    diffCount = 0
    times = []
    print("avg avg: " + str((total_avg / avg_cunt)/1000000000)) 
 
    font = {'family' : 'normal',
        'size'   : 20}

    plt.rc('font', **font)

    # plt.hist(time_diffs, bins=[0,0.75,0.80,0.85,0.9,0.95,1,1.05,1.1,1.15,1.20,1.25,1.30,1.5])
    # plt.xlabel("Time difference [s]")
    # plt.ylabel("Count")


    # plt.boxplot(time_diffs, vert=False, whis=[1, 99])
    # plt.yticks([1], [''])
    # plt.xlabel("Time difference [s]")
    # plt.show() 
    variance  = numpy.var(time_diffs)
    print(variance)
            
         

    print(times[0:10])
    print(times[-10:])