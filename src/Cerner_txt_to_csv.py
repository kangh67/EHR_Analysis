# ----
# Convert txt to csv
# ----

import os
import re

# set data group
# raw data is in data/Cerner_Samples/
# csv data will be saved in data/Cerner_Samples_csv/
# column titles are in data/Cerner_Samples_csv/data_column_names.txt

rawData = "Cerner_Samples"
csvData = "Cerner_Samples_csv"
columnTitleFile = "data_column_names.txt"

# get data dir: /data/
data_dir = os.path.join(os.path.dirname("Cerner_txt_to_csv.py"), os.path.pardir)
rawData_dir = os.path.abspath(data_dir) + "/data/" + rawData
csvData_dir = os.path.abspath(data_dir) + "/data/" + csvData

fileList = os.listdir(rawData_dir)
print("Raw data folder is located at " + rawData_dir)
print("CSV data folder is located at " + csvData_dir)


def txt_to_csv(fileName):
    """
    :param fileName: .txt file name

    """
    outputFile = fileName.replace(".txt", ".csv")
    print("--- Converting file \"" + fileName + "\" to \"" + outputFile + "\"")
    inputFilePath = rawData_dir + "/" + fileName
    outputFilePath = csvData_dir + "/" + outputFile

    reading = open(inputFilePath, 'r')
    writing = open(outputFilePath, 'w')

    titles = get_column_title(fileName)
    writing.write(titles)
    if not titles.endswith("\n"):
        writing.write("\n")

    for eachline in reading:
        if re.search("\t", eachline):
            writing.write(eachline.replace("\t", ","))

    reading.close()
    writing.close()

def get_column_title(fileName):
    columnFile = csvData_dir + "/" + columnTitleFile
    reading = open(columnFile, 'r')

    title = "No Column Titles"

    for eachline in reading:
        if eachline.startswith(fileName):
            title = eachline.replace(fileName + ":", "").replace(" ", "")

    reading.close()
    return title

for txtFile in fileList:
    if txtFile.endswith(".txt"):
        txt_to_csv(txtFile)


