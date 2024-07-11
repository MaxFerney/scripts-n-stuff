from enum import Enum
print('''
usage: `FindNum(goal)`

gets numbers near another number via functions and small numbers.

setDivs()
calculates all divisors between 2 and self.goal//2

setExp()
calculates all exponents leading to self.goal//2

setAdd()
calculates all(up to 50) adds leading to self.goal-1

''')
#region input handler
def inputWithErrorChecking(prompt:str, iType:type=int, validatorCallback=None):
    """While true loop for input handling. iType is expected string and validator is a bool function expecting the user input

    Args:
        prompt (str): string prompt to be displayed to the user
        iType (type, optional): type expected for the input value. Defaults to int.
        validatorCallback (function, optional): Validator for handling values that **returns a boolean for if it passes or fails**. uses a singular input of _iType_. Defaults to None.

    Returns:
        iType: the input provided by the user. If a validator callback is used, it will return None if it fails. 
    """
    
    while True:
        try:
            # Get user Input
            rawInput = input(prompt)
            print('raw '+rawInput)
            userInput = iType(rawInput)
        except(TypeError): #it doesnt hit this lol - not anymore
            print(f'Type Error. Expected [{iType.__name__}] | Received [{type(rawInput).__name__}] Please try again.')
            continue
        except(ValueError):
            print(f'Value error. Expected [{iType.__name__}] | Received [{type(rawInput).__name__}] Please try again.')
            continue
        
        try:
            # Without Validator
            if(validatorCallback is None):
                return userInput
            # Validator Handling
            else:
                if(validatorCallback(userInput)):
                    return userInput
                else:
                    print(f'Validator failed. Please try again.')
                    continue
        except(TypeError): #it doesnt hit this lol - not anymore
            print(f'VALIDATION Type Error. Expected [{iType.__name__}] | Received [{type(rawInput).__name__}] Please try again.')
            continue

    return userInput
#endregion
#region Recursors

def testNumberUsefullness(number:int=11172, passDist=None):
    # print(f'goal: {number}')
    #((7*14)*((2^7)-14))=11172
    
    numObj=FindNum(number)
    
    def doSetFunction(functionName):
        value=functionName(True, passDist)
        if(value == numObj.goal):
            value = 0
        # print(f'{functionName.__name__} : {value}')
        return value
    
    
    divVal = doSetFunction(numObj.setDivs)
    expVal = doSetFunction(numObj.setExp)
    return (divVal, expVal)


def findBestNumberOfArray(numArray: list[int], dictRef= dict[int,int]):
    if(len(numArray)>0):
        bestDiv, bestExp = testNumberUsefullness(numArray[0])
    else:
        bestDiv = bestExp = (0,'default')
    for dist,num in dictRef.items():
        (div,exp) = testNumberUsefullness(num, dist)
        if(bestDiv[0]==0 or div[0]<=bestDiv[0]):
            bestDiv = div
        if(bestExp[0]==0 or exp[0]<=bestExp[0]):
            bestExp = exp
    dictRef.values
#     print(f"""
# Best Divide:
#     Equation: {bestDiv[1]}
# Best Exponent:
#     Equation: {bestExp[1]}
# """)
    return (bestDiv, bestExp)

#endregion recursors
    

def findAndReplaceInString(number:int):
    #total open parens before = nest level. 1 = 0, 2 = 1, 0 is unlocked
    #((7*14)*((2^7)-14))=11172
    #(98*114)=11172 #locked, nest 0
    searchString = '((7*14)*((2^7)-14))=11172'
    

class diveT(Enum):
    base=1
    divide=2
    exponent=3
    add=4

global SavedNums

class FindNum:
    #region Variables
    goal = 0
    divs = {}
    divRange = 0
    exponents = {}
    expRange = 0
    adds = {}
    addRange=30
    diveList = []
    diveType = diveT.base
    expDistance = None
    diveMessage = 'note when splitting number up'
    equationPart = None #f'[6]*9 = 54'
    shorthandEquation = None #'6*9'
    locked = False
    # [2, [2, 5], [7, 2, 1]]
    #endregion
    
    #region class definition
    def __init__(self, 
                 goal, 
                 equationPart='[6]*9 = 54',
                 systemArgs: tuple[diveT,int]=None):
        self.goal = int(goal)
        self.equationPart = equationPart
        self.shorthandEquation = str(goal)

        self.setDivs()
        self.setExp()
        self.setAdds()
        
        if(systemArgs is not None):
            match(systemArgs[0]):
                case diveT.divide:
                    self.selectDiv(systemArgs[1])
                case diveT.exponent:
                    self.selectExp(systemArgs[1])


    def __str__(self):
        # # not yet implemented
        # self.getDivs()
        # self.getExp(2000)
        return str(self.goal)
    #endregion
    
    #region Utility Functions
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
        elif(self.diveType==diveT.add):
            internalString = f'({self.diveList[0].formatShorthand(nestLvl+1)}+{self.diveList[1].formatShorthand(nestLvl+1)})'
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
    #endregion

    #region Adds
    def setAdds(self):
        adds={}
        if (self.goal-1 <= self.addRange): self.addRange = self.goal-1
        for a in range(1, 50):
            subtractable = self.goal-a
            adds[a] = subtractable
        self.adds=adds
        # self.getAdds()
    
    def getAdds(self):
        # for k, v in self.adds.items():
        #     print(f'{k}+{v} = {self.goal}')
        numArray = list(self.adds.values())
        (div,exp) = findBestNumberOfArray(numArray, self.adds)
        print(f"""
Key: [{div[3]}]
    Generates: ({div[1]})+{div[3]}={self.goal}
Key: [{exp[3]}]
    Generates: ({exp[1]})+{exp[3]}={self.goal}
""")

    def selectAdd(self):
        self.printPretext()
        print('[key] + value')
        # for k, v in self.adds.items():
        #     print(f'[{k}]+{v} = {self.goal}')
        self.getAdds()
        numArray = list(self.adds.values())
        (div,exp) = findBestNumberOfArray(numArray, self.adds)

        def addErrorChecking(val:int) -> bool:
            try:
                self.adds[val]
                if( val in [div[3],exp[3]]):
                    return True
                print("Not a useful number. Try one from keys above")
                return False
            except(KeyError):
                return False
        keySelection = inputWithErrorChecking('select key: ', int, addErrorChecking)
        if(keySelection==div[3]):sysCall=(diveT.divide, div[4])
        if(keySelection==exp[3]):sysCall=(diveT.exponent, div[4])
        valueSelection = self.adds[keySelection]
        newEntry = [ 
            FindNum(keySelection,f'[{keySelection}]+{valueSelection}={self.goal}'), 
            FindNum(valueSelection, f'{keySelection}+[{valueSelection}]={self.goal}', sysCall)
        ]
        self.diveType = diveT.add
        self.setDive(newEntry, f"goal {self.goal} Added! into more")
        return newEntry
    #endregion Adds

    #region Divs
    def setDivs(self, systemCall=False, passThroughDist=None):
        """_summary_

        Args:
            systemCall (bool, optional): system call bool. Defaults to False.
            passThroughDist (int, optional): addition distance pass through, for handling sum distance. Defaults to None.

        Returns:
            _type_: _description_
        """
        divs = {}
        divRange = self.goal//2
        self.divRange = divRange
        minSum=self.goal
        smallestCombo = ''
        smallestKey=None
        for d in range(2,int(divRange)+1):
            v = self.goal/d
            if (v).is_integer():
                if(minSum >= d+v):
                    minSum = d+v
                    smallestKey=d
                    smallestCombo = f'{int(d)}*{int(v)}={self.goal}'
                divs[d] = int(v)
        
        self.divs = divs
        if(systemCall):
            return (int(minSum), smallestCombo, self.goal, passThroughDist, smallestKey)
        # self.getDivs()s
##        return divs

    def getDivs(self):
        self.printPretext('range: '+str(self.divRange))
        sum=0
        for k,v in self.divs.items():
            if(sum==k+v):
                print(f'[[{k}]*{v}]')
            else:
                sum=k+v
                print(f'[{k}]*{v}')
            
    
    def selectDiv(self, systemCallValue=None):
        if(systemCallValue is None):#User Input
            self.getDivs()
            
            def divErrorChecking(val:int) -> bool:
                try:
                    self.divs[val]
                    return True
                except(KeyError):
                    return False
            keySelection = inputWithErrorChecking('select key: ', int, divErrorChecking)
        else: #Selected via other function call
            keySelection = systemCallValue
        valueSelection = self.divs[keySelection]
        newEntry = [ 
            FindNum(keySelection,f'[{keySelection}]*{valueSelection}={self.goal}'), 
            FindNum(valueSelection, f'{keySelection}*[{valueSelection}]={self.goal}')
        ]
        self.diveType = diveT.divide
        self.setDive(newEntry, f"goal {self.goal} Divided! into more")
        return newEntry
    #endregion Divs

    #region Exponents                
    def setExp(self, systemCall=False, passThroughDist=None):
        """_summary_

        Args:
            systemCall (bool, optional): call this function via system call. Defaults to False.
            passThroughDist (int, optional): addition distance pass through, for handling sum distance. Defaults to None.

        Returns:
            _type_: _description_
        """
        exclusion = self.goal-1
        exponents = {}
        expRange = int(self.goal//2)
        self.expRange = expRange
        minSum = self.goal
        smallestCombo = ''
        smallestKey = None
        for ex in range(2, expRange+1):
            baseval = int(round(self.goal**(1./ex)))
            mult = int(round(baseval**ex,2))
            distance = int(abs(round(self.goal-mult)))
            if(distance <= exclusion and mult!=1):
                if(minSum >= baseval+ex+distance):
                    minSum = baseval+ex+distance
                    rawdistance = self.goal-mult
                    smallestKey = ex
                    if(rawdistance < 0):
                        smallestCombo = f'({baseval}^{ex})-{distance} = {self.goal}'
                    elif(rawdistance > 0):
                        smallestCombo = f'({baseval}^{ex})+{distance} = {self.goal}'
                    elif(rawdistance == 0):
                        smallestCombo = f'{baseval}^{ex} = {self.goal}'
                        
                    
                exponents[ex] = baseval

        self.exponents = exponents
        if(systemCall):
            return (int(minSum), smallestCombo, self.goal, passThroughDist, smallestKey)
        # self.getExp()
##        return exponents

    def getExp(self):
        exclusion = self.goal-1
        self.printPretext('range: '+str(self.expRange)+', exclusion: '+str(exclusion))
        for k,v in self.exponents.items():
            mult = round(v**k,2)
            distance = abs(round(self.goal-mult))
            if(distance <= exclusion and mult!=1):
                rawdistance = self.goal-mult
                redesignedString = str(v)+'^'+str(k)+' = '+str(mult)+' | '+str(distance)+' away'
                if(rawdistance < 0):
                    redesignedString = f'({v}^{k})-{distance} = {self.goal}'
                elif(rawdistance > 0):
                    redesignedString = f'({v}^{k})+{distance} = {self.goal}'
                elif(rawdistance == 0):
                    redesignedString = f'{v}^{k} = {self.goal}'
                print(redesignedString)

    def selectExp(self, systemCallValue=None):
        if(systemCallValue is None):
            self.getExp()
            def expErrorChecking(val:int) -> bool:
                try:
                    self.exponents[val]
                    return True
                except(KeyError):
                    return False
            keySelection = inputWithErrorChecking('select key: ', int, expErrorChecking)
        else:
            keySelection = systemCallValue
        value=self.exponents[keySelection]
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
    #endregion exponents
                
