#!/bin/python
import os
import sys
import time
from utils import *

PIPE_FILE = "/tmp/cald_pipe"
CSV_FILE = "/tmp/calendar_link"

def proccess(commond):
    # read data
    data = readCsv(CSV_FILE)

    # get commond head
    head = commond.pop(0)

    if head == 'GET':
        options = commond.pop(0)

        if options == 'DATE':
            # check arg format
            if not checkDate(commond[0]):
                return
            match = [record for record in data if record[0] == commond[0]]
            calendPrint(match)
        
        elif options == 'INTERVAL':
            # get start and end time
            start, end = commond[0], commond[1]
            # check args
            if not checkInterval(commond[0], commond[1]):
                return 
            # get index that match the interval time
            match = [record for record in data if record[0] >= commond[0] and record[0] <= commond[1]]
            calendPrint(match)

        elif options == 'NAME':
            if(len(commond) == 0):
                log("Please specify an argument")
                return
            if not checkDate(commond[0]):
                log("Unable to parse date")
                return
            # match the event name that start with the args
            match = [record for record in data if record[1].startswith(commond[0])]
            calendPrint(match)

# print due to format
def calendPrint(match):
    if(len(match) > 0):
        # get data list
        # print data
        for info in match:
            if info[2] != ' ':
                print("{} : {} : {}".format(info[0], info[1], info[2]))
            else: 
                print("{} : {} :".format(info[0], info[1]))

def run():
    if os.path.exists(PIPE_FILE):
        # only for write

        try:
            # get args and remove the file name
            pipe_commond = [commond for commond in sys.argv]
            pipe_commond.pop(0)

            head = pipe_commond[0]

            if head == 'UPD' or head == 'ADD' or head == 'DEL':
                pipe = os.open(PIPE_FILE, os.O_WRONLY)
                # send commond to daemon
                os.write(pipe, bytes(' '.join(pipe_commond), "UTF-8"))

                os.close(pipe)
            else:
                proccess(pipe_commond)

        except OSError:
            print("Pipe has been closed")
   
    else:
        print("PIPE DOESN't EXIST", file=sys.stderr)

if __name__ == '__main__':
    run()