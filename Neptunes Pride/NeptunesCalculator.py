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
        level = tryInput("Tech Level: ")
        manu(industry, level)
        
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
        match (bless):
            case 0: blessing = None
            case 1: blessing = True
            case 2: blessing = False
            case _: blessing = None
        
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
            match(menuInput):
                case 0:
                    manuInput()
                case 1:
                    researchInput()
        except:
            print("\nEscaping inner function. Returning to menu.")
        
            

def manu(industry, TechLevel):
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    
    printString = f"""
Per Production Cycle: {total}
Per Hour Tick:        {perTick:.2f}
"""
    print(printString)

def simplifyHours(hours):
    hrStr = "Hour"
    if(hours>24):
        days = hours//24
        dayStr = "Day"
        if days > 1:
            dayStr = "Days"
            
        hrs = hours%24
        if hrs > 1:
            hrStr = "Hours"
            
        return f"{days} {dayStr} {hrs} {hrStr}"
    else:
        if hours > 1:
            hrStr = "Hours"
        return f"{hours} {hrStr}"
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
    match blessing:
        case None:
            CostRate = 144
        case True:
            CostRate = 128
        case False:
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
