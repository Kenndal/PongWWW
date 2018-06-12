
# dictionary
programElements = {}


# read data from config file
def readFile():
    f = open('Config.txt', 'r')

    for line in f:
        key = line.split(";")[0]  # read key from config file
        value = line.split(";")[1]  # read value from config file
        value = value.replace("\n", "")  # replace
        programElements[key] = value  # add value to dictionary









