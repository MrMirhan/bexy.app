import logging, datetime, time, os, sys
import config as cf
from re import search

date = str(datetime.datetime.now())
todayDate = str(date.split(" ")[0])
nowTime = str(date.split(" ")[1]).split(":")
nowTime = str(nowTime[0]) + "." + nowTime[1] + "." + str(round(float(nowTime[2])))
try:
    os.makedirs(f"logs/" + cf.branch + f"/{todayDate}")    
    print("Todays logging directory " , todayDate ,  " created.")
    open(f"logs/" + cf.branch + f"/{todayDate}/{nowTime}.log", "w")
    logging.basicConfig(filename=f"logs/" + cf.branch + f"/{todayDate}/{nowTime}.log", filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning('Process started.')
except FileExistsError:
    print("This process started time " , nowTime ,  " logging file created.")  
    open(f"logs/" + cf.branch + f"/{todayDate}/{nowTime}.log", "w")
    logging.basicConfig(filename=f"logs/" + cf.branch + f"/{todayDate}/{nowTime}.log", filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning('Process started.')

def sendLog(message):
    if search("raised", str(message)):
        return
    logging.warning(message)
    print(message)