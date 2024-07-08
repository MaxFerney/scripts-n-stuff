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
            if(self.expDistance==0):
                internalString = f'({self.diveList[0].formatShorthand(nestLvl+1)}^{self.diveList[1].formatShorthand(nestLvl+1)})'
            else:
                if(self.expDistance<0):
                    posNegSign = '-'
                elif(self.expDistance>0):
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
            pass
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