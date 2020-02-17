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

if(not(path.exists("log.txt"))):
    print("Log file not found. Downloading log file.")
    log_url = "https://s3.amazonaws.com/tcmg476/http_access_log"
    r = requests.get(log_url)
    with open("log.txt",'wb') as f: 
        # Saving received content as a png file in 
        # binary format 
        # write the contents of the response (r.content) 
        # to a new file in binary mode. 
        f.write(r.content) 
else:
    print("Log file is in directory.")



#Testing Git to see if it updates! Again





















