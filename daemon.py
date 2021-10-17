#!/bin/python
import os
import sys
import signal
from utils import *

from calendarPipe import PIPE_FILE
CSV_FILE = 'cald_db.csv'

def exit_program(signum, frame):
    os.unlink('/tmp/calendar_link')
    print("\nbye\n")
    sys.exit()



def proccess(commond, data):
    # get commond array
    cmdList = commond.split()

    head = cmdList.pop(0)

    if not checkDate(cmdList[0]):
        log("Unable to parse date")
        return

    
    if head == 'ADD':
        if len(cmdList) == 1:
            log('Missing event name')
            return
        # proccess ADD
        if len(cmdList) == 2:
            cmdList.append(' ')
        # create a new dataframe
        data.append(cmdList)
        saveCsv(CSV_FILE, data)
            


    elif head == 'DEL':
        # proccess DEL

        # with open(CSV_FILE, 'r')
        # find the date
        data = [record for record in data if not(record[0] == cmdList[0] and record[1] == cmdList[1])]    
        # save data
        saveCsv(CSV_FILE, data)
        # data.to_csv(CSV_FILE, index=False)


    elif head == 'UPD':
        if len(cmdList) < 3:
            log('Not enough arguments given')
            return
        if len(cmdList) == 3:
            cmdList.append(' ')
        
        updated = False
        # proccess UPD
        for record in data:
            if record[0] == cmdList[0] and record[1] == cmdList[1]:
                record[1] = cmdList[2]
                record[2] = cmdList[3]
                updated = True

        if not updated:
            log('Unable to update, event does not exist')
        
        # save data
        saveCsv(CSV_FILE, data)

    return data

def createLink(path):
    os.link(path, '/tmp/calendar_link')


def run():
    global CSV_FILE
    signal.signal(signal.SIGINT, exit_program)

    # create if not exist
    if not os.path.exists(PIPE_FILE):
        os.mkfifo(PIPE_FILE)

    # read args
    if(len(sys.argv) > 1):
        CSV_FILE = sys.argv[1] + '/cald_db.csv'
    


    # init file head
    with open(CSV_FILE, "w") as f:
        f.write('DATE,EVENT,DESCRIPTION')

    createLink(CSV_FILE)

    # init log file
    with open(LOG_FILE, "w") as f:
        f_log = f.write('# this is a log file\n')

    # create file link
    data = readCsv(CSV_FILE)

    while True:
        # open pipe
        pipe = open(PIPE_FILE, 'r')

        # read pipe
        # receive = os.read(pipe, 200).decode()
        receive = pipe.readline()

        data = proccess(receive, data)
        # test if the commond is received
        # if len(receive) !=0 and not QUIT_SIG:
        #     print(receive)


    pipe.close()

if __name__ == '__main__':
    run()