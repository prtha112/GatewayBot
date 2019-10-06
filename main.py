from datetime import datetime
import psutil
import time
import wmi
import subprocess
import configparser
import pyautogui
import logging
import logging.handlers

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
logger.info("Power by. essoft")
logger.info("Version: %s",app_version)

def findProcess():
    maxMem = 0.00
    for proc in psutil.process_iter():
        try:
            if proc.name() == appname:
                processMem = proc.memory_info().rss / (1024 * 1024)
                if processMem > maxMem:
                    processID = proc.pid
                    maxMem = processMem
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return maxMem, processID

def totalMem():
    sysMem = wmi.WMI ()
    return float(sysMem.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024 * 1024)

def checkConnectButton(position1):
    if (position1 != None):
        try:
            position_point = pyautogui.center(position1)
            x = position_point.x
            y = position_point.y
            pyautogui.click(x, y)
            print("Click Connect")
        except TypeError:
            pass

while True:
    time.sleep(interval)
    logger.info("%s : Check time ",datetime.fromtimestamp(time.time()))
    process = findProcess()
    if (process[0] / totalMem()) > memory_percen:
        p = psutil.Process(process[1])
        # p.terminate()
        logger.info("%s : Memory overflow kill pid at: %s mb", format(datetime.fromtimestamp(time.time())), format(process[0]))
        # subprocess.call(gateway_path)
        position = pyautogui.locateOnScreen(position_image)
        checkConnectButton(position)
    else: 
        position = pyautogui.locateOnScreen(position_image)
        checkConnectButton(position)
        logger.info("%s : Memory it's ok", format(datetime.fromtimestamp(time.time())))