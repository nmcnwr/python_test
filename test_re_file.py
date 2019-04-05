import re


filename ="FILE1.txt"

print("Filename: ",filename)


file = open(filename, "r")


for line in file:
    line = line.replace("\n", "")
    line = line.replace("=", "-")

    new_line    = re.split('-',line)

    print(line,new_line[0],new_line[1],end=","),   print(", type:",type(new_line))


file.close()
