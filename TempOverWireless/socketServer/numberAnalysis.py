import csv

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

print('Count is: ')
with open('logFromServer4.csv', 'r') as csvfile:
    count = 0
    sum = 0
    oofCount = 0
    prevTime = 0
    currentTime = 0
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if RepresentsInt(row[0]):
            try:
                if count == 0:
                    prevTime = int(row[4])
                else:
                    currentTime = int(row[4])
                    sum+=(currentTime-prevTime) 
                    prevTime = currentTime
                count+=1
            except:
                print('oof')
                print(row)
                oofCount+=1
    print(str(oofCount))
    print(str(count))
    print(str(sum))
    avg = int(sum / count)
    print(str(avg))
    


