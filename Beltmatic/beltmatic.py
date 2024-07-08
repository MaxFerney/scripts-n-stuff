
import math
print('''
usage: `FindNum(goal)`

gets numbers near another number via functions and small numbers.

setDivs(range)
calculates all divisors between 2 and range

setExp(range)
calculates all exponents leading to range

''')
from enum import Enum
class diveT(Enum):
    base=1
    divide=2
    exponent=3
    add=4

def insertIntoEquation(diveType,diveArray, goal):
    match(diveType):
        case diveT.base:
            return goal
        case diveT.divide:
            return f'{diveArray}'
global SavedNums
class FindNum:
    goal = 0
    divs = {}
    divRange = 0
    exponents = {}
    expRange = 0
    adds = {}
    diveList = []
    diveType = diveT.base
    expDistance = None
    diveMessage = 'note when splitting number up'
    equationPart = f'[6]*9 = 54'
    shorthandEquation = '6*9'
    locked = False
    # [2, [2, 5], [7, 2, 1]]
    
    def __init__(self, 
                 goal, 
                 equationPart='[6]*9 = 54'):
        self.goal = int(goal)
        self.equationPart = equationPart
        self.shorthandEquation = str(goal)

        searchVal = goal//2
        self.setDivs(int(searchVal))
        self.setExp(int(searchVal), 200)


    def __str__(self):
        # # not yet implemented
        # self.getDivs()
        # self.getExp(2000)
        return str(self.goal)
    
    
    def formatShorthand(self, nestLvl=0):
        posNegSign = '+'
        internalString = ''
        if(self.diveType==diveT.divide):
            internalString = f'({self.diveList[0].formatShorthand(nestLvl+1)}*{self.diveList[1].formatShorthand(nestLvl+1)})'
        elif(self.diveType==diveT.exponent):
            if(self.expDistance<0):
                posNegSign = '-'
            else:
                posNegSign = '+'
            internalString = f'(({self.diveList[0].formatShorthand(nestLvl+1)}^{self.diveList[1].formatShorthand(nestLvl+1)}){posNegSign}{self.diveList[2].formatShorthand(nestLvl+1)})'
        elif(self.diveType==diveT.base):
            internalString = f'{self.goal}'
        if(nestLvl==0):
            internalString += f'={self.goal}'
        return internalString
    
    def setDive(self, findNumArray, diveMessage):
        self.diveMessage = diveMessage
        self.diveList = findNumArray
        self.locked = True

    def printPretext(self, info=''):
        print('\nGoal: '+str(self.goal)+' | '+info+'\n'+('-'*37))

    def setAdds(self):
        adds={}
        for a in range(1, self.goal-1):
            
        self.adds=adds
        self.getAdds()
    
    def getAdds(self):
        pass

    def selectAdd(self):
        self.printPretext()
        print('key + value')
        pass


def selectDiv(self):
        self.printPretext('range: '+str(self.divRange))
        print('key * value')
        for k,v in self.divs.items():
            print('['+str(k)+'] * '+str(v))
        while True:
            try:
                keySelection = int(input('select key: '))
                valueSelection = self.divs.get(keySelection)
                newEntry = [ 
                    FindNum(keySelection,f'[{keySelection}]*{valueSelection}={self.goal}'), 
                    FindNum(valueSelection, f'{keySelection}*[{valueSelection}]={self.goal}')
                ]
                self.diveType = diveT.divide
                self.setDive(newEntry, f"goal {self.goal} Divided! into more")
                return newEntry
            except(KeyError):
                print('Invalid entry, try again')


    def setDivs(self, divRange=20):
        divs = {}
        self.divRange = divRange
        for d in range(2,int(divRange)+1):
            v = self.goal/d
            if (v).is_integer():
                divs[d] = int(v)
        
        self.divs = divs
        self.getDivs()
##        return divs

    def getDivs(self):
        self.printPretext('range: '+str(self.divRange))
        for k,v in self.divs.items():
            print(str(k)+' * '+str(v))
    
    def selectDiv(self):
        self.printPretext('range: '+str(self.divRange))
        print('key * value')
        for k,v in self.divs.items():
            print('['+str(k)+'] * '+str(v))
        while True:
            try:
                keySelection = int(input('select key: '))
                valueSelection = self.divs.get(keySelection)
                newEntry = [ 
                    FindNum(keySelection,f'[{keySelection}]*{valueSelection}={self.goal}'), 
                    FindNum(valueSelection, f'{keySelection}*[{valueSelection}]={self.goal}')
                ]
                self.diveType = diveT.divide
                self.setDive(newEntry, f"goal {self.goal} Divided! into more")
                return newEntry
            except(KeyError):
                print('Invalid entry, try again')
                
    def setExp(self, expRange=20, exclusion=3000):
        exponents = {}
        self.expRange = expRange
        for ex in range(2, int(expRange)+1):
            exponents[ex] = int(round(self.goal**(1./ex)))

        self.exponents = exponents
        self.getExp(exclusion)
##        return exponents

    def getExp(self, exclusion=3000):
        self.printPretext('range: '+str(self.expRange)+', exclusion: '+str(exclusion))
        for k,v in self.exponents.items():
            mult = round(v**k,2)
            distance = abs(round(self.goal-mult))
            if(distance <= exclusion and mult!=1):
                print(str(v)+'^'+str(k)+' = '+str(mult)+' | '+str(distance)+' away')

    def selectExp(self, exclusion=3000):
        self.printPretext('range: '+str(self.expRange)+', exclusion: '+str(exclusion))
        print('[key] value^key = result | remainder away')
        for k,v in self.exponents.items():
            mult = round(v**k,2)
            distance = abs(round(self.goal-mult))
            if(distance <= exclusion and mult!=1):
                cryptidString = f'[{k}] {v}^{k} = {mult} | {distance} away'
                print(cryptidString)
        
        while True:
            try:
                keySelection = int(input('select key: '))
                value=self.exponents.get(keySelection)
                mult = round(value**keySelection,2)
                distance = abs(round(self.goal-mult))
                # positive = False
                # if(round(self.goal-mult)>=0):
                #     posNeg=True
                self.expDistance = round(self.goal-mult)
                print('goal-mult'+str(round(self.goal-mult)))
                newEntry = [ 
                    FindNum(value, f'[{value}] ^ {keySelection} = {mult} ({distance} away from {self.goal})'),
                    FindNum(keySelection,f'{value} ^ [{keySelection}] = {mult} ({distance} away from {self.goal})'), 
                    FindNum(distance,f'{value} ^ {keySelection} = {mult} ([{distance}] away from {self.goal})'),
                ]
                self.diveType = diveT.exponent
                self.setDive(newEntry, f"goal {self.goal} Exponentiated! into more")
                return newEntry
            except(KeyError):
                print('invalid entry, try again')

        

class displayObject:
    storedValue=NotImplemented
    displayString=''
    def __init__(self, VALUE, DISPLAY) -> None:
        self.storedValue = VALUE
        self.displayString = DISPLAY
    def __str__(self):
        message = 20*'+'
        if(type(self.storedValue)==list):
            message+=self.displayString+'\n'
            message+='List\n'
            for i in range(len(self.storedValue)):
                message+=f"[{i}] - {self.storedValue[i]}\n"

        else:
            message+=f"\n Value: {str(self.storedValue)}\n Display: {str(self.displayString)}"
        return message


mainGoal = FindNum(4390, 'Goal/Base Number')

def menuString(nestLevel=0):
    if nestLevel==0:
        exitString = f'Exit APPLICATION'
    else:
        exitString = f'Exit (Go Up. Nest {nestLevel})'
    return f"""
{20*'#'}
[0] set current findNum
[1] dive (modify) current findnum
[2] set index
[3] view all
[4] {exitString}

"""

findNumDescription = f"""
{30*'#'}
[1] select div
[2] select exp
[3] exit (go back)
[4] print all

"""

saveValue=None
minified=None

def getValuesFromFindNumArray(findNumArray):
    printArray = []
    if(type(findNumArray)==list):
        for findnum in findNumArray:
            if(type(findnum) == FindNum):
                printArray.append(findnum.goal)
            elif(type(findnum)==list):
                newVals = getValuesFromFindNumArray(findnum)
                printArray.append(newVals)
    elif (type(findNumArray)==FindNum):
        printArray.append(findNumArray.goal)
    return printArray


def formatStringForFindnum(findNumObject:FindNum, nestLevel=0):
    nestIndent = '\t'*nestLevel
    singlePrintString = f"""------------
{nestIndent}Goal: {findNumObject.goal}
{nestIndent}Equation Part: {findNumObject.equationPart}
{nestIndent}------------"""
    
    if(findNumObject.locked):
        subArrayMessage = ''
        for fNum in findNumObject.diveList:
            subArrayMessage += f"{formatStringForFindnum(fNum,nestLevel+1)}\n"
        divePrintString = f"""{nestIndent}++++++++++++++++++++++++++++++++
{nestIndent}Goal: {str(findNumObject.goal)}
{nestIndent}Equation Part: {findNumObject.equationPart}
{nestIndent}Dive Message: {findNumObject.diveMessage}
{nestIndent}
{nestIndent}Parts: vvvvvvvvvv
{nestIndent}{subArrayMessage}
{nestIndent}^^^^^^^^^^^^^^^^^
{nestIndent}
{nestIndent}++++++++++++++++++++++++++++++++"""
        return divePrintString
    return singlePrintString

def menu(baseFindNum:FindNum, nestLevel=0, doinADive=False):
    currentIndex = 0

    if(nestLevel==0):
        global minified
        minified = baseFindNum.formatShorthand()

    def getVerbose():
        if(baseFindNum.locked):
            diveList = baseFindNum.diveList
        else:
            diveList = [baseFindNum]
        return f'Verbose Equation: {diveList[currentIndex].equationPart}'
    def printState():
        if(baseFindNum.locked):
            diveList = baseFindNum.diveList
        else:
            diveList = [baseFindNum]
        # Main Object:{formatStringForFindnum(baseFindNum)}
        print(f"""
###################################################
        Minified Equation: {baseFindNum.formatShorthand()}
        currentIndex: {currentIndex}
        currentNest:  {nestLevel}
        Selected Value: [{diveList[currentIndex]}]
        {getVerbose()}
        """)
    

    
    invalid = True
    while True:
        
        #Input Current Level Input
        if(doinADive):
            print(" lol did a dive")
            uInput = 1
        else:
            printState()

            print(menuString(nestLevel))
            print('__________________')
            uInput = int(input('input MENU option: '))

        #User Input Handling
        match(uInput):
            case 0: # set current findNum
                print('--Set findNum')    
                findVal = int(input('set current FindNum(input): '))
                baseFindNum = FindNum(findVal, 'Overwrote Current Findnum')
            case 1: # modify findNum
                print('--Dive findNum')
                exit = False
                if(baseFindNum.locked):
                    menu(baseFindNum.diveList[currentIndex], nestLevel+1, True) # Dive into
                    exit = True
                else:
                    # Print Findnum Values
                    baseFindNum.getDivs()
                    baseFindNum.getExp()

                    invalidInput = True
                    while (invalidInput == True):
                        print(findNumDescription)
                        uInput = int(input('SUBMENU option: '))
                        invalidInput = False
                        match(uInput):
                            case 1: # div
                                baseFindNum.selectDiv()
                                # baseFindNum.setDive(newEntry, f"goal {baseFindNum.goal} Divided! into more")
                                
                                # saveValArray[currentIndex] = newEntry
                            case 2: # exp
                                baseFindNum.selectExp()
                                # baseFindNum.setDive(newEntry, f"goal {baseFindNum.goal} Exponentiated! into more")
                            case 3: # exit
                                print('--exit')
                                exit=True
                                continue
                            case 4: #print all
                                # print(formatStringForFindnum(baseFindNum))
                                print(baseFindNum.formatShorthand())
                                invalidInput = True
                            case _:
                                print('invalid input')
                                invalidInput = True
                    
                            
                # if(not exit):
                #     menu(baseFindNum.diveList[currentIndex],nestLevel+1)

            case 2: # change index
                print('--change index')
                if(not baseFindNum.locked):
                    print('findNum not locked. please dive[1] or go up[4].')
                    invalidInput = True
                    continue
                else:
                    print('Current Values: ')
                    print(getVerbose())
                    for i in range(len(baseFindNum.diveList)):
                        item = baseFindNum.diveList[i]
                        if(item.locked):
                            print( f"[{i}] {item.goal} eq: {item.equationPart}")
                        else:
                            print(f'[{i}] Dive into {item.goal}')
                    currentIndex = int(input('Select Index: '))
                
            case 3: # view all
                print('--view all')
                # print(formatStringForFindnum(saveValue))
                print(baseFindNum.formatShorthand())
                print(f'Global: {minified}')
                # print(getValuesFromFindNumArray(saveValArray))
                # print(getValuesFromFindNumArray(saveValue))
            case 4: #exit
                print('--exit')
                invalid=False
                return
            case _:
                print('--default')
                #default
                print('default')
                invalid = True
                doinADive=False
        # Set doinADive back to false since it's just a one time toggle.
        doinADive=False

saveValue = mainGoal
saveIndex = 0


print('-'*20+'\ncurrent save value: ',end='')
# print(getValuesFromFindNumArray(saveValue))
print('save index: '+str(saveIndex))

menu(saveValue,0)
    
    


