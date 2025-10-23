import math

def manu(industry, TechLevel):
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    
    printString = f"""
Per Production Cycle: {total}
Per Hour Tick:        {perTick:.2f}
"""
    print(printString)


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
        
##        for level in range(1,4):
##            lvl = CurrentLevel+1+level
##            hrs = EstimatedHours+\
##                  researchTime(TotalScience\
##                               ,CurrentLevel+level\
##                               , 0\
##                               ,blessing\
##                               , False)
##            
##        
##        
##            print('\n\n')
##            print(f"Level {lvl}:\t{hrs}")
    return EstimatedHours
