# Adapted from https://github.com/haloboy777/arfftocsv/blob/master/arffToCsv.py
from python import globals as glob
import os
import pandas as pd
import ntpath
import sys

# Getting all the arff files from the current directory
files = [glob.wdec_train, glob.wdec_test]

# Function for converting arff list to csv list
def toCsv(content):
    data = False
    header = ""
    newContent = []
    for line in content:
        if not data:
            if "@attribute" in line:
                attri = line.split()
                columnName = attri[attri.index("@attribute")+1]
                header = header + columnName + ","
            elif "@data" in line:
                data = True
                header = header[:-1]
                header += '\n'
                newContent.append(header)
        else:
            newContent.append(line.replace('true', '1').replace('false', '0'))

    return newContent

# Main loop for reading and writing files
for file in files:
    with open(file , "r") as inFile:
        content = inFile.readlines()
        path, ext = os.path.splitext(inFile.name)
        # name = ntpath.basename(path).split('_')[0]
        name = ntpath.basename(path)
        new = toCsv(content)
        with open('data/' + name + ".csv", "w") as outFile:
            outFile.writelines(new)

files = [f for f in os.listdir('data')]
for file in files:
    data = pd.read_csv('data/' + file)
    # remove columns with only zero
    data = data.loc[:, (data != 0).any(axis=0)]

    # check number of non-zero rows
    print(data.astype(bool).sum(axis=0))

    # write file
    with open('data/'+file, 'wb') as dst:
        data.to_csv('data/'+file, sep=',', encoding='utf-8', index=False)
        dst.seek(-1, os.SEEK_END)  # remove last empty line
        dst.truncate()



