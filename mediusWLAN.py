#!/usr/bin/env python3

from pandas import read_html
from requests import get
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil
from memory_units import Unit,Memory
import csv
from pathlib import Path


fullURL         = "http://10.181.8.1:4501/?action=login"
baseUrl         = "http://10.181.8.1:4501"
actionEndpoint  = "?action="
actions         = ["login"]    

def poll():
    result  =   get("http://10.181.8.1:4501/",
    headers =   {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Host": "10.181.8.1:4501",
                    "Referer": "http://10.181.8.1:4501/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }
    )

    page = result.content.decode()

    data = read_html(page)[0]
    return data

def structureMediusData(data):

    desiredUnit = Unit.GIGA
    timePattern =  "%Y-%m-%d %H:%M"

    dataRaw     = data[1][1]
    dataTuple   = dataRaw.split(' / ')
    dataUsed    = Memory.from_str(dataTuple[0])
    dataMax     = Memory.from_str(dataTuple[1])
    
    dataStatus  = f"{dataUsed}/{dataMax}"

    timeEnd     = datetime.strptime(data[1][0],timePattern) 
    timeNow     = datetime.now()
    timeDelta   = relativedelta(timeEnd,timeNow)
    daysLeft    = timeDelta.days
    hoursLeft   = timeDelta.hours
    minutesLeft = timeDelta.minutes
    secondsLeft = (timeEnd - timeNow).total_seconds()

    daysLeftExact = ceil(secondsLeft / (60*60*24))

    dataBuf     = Memory(dataMax.bytes()-dataUsed.bytes(),Unit.BYTES)
    dataBuffer  =   dataBuf.to(desiredUnit)
    dailyBuf    = Memory(dataBuffer.bytes()/daysLeftExact,Unit.BYTES)
    dailyBuffer =   dailyBuf.to(desiredUnit)

    devsUsed, devsFree = data[1][2].split(' / ')
    deviceStatus = f"{devsUsed}/{devsFree} devices"

    if daysLeft   == 1:
        timeStatus = f"{daysLeft}d {hoursLeft:02}:{minutesLeft:02}"
    elif daysLeft == 0: 
        timeStatus = f"0d {hoursLeft:02}:{minutesLeft:02}"
    else: 
        timeStatus = f"{daysLeft}d {hoursLeft:02}:{minutesLeft:02}" 

    structuredData  = {
        'timeNow'       :   timeNow,
        'timeEnd'       :   timeEnd,
        'dataUsed'      :   dataUsed,
        'dataBuffer'    :   dataBuffer,
        'dailyBuffer'   :   dailyBuffer,
        'dataCap'       :   dataMax,
        'dataStatus'    :   dataStatus,
        'deviceStatus'  :   deviceStatus,
        'devsUsed'      :   devsUsed,
        'devsFree'      :   devsFree,
        'timeStatus'    :   timeStatus
    }

    return structuredData

def printSttructuredData(structuredData):

    print(  f"{structuredData['dataBuffer'].value:.2f}  {structuredData['dataBuffer'].suffix} remaining    "    \
            f"{structuredData['dailyBuffer'].value:.2f} {structuredData['dailyBuffer'].suffix} allowance    "    \
            f"{structuredData['dataStatus']}    "  \
            f"{structuredData['deviceStatus']}    "  \
            f"{structuredData['timeStatus']} left")

if __name__ == "__main__":
    rawData = poll()
    structuredData = structureMediusData(rawData)
    printSttructuredData(structuredData)

