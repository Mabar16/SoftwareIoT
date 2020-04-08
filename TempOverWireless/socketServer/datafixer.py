import csv

rows = []
oofs = []
with open('log100ms.csv', 'r') as file_object:
    csv_reader = csv.reader(file_object, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count +=1
        if line_count == 1:
            print(f'Column names are {", ".join(row)}')
        else:
            if len(row) == 5:
                rows.append(row)
            elif len(row) > 5:
                newrow = []
                index = 0
                temp = row[0]
                while len(row) > 5:
                    newrow.append(temp)
                    newrow.append(row[1])
                    newrow.append(row[2])
                    timestamp = row[3][0:len(row[3])-4]
                    newrow.append(timestamp)
                    temp =  row[3][len(row[3])-4:]
                    row = row[3:]
                    rows.append(newrow)
                    newrow = []
                if len(row) < 5:
                    oofs.append((line_count,row))
                else:
                    rows.append([temp,row[1],row[2],row[3],row[4]])

print(len(oofs))

with open('fixed100ms.csv', 'a') as file_object:
    file_object.write("temp,light,count,pycomtime,laptoptime    \n")
    for row in rows:
        if(len(row) > 4):
            file_object.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+ "\n")
        elif len(row) > 3:
            file_object.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+ "\n")
        else:
            print("BADLINE: " + str(row))
