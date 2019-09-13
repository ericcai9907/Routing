newfile = open('ANSIprettycaliroads2.txt', 'w+')
filePath = 'ANSIprettycaliroads1.txt'
with open(filePath) as file:
    for line in file:
        if line != '\n':
            newfile.write(line.strip())
            newfile.write('\n')


print("done")
