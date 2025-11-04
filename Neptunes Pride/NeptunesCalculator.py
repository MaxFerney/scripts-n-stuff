import math

def tryInput(message="", ValType=int):
    while True:
        try:
            return ValType(input(message))
        except ValueError:
            print("Invalid type. Please try again.")

def menu():
    keepRunningMenu = True
    def manuInput():
        print("Input the total manufacturing for a star, and the technology level.")
        industry = tryInput("Industry: ")
        level = tryInput("Manufacturing Level: ")
        currentShips = tryInput("Current Ships: ")
        if currentShips == None:
            currentShips = 0
        planLevel = tryInput("How many days to plan for? ")
        if planLevel == None:
            planLevel = 1
        manu(industry, level, currentShips, planLevel)
        
    def researchInput():
        print("input the Total amount of science, current tech level, xp toward next level, Strength/weakness, and how many levels to estimate")
        
        science = tryInput("Total Science: ")
        curLevel = tryInput("Current Tech Level: ")
        curExp = tryInput("Current Exp toward next level: ")
        
        print("""Blessings (aka, Strengths/Weaknesses)
              [0] - No bonuses
              [1] - Strength (it's cheaper to research this)
              [2] - Weakness (it cost more to research this)""")
        bless = tryInput("Blessing: ")
        if bless ==  0: blessing = None
        elif bless ==  1: blessing = True
        elif bless ==  2: blessing = False
        else: blessing = None
        
        planLevel = tryInput("How many levels to plan for? ")
        if planLevel == None:
            planLevel = 1
        
        planResearch(science, curLevel, curExp, blessing, planLevel)
    
    while keepRunningMenu == True:
        print(f"""
              Select a menu option.
              
              [0] Manufacturing
              [1] Research
              """)
        
        try:
            menuInput = tryInput("Menu Option: ")
        except KeyboardInterrupt:
            print("Leaving the main function.")
            keepRunningMenu = False
            return
        try:
            if menuInput ==  0:
                manuInput()
            if menuInput ==  1:
                researchInput()
        except:
            print("\nEscaping inner function. Returning to menu.")
        
            


def manu(industry, TechLevel, currentShips=0, planLevel=10):
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    EstimatedShips = total*planLevel+currentShips
    
    printString = f"""
Ships Per Production Cycle: \t{total}
Ships Per Hour Tick:        \t{perTick:.2f}
Current Ships:              \t{currentShips}
Ships in {planLevel} days:        \t{EstimatedShips}

"""
    print(printString)

def simplifyHours(hours):
    # Days
    days = 0
    if(hours>=24):
        days = hours//24
    finalDaysStr = '' #0 days
    dayStr = "Day"
    if days > 1:
        dayStr = "Days"
    if(days > 0):
        finalDaysStr = f"{days} {dayStr} " # 1 day (s)
    
    # Hours
    hrs = hours%24
    finalHourStr = '' #0 hours
    hrStr = "Hour"
    if hrs > 1:
        hrStr = "Hours"
    if(hrs > 0): 
        finalHourStr = f"{hrs} {hrStr}" # 1 hour (s)
    
    # Edge case formatting
    if days == 1 and hrs == 0:
        return "1 Day    "
    
    # String Return
    return f"{finalDaysStr}{finalHourStr}"

def planResearch(TotalScience,CurrentLevel,CurrentExp,Blessing,Levels=3):
    totalHours = 0
    loopExp = CurrentExp
    print("_"*55)
    print("| Level | \t| Hours This Level | \t| Total Hours |")
    for level in range (Levels):
        if(level > 0):
            loopExp = 0
        loopLevel = level+CurrentLevel
        hoursThisLevel = researchTime(TotalScience, loopLevel, loopExp, Blessing, False)
        totalHours += hoursThisLevel
        print(f"Level {loopLevel+1}:\t{simplifyHours(hoursThisLevel)} \t\t| {simplifyHours(totalHours)}")
    print("_"*55)

def researchTime(TotalScience, \
                 CurrentLevel, \
                 CurrentExp ,\
                 blessing=None,\
                 PrintStr=True):
    CostRate = 144

    if blessing ==  None:
        CostRate = 144
    if blessing ==  True:
        CostRate = 128
    if blessing ==  False:
        CostRate = 160

    CurrentCost = CostRate*CurrentLevel
    RemainingResearch = CurrentCost - CurrentExp
    
    exactHours = RemainingResearch / TotalScience
    EstimatedHours = math.floor(exactHours)

    
    if(PrintStr):
        OutputString = f"""
Time until Next Research: {EstimatedHours} Hours

Level {CurrentLevel+1}:\t{EstimatedHours}
Level {CurrentLevel+2}:\t{EstimatedHours+researchTime(TotalScience,CurrentLevel+1, 0,blessing, False)}
Level {CurrentLevel+3}:\t{EstimatedHours+researchTime(TotalScience,CurrentLevel+1, 0,blessing, False)+researchTime(TotalScience,CurrentLevel+2, 0,blessing, False)}
"""
        print(OutputString)
    return EstimatedHours

menu()
