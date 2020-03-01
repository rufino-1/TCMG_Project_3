#### Header
# Name:     Rufino A. Oregon
# UIN:      826004309
# CLASS:    TCMG 412
# SECTION:  500
# PROJECT:  3
# DATE:     2/17/2020

####Imports
import os.path
from os import path
import requests
####Functions

####Main

#Variables
count = 0
totalLines = 0
dataDictionary = {}
error4xx = 0
error3xx = 0
countBad = 0
fileDictionary = {}
tempDate = ''
counter0 = 0
tempMonth = ''

# Checking if log file is in directory
if(not(path.exists("log.txt"))):
    print("Log file not found. Downloading log file.")
    log_url = "https://s3.amazonaws.com/tcmg476/http_access_log"
    r = requests.get(log_url)
    with open("log.txt",'wb') as f: 
        f.write(r.content) 
    r.close()
else:
    print("Log file is in directory.")

fileID = open('log.txt','r')

for line in fileID:
    count += 1
totalLines = count

fileID.seek(0)       # Resetting pointer to the first row of the file
############
count1 = 0
date = ""
badID = open("badLines.txt",'w')
# Parsing to check requests per day
print()
print("Parsing to check requests per day")
for line in fileID:
    lineVector = line.split()
    if len(lineVector) == 10:

        ##################### Populating Files Dictionary
        if fileDictionary.get(lineVector[6],-1) == -1:
            fileDictionary[lineVector[6]] = 1
        else:
            fileDictionary[lineVector[6]] += 1
        #####################

        ##################### Counting 4xx and 3xx errors 
        if lineVector[9][0] == '4':
            error4xx += 1
        elif lineVector[9][0] == '3':
            error3xx += 1
        
        
        #####################
        date = lineVector[3].split(':')
        date = date[0]
        date = date[1:]

        ##################### Creating new smaller files per month
        tempDate = date.split('/')
        tempDate = tempDate[1]

        if counter0 == 0:
            tempMonth = tempDate
            monthID = open(tempMonth + ".txt",'w')
            monthID.write(line)
            counter0 += 1
        elif tempMonth != tempDate:
            monthID.close()
            tempMonth = tempDate
            monthID = open(tempMonth + ".txt",'w')
            monthID.write(line)
        elif tempMonth == tempDate:
            monthID.write(line)

        #####################
        if dataDictionary.get(date,-1) == -1:
            dataDictionary[date] = 0
        else:
            dataDictionary[date] = dataDictionary[date] + 1
    else:
        badID.write(line)
        countBad += 1
badID.close()
monthID.close()
# print(dataDictionary)
print("requests per day: ")
for i, j in dataDictionary.items():
    print(i, j)

# Parsing to check requests per week
print()
print("Parsing to check requests per week")
counter = 0
weekNumber = 1
currentWeek = ''
dataWeeks = {}

for i, j in dataDictionary.items():
    if counter == 0:
        currentWeek = "Week " + str(weekNumber)
        dataWeeks[currentWeek] = j
        counter += 1
    else:
        dataWeeks[currentWeek] = j + dataWeeks[currentWeek] 
        counter += 1
    if counter == 7:
        counter = 0
        weekNumber += 1

print("Requests per week: ")   
for i, j in dataWeeks.items():
    print(i, j)
      
# Parsing to check requests per month
print()
print("Parsing to check requests per month")
dataMonths = {}
counter = 0
curerntMonth = ''
tempSTR = ''
for i, j in dataDictionary.items():
    tempSTR = i.split('/')
    tempSTR = tempSTR[1]
    if dataMonths.get(tempSTR,-1) == -1:
        dataMonths[tempSTR] = j
    else:
        dataMonths[tempSTR] += j

print("Requests per month: ")     
for i, j in dataMonths.items():
    print(i, j)


# How many total requests were made in the time period represented in the log?
# How many requests were made on each day? per week? per month?
# What percentage of the requests were not successful (any 4xx status code)?
# What percentage of the requests were redirected elsewhere (any 3xx codes)?
# What was the most-requested file?
# What was the least-requested file?

print()
#print("4xx errors: " + str(error4xx))
percent4 = error4xx / totalLines * 100 
print("Percentage of the requests were not successful: %.2f%%" % percent4)

#print("3xx errors: " + str(error3xx))
percent3 = error3xx / totalLines * 100 
print("\nPercentage of the requests were redirected elsewhere: %.2f%%" % percent3)


#print("Bad Lines: " + str(countBad))
print("\nTotal requests that were made in the time period represented in the log: %d" % totalLines)

##################### Parsing to check least and most requested file
maxNumber = fileDictionary["index.html"]
maxFile = 'index.html'
minNumber = fileDictionary["index.html"]
minFile = 'index.html'
for i, j in fileDictionary.items():
    if  j > maxNumber:
        maxNumber = j
        maxFile = i
    if j < minNumber:
        minNumber = j
        minFile = i
    # print(i, j)
    
print()
print("The most-requested file is: %s" % maxFile)
print()
print("The least-requested file is: %s" % minFile)
#####################








print("\n^^^^^End of Code^^^^^")