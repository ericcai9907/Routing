#from pathlib import Path


newfile = open('ANSIprettycaliroads1.txt', 'w+')
filePath = 'ANSIcaliroads.txt'
with open(filePath) as file:
    for line in file:
        line = line.split('  ')
        for item in line:
            item.strip()
            newfile.write(item)
            newfile.write('\n')


print("done")
