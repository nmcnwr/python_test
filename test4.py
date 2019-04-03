filename ="FILE1.txt"

print("Filename: ",filename)


file = open(filename, "r")


for line in file:
    line = line.replace("\n", "")
    print(line)


file.close()


