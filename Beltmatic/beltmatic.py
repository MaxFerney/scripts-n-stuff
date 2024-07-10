
from FindNum import FindNum, inputWithErrorChecking
from enum import Enum



mainGoal = FindNum(inputWithErrorChecking('SET FINDNUM GOAL: ', int), 'Goal/Base Number')
class MainMenu(Enum):
    setFindNum=0
    dive=1
    setDiveIndex=2
    viewAll=3
    stepOut=4
def menuString(nestLevel=0):
    if nestLevel==0:
        exitString = f'Exit APPLICATION'
    else:
        exitString = f'Exit (Go Up. Nest {nestLevel})'
    return f"""
{20*'#'}
[0] set current findNum
[1] dive (step into) current findnum
[2] set index
[3] view all
[4] {exitString}

"""
class FindNumMenu(Enum):
    selectDiv=1
    selectExp=2
    stepOut=3
    printAll=4

findNumDescription = f"""
{30*'#'}
[{FindNumMenu.selectDiv.value}] select div
[{FindNumMenu.selectExp.value}] select exp
[{FindNumMenu.stepOut.value}] exit (go back)
[{FindNumMenu.printAll.value}] print all

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

def menu(paramFindNum:FindNum, nestLevel=0, doinADive=False):
    baseFindNum = paramFindNum
    currentIndex = 0

    

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

        if(nestLevel==0):
            print(f'saving {baseFindNum.formatShorthand()} to minified...')
            global minified
            minified = baseFindNum.formatShorthand()
        
        #Input Current Level Input
        if(doinADive):
            print(" lol did a dive")
            uInput = 1
        else:
            printState()

            print(menuString(nestLevel))
            print('__________________')
            uInput = inputWithErrorChecking('input MENU option: ', int) #int(input('input MENU option: '))

        #User Input Handling
        match(uInput):
            case MainMenu.setFindNum.value : # set current findNum
                print('--Set findNum')    
                findVal = inputWithErrorChecking('set current FindNum([Input]): ', int)
                # findVal = int(input('set current FindNum(input): '))
                currentIndex = 0
                baseFindNum = FindNum(findVal, 'Overwrote Current Findnum')
            case MainMenu.dive.value: # modify findNum
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
                        uInput = inputWithErrorChecking('SUBMENU option: ', int)
                        match(uInput):
                            case FindNumMenu.selectDiv.value: # div
                                baseFindNum.selectDiv()
                                invalidInput = False
                            case FindNumMenu.selectExp.value: # exp
                                baseFindNum.selectExp()
                                invalidInput = False
                            case FindNumMenu.stepOut.value: # exit
                                print('--stepOut')
                                invalidInput = False
                                continue
                            case FindNumMenu.printAll.value: #print all
                                # print(formatStringForFindnum(baseFindNum))
                                print(baseFindNum.formatShorthand())
                                invalidInput = True
                            case _:
                                print('Input case not implemented')
                                invalidInput = True
                    
                            
                # if(not exit):
                #     menu(baseFindNum.diveList[currentIndex],nestLevel+1)

            case MainMenu.setDiveIndex.value: # change index
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
                    def diveListError(val:int)->bool:
                        
                        if(val >= 0 and val < len(baseFindNum.diveList)):
                            return True
                        print(f'[Failed Validation]: Value out of range[{0}, {len(baseFindNum.diveList)}].')
                        return False
                    currentIndex = inputWithErrorChecking('Select Index: ', int, diveListError)
                
            case MainMenu.viewAll.value: # view all
                print('--view all')
                # print(formatStringForFindnum(saveValue))
                print(baseFindNum.formatShorthand())
                print(f'Global: {minified}')
                # print(getValuesFromFindNumArray(saveValArray))
                # print(getValuesFromFindNumArray(saveValue))
            case MainMenu.stepOut.value: #exit
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

menu(saveValue,0,True)
    
    


