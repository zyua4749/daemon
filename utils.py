LOG_FILE = '/tmp/cald_err.log'

def checkDate(date):
    dateList = date.split('-')
    if len(dateList) != 3:
        log('Unable to parse date')
        return 0

    elif len(dateList[0]) != 2 or len(dateList[1]) != 2 or len(dateList[2]) != 4:
        log('Unable to parse date')
        return 0
    return 1

def log(str):
    print(str)
    with open(LOG_FILE, "a") as f:
        f_log = f.write(str + '\n')


# check if interval time is valid
def checkInterval(start, end):
    if not (checkDate(start) and checkDate(end)):
        return 0
    start = start.split('-')
    end = end.split('-')

    # check if the start is before end
    for i in range(3):
        if start[2 - i] > end[2 - i]:
            log('Unable to Process, Start date is after End date')
            return 0

    return 1

# readCsv file
def readCsv(file_path):
    data = []
    with open(file_path, 'r') as f:
        # ignore the first line
        f.readline()
        for line in f.readlines():
            line = line.split("\n")
            data.append(line[0].split(","))
    return data

def saveCsv(file_path, data):
    with open(file_path, 'w') as f:
        f.write('DATE,EVENT,DESCRIPTION\n')
        for record in data:
            f.write(','.join(record)+'\n')