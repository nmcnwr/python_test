import re


filename ="FILE1.txt"
filename2 ="FILE2.txt"


print("Filename: ",filename)
print("Filename2: ",filename2)

file = open(filename, "r")
file2 = open(filename2, "w")

for line in file:
    line = line.replace("\n", "")
    line = line.replace("=", "-")

    new_line    = re.split('-',line)

    print(line,new_line[0],new_line[1])
    line2=new_line[0],new_line[1]
    line2 = str(line2)
    file2.write(line2)


file.close()
