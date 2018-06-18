# dictionary
programElements = {}
programDefaultElements = {}


# read data from default config file
def readDefaultFile():
    f = open('DefaultConfig.txt', 'r')  # open config file
    for line in f:
        key = line.split(";")[0]  # read key from default config file
        value = line.split(";")[1]  # read value from default config file
        value = value.replace("\n", "")  # replace
        if "Color" in key:
            programDefaultElements[key] = eval(value)
        else:
            programDefaultElements[key] = int(value)
    f.close()


# read data from config file
def readFile():
    readDefaultFile()
    f = open('Config.txt', 'r')  # open config file
    for line in f:
        key = line.split(";")[0]  # read key from config file
        value = line.split(";")[1]  # read value from config file
        value = value.replace("\n", "")  # replace
        if checkKey(key):
            checkValue(key, value)
        else:
            programElements.clear()
            setDefault()
            print('Wprowadzono domyślne parametry z powodu błędów w kluczach')
            print('Poprawne nazwy kluczy: [width, height, lineThickness, elementsColor, padColor, ballColor, menuColor]')
            break
    f.close()


# function to check compatibility
def checkValue(key, value):
    if "Color" in key:
        try:  # check if it is possible to change to tuple
            value = eval(value)  # change value to tuple
            k = 0
            for v in value:
                if v > 255 or v < 0:  # check color range.
                    programElements[key] = programDefaultElements[key]
                    print('Załadowano domyślą wartość ' + key)
                    check = False

                    break
                if v == 0:
                    k += 1
                if k == 3:  # Can't put 0, 0, 0, because of black background
                    programElements[key] = programDefaultElements[key]
                    print('Załadowano domyślą wartość ' + key)
                    check = False
                    break
                check = True

            if check:  # if color range is ok set config value
                programElements[key] = value
                print('Załadowano ' + key)
        except:  # if change to tuple is impossible set default value
            programElements[key] = programDefaultElements[key]
            print('Załadowano domyślą wartość ' + key)
    else:
        try:  # check if it is possible to change to int
            value = int(value)
            if value >= programDefaultElements[key]:  # check min value of board
                programElements[key] = value
                print('Załadowano ' + key)
            else:  # if not set default value
                programElements[key] = programDefaultElements[key]
                print('Załadowano domyślą wartość ' + key)
        except: # if change to int is impossible set default value
            programElements[key] = programDefaultElements[key]
            print('Załadowano domyślą wartość ' + key)


# Function to check right names of values
def checkKey(key):
    if key in programDefaultElements.keys():  # if key is in default range return True
        return True
    else:  # if not return false
        return False


# Function to set default values
def setDefault():
    for key in programDefaultElements.keys():
        programElements[key] = programDefaultElements[key]