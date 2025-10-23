import math

def menu():
    def manuInput():
        print("Input the total manufacturing for a star, and the technology level.")
        industry = int(input("Industry: "))
        level = int(input("Tech Level: "))
        manu(industry, level)
        
    def researchInput():
        print("input the Total amount of science, current tech level, xp toward next level, Strength/weakness, and how many levels to estimate")
        
        science = int(input("Total Science: "))
        curLevel = int(input("Current Tech Level: "))
        curExp = int(input("Current Exp toward next level: "))
        
        print("""Blessings (aka, Strengths/Weaknesses)
              [0] - No bonuses
              [1] - Strength (it's cheaper to research this)
              [2] - Weakness (it cost more to research this)""")
        bless = int(input("Blessing: "))
        match (bless):
            case 0: blessing = None
            case 1: blessing = True
            case 2: blessing = False
            case _: blessing = None
        
        planLevel = int(input("How many levels to plan for? "))
        if planLevel == None:
            planLevel = 1
        
        planResearch(science, curLevel, curExp, blessing, planLevel)
    
    while True:
        print(f"""
              Do a calculation
              
              [0] Manufacturing
              [1] Research
              """)
        
        menuInput = int(input("Menu Option: "))
        
        match(menuInput):
            case 0:
                manuInput()
            case 1:
                researchInput()

def manu(industry, TechLevel):
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    
    printString = f"""
Per Production Cycle: {total}
Per Hour Tick:        {perTick:.2f}
"""
    print(printString)


def planResearch(TotalScience,CurrentLevel,CurrentExp,Blessing,Levels=3):
    totalHours = 0
    loopExp = CurrentExp
    for level in range (Levels):
        if(level > 0):
            loopExp = 0
        loopLevel = level+CurrentLevel
        hoursThisLevel = researchTime(TotalScience, loopLevel, loopExp, Blessing, False)
        totalHours += hoursThisLevel
        print(f"Level {loopLevel+1}:\t{totalHours} Hours")

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
