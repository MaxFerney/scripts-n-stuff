
import math
print('''
usage: `FindNum(goal)`

gets numbers near another number via functions and small numbers.

setDivs(range)
calculates all divisors between 2 and range

setExp(range)
calculates all exponents leading to range

''')

class displayObject:
    storedValue=NotImplemented
    displayString=''
    def __init__(self, VALUE, DISPLAY) -> None:
        self.storedValue = VALUE
        self.displayString = DISPLAY
    def __str__(self):
        message = 20*'+'+'\n'
        if(type(self.storedValue)==list):
            message+=self.displayString+'\n'
            message+='List\n'
            for i in range(len(self.storedValue)):
                message+=f"[{i}] - {self.storedValue[i]}\n"
        elif(type(self.storedValue)==FindNum):

            subMessage=f"""
    FindNum({self.storedValue.goal})
    
"""
            message+=subMessage
        else:
            message+=f"\n Value: {str(self.storedValue)}\n Display: {str(self.displayString)}"
        return message

global SavedNums
class FindNum:
    goal = 0
    divs = {}
    divRange = 0
    exponents = {}
    expRange = 0
    savedNums = []
    # [2, [2, 5], [7, 2, 1]]
    
    def __init__(self, goal, storeMsg=''):
        self.goal = int(goal)
        searchVal = goal//2
        self.setDivs(int(searchVal))
        self.setExp(int(searchVal), 200)
        self.storeMsg = storeMsg


    def __str__(self):
        # not yet implemented
        self.getDivs()
        self.getExp(2000)
        return f'''
    FindNum Object ({self.goal})
'''

    def printPretext(self, info=''):
        print('\nGoal: '+str(self.goal)+' | '+info+'\n'+('-'*37))

    def setDivs(self, divRange=20, noShow=True):
        divs = {}
        self.divRange = divRange
        for d in range(2,int(divRange)+1):
            v = self.goal/d
            if (v).is_integer():
                divs[d] = int(v)
        
        self.divs = divs
        if not noShow:
            self.getDivs()
##        return divs

    def getDivs(self):
        self.printPretext('range: '+str(self.divRange))
        for k,v in self.divs.items():
            print(str(k)+' * '+str(v))
    
    def selectDiv(self) -> list[displayObject]:
        self.printPretext('range: '+str(self.divRange))
        print('key * value')
        for k,v in self.divs.items():
            print('['+str(k)+'] * '+str(v))
        while True:
            try:
                keySelection = int(input('select key: '))
                valueSelection = self.divs.get(keySelection)
                newEntry = [ 
                    displayObject(FindNum(keySelection),f'[{keySelection}]*{valueSelection}={self.goal}'), 
                    displayObject(FindNum(valueSelection), f'{keySelection}*[{valueSelection}]={self.goal}')
                ]
                return newEntry
            except(KeyError):
                print('Invalid entry, try again')
                
    def setExp(self, expRange=20, exclusion=3000, noShow=True):
        exponents = {}
        self.expRange = expRange
        for ex in range(2, int(expRange)+1):
            exponents[ex] = int(round(self.goal**(1./ex)))

        self.exponents = exponents
        if not noShow:
            self.getExp(exclusion)
##        return exponents

    def getExp(self, exclusion=3000):
        self.printPretext('range: '+str(self.expRange)+', exclusion: '+str(exclusion))
        for k,v in self.exponents.items():
            mult = round(v**k,2)
            distance = abs(round(self.goal-mult))
            if(distance <= exclusion and mult!=1):
                print(str(v)+'^'+str(k)+' = '+str(mult)+' | '+str(distance)+' away')

    def selectExp(self, exclusion=3000) -> list[displayObject]:
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
                # createdArray = [FindNum(keySelection), FindNum(value), FindNum(distance)]
                newEntry = [ 
                    displayObject(FindNum(value), f'[{value}] ^ {keySelection} = {mult} ({distance} away from {self.goal})'),
                    displayObject(FindNum(keySelection),f'{value} ^ [{keySelection}] = {mult} ({distance} away from {self.goal})'), 
                    displayObject(FindNum(distance),f'{value} ^ {keySelection} = {mult} ([{distance}] away from {self.goal})'),
                ]
                return displayObject(newEntry, f'Wrapper {value} ^ {keySelection} = {mult} ({distance} away from {self.goal})')
            except(KeyError):
                print('invalid entry, try again')

        


searchint = 4626
mainGoal = FindNum(searchint)

mainMenu = f"""
{20*'#'}
[0] set current findNum
[1] dive current findnum
[2] set index
[3] view all
[4] Exit

"""

findNumDescription = f"""
{30*'#'}
[1] select div
[2] select exp
[3] exit

"""

global saveValue

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

def menu(saveValArray:displayObject):
    
    currentIndex = 0

    def printState():
        
        print(f"""
        Save Title: {str(saveValArray.displayString)}
        Save Val Values: {str(saveValArray.storedValue)}
        currentIndex: {currentIndex}
        Selected Value: [{saveValArray}]
        """)
    invalid = True
    while True:
        invalid=False
        printState()

        print(mainMenu)
        uInput = int(input('input menu option: '))
        match(uInput):
            # WRITE
            case 0: # set current findNum
                print('--set current findNum')
                findVal = int(input('set current FindNum(input): '))
                # if(type(saveValArray)==displayObject) and (type(saveValArray.storedValue)==list):
                    
                # if(len(saveValArray)==0):
                #     saveValArray.append(displayObject(FindNum( findVal), f'InitiatorVal: {findVal}') )
                #     currentIndex = len(saveValArray)-1
                # else:
                saveValArray.storedValue[currentIndex] = displayObject(FindNum(findVal), f'InitiatorVal: {findVal}') 
            # MODIFY/UPDATE
            case 1: # modify findNum
                print('--modify findNum')
                if(type(saveValArray.storedValue[currentIndex])==list): # Dive into
                    menu(displayObject(saveValArray[currentIndex])) 
                else: #expand current
                    findVal = saveValArray.storedValue[currentIndex].goal
                    print(f"~FindNum: {findVal}~")
                    FindNum(findVal)
                    print(findNumDescription)

                    invalidInput = True
                    while (invalidInput == True):
                        uInput = int(input('SUBMENU option: '))
                        invalidInput = False
                        match(uInput):
                            case 1: # div
                                # newEntry = saveValArray[currentIndex].selectDiv()

                                newEntry = displayObject(saveValArray.storedValue[currentIndex].selectDiv(), f'InitiatorVal: {findVal}')
                                saveValArray.storedValue[currentIndex] = newEntry
                            case 2: # exp
                                # newEntry = saveValArray[currentIndex].selectExp()
                                newEntry = displayObject(saveValArray.storedValue[currentIndex].selectExp(), f'InitiatorVal: {findVal}')
                                saveValArray.storedValue[currentIndex] = newEntry
                            case 3: # exit
                                print('--exit')
                                return
                            case _:
                                print('invalid input')
                                invalidInput = True
                    
                            

                    menu(saveValArray.storedValue[currentIndex])

            case 2: # change index
                print('--change index')
                print('Current Values: ')
                
                for i in range(len(saveValArray.storedValue)):
                    item = saveValArray.storedValue[i]
                    if(type(item.storedValue)!=list):
                        print( f"[{i}] {item.goal}")
                    else:
                        print(f'[{i}] Dive into {item}')
                currentIndex = int(input('Select Index: '))
                
            case 3: # view all
                print('--view all')
                # print(getValuesFromFindNumArray(saveValArray))
                # print(getValuesFromFindNumArray(saveValue))
                print(saveValArray)
                print(saveValue)
            case 4: #exit
                print('--exit')
                return
            case _:
                print('--default')
                #default
                print('default')
                invalid = True

saveValue = displayObject([mainGoal],f'The og object {mainGoal.goal}')
saveIndex = 0


# print('-'*20+'\ncurrent save value: ',end='')
# print(getValuesFromFindNumArray(saveValue))
# print('save index: '+str(saveIndex))

menu(saveValue)
    
    


