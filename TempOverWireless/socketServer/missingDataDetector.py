import numpy
import csv
import matplotlib.pyplot as plt

with open('logFromServer4.csv', 'r') as file_object:
    csv_reader = csv.reader(file_object, delimiter=',')

    line_count = 0
    isFirst = True
    counts =  []
    countsListList = []
    for row in csv_reader:
        line_count +=1
        if line_count == 1:
            print(f'Column names are {", ".join(row)}')
        else:
            if(row[0].isnumeric() and row[2].isnumeric()):
                temp = float(row[0])
                lite = float(row[1])
                cunt = int(row[2])
                if cunt == 0 and not isFirst:
                    countsListList.append(counts)
                    counts = []
                else:
                    isFirst = False
                    counts.append(cunt)

    for countList in countsListList:
        print("len: " + str(len(countList)) + " . Last num: " + str(countList[-1]))
            
         