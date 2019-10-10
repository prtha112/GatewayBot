# Python program to illustrate the concept 
# of threading 
from datetime import datetime
import multiprocessing
import os 
import configparser
import logging
import logging.handlers
import wmi
import time
import psutil
import random
import pyautogui

config = configparser.ConfigParser()
config.read('config/config.ini')

appname = str(config['DEFAULT']['appname'])
app_version = str(config['DEFAULT']['app_version'])
gateway_path = config['DEFAULT']['gateway_path']
interval = int(config['DEFAULT']['interval_check'])
position_image = str(config['DEFAULT']['position_image'])
memory_percen = float(config['DEFAULT']['memory_percentage'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler('debug.log', when='D', interval=1, backupCount=7)
logger.addHandler(handler)

print("Start Gateway Bot Management")
print("Power by. essoft")
print("Version: ", app_version)

logger.info("Start Gateway Bot Management")

stackProcessId = []

def findProcess():
    maxMem = 0.00
    processID = None
    for proc in psutil.process_iter():
        try:
            if proc.name() == appname:
                processMem = proc.memory_info().rss / (1024 * 1024)
                stackProcessId.append(proc.pid)
                if processMem > maxMem:
                    processID = proc.pid
                    maxMem = processMem
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return maxMem, processID

def totalMem():
    sysMem = wmi.WMI()
    return float(sysMem.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024 * 1024)

def logInfo(input_time, input_state):
    logger.info("%s : %s ", input_time, input_state)

def loopCheckMem():
    while True:
        time.sleep(interval)
        logInfo(datetime.fromtimestamp(time.time()), "Check time")
        process = findProcess()
        if ((process[0] / totalMem()) > memory_percen) and process[1] != None:
            for stk in stackProcessId:
                try:
                    p = psutil.Process(stk)
                    p.terminate()
                    logger.info("%s : Memory overflow kill pid at: %s", format(datetime.fromtimestamp(time.time())), stk)
                    print(p)
                except psutil.NoSuchProcess:
                    continue
            stackProcessId = []
            openPro()
        else:
            if process[1] == None:
                openPro()
            logInfo(datetime.fromtimestamp(time.time()), "Memory it's ok")
        logInfo(datetime.fromtimestamp(time.time()), "End loop")
  
def loopImageProcessing():
    while True:
        time.sleep(random.randrange(15, 20))
        logInfo(datetime.fromtimestamp(time.time()), "Loop check connect")
        position = pyautogui.locateOnScreen(position_image)
        if (position != None):
            try:
                position_point = pyautogui.center(position)
                x = position_point.x
                y = position_point.y
                pyautogui.click(x, y)
                logInfo(datetime.fromtimestamp(time.time()), "Click connect")
            except TypeError:
                pass

def processMem(): 
	loopCheckMem()
	print("Process running worker1")
  
def processConnect(): 
	loopImageProcessing()
	print("Process running worker2")
  
if __name__ == "__main__": 
	multiprocessing.freeze_support()
	p1 = multiprocessing.Process(target=processMem)
	p2 = multiprocessing.Process(target=processConnect) 
  
    # starting processes 
	p1.start()
	p2.start() 
  
    # process IDs 
	print("ID of process p1: {}".format(p1.pid))
	print("ID of process p2: {}".format(p2.pid)) 
  
    # wait until processes are finished
	p1.join()
	p2.join()