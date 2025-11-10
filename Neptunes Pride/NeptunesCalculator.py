import math

global debug

debug = False
# Todo: Input Enemy Stats. I wanna save luke's stats to a session. then cut down on questions.

def basicCombat(atkShips=0, atkWeap=0, defShips=0, defWeap=0, paramArray=None):
    # Input Translation
    if paramArray != None:
        atkShips = paramArray[0].inputValue
        atkWeap = paramArray[1].inputValue
        defShips = paramArray[2].inputValue
        defWeap = paramArray[3].inputValue
    
    # Defender Bonus
    defWeap = defWeap+1 

    # Create Entities
    attacker = CombatEntity(atkShips, atkWeap, "Attacker")
    defender = CombatEntity(defShips, defWeap, "Defender")
    
    if(debug):
        print("Attacker")
        print(attacker)
        print("Defender")
        print(defender)
    
    # Combat Loop
    while defender.isAlive() and attacker.isAlive():
        if defender.isAlive():
            attacker.takeHit(defender.doAttack())
            if debug: print(f'DEBUG | Attacker Ships Remaining: {attacker.ships:.2f}')
        if attacker.isAlive():
            defender.takeHit(attacker.doAttack())
            if debug: print(f'DEBUG | Defender Ships Remaining: {defender.ships:.2f}')
        else:
            defender.winString()
            break
            # print(f'\nDefender wins with {defender.ships:.2f} ships remaining!')
        if not defender.isAlive():
            attacker.winString()
            break
            # print(f'\nAttacker wins with {attacker.ships:.2f} ships remaining!')

# Stores player stats to cut down on number of inputs.
class Player:
    pass

class CombatEntity:
    ships = 0
    weapons = 1
    title = "Default Title"
    
    def __init__(self, Ships, WeaponLevel, Title):
        self.ships = Ships
        self.weapons = WeaponLevel
        self.title = Title
        
    def doAttack(self):
        if(self.ships > 0):
            return self.weapons
        else:
            return 0
    
    def winString(self):
        print(f'\n{self.title} wins with {self.ships:.2f} ships remaining!')
    
    def takeHit(self, damage):
        self.ships = self.ships-damage
        if self.ships < 0:
            self.ships = 0
        return self.ships
    
    def isAlive(self):
        if self.ships > 0:
            return True
        return False
    
    def __str__(self):
        return f"""
## Combat Entity <{self.title}> ##
{self.ships} Ships
{self.weapons} Weapons
######################{len(self.title)*'#'}
"""


class InputParameter:
    inputMessage = "Default Input: "
    # If passed in on creation - will handle NoneType input, and use said default.    
    inputValue = None
    inputType = int
    
    def __init__(self, message, type=int, defaultValue=None):
        self.inputMessage = message
        self.inputType = type
        self.inputValue = defaultValue
        
        # self.tryInput()
    
    def tryInput(this, message=None, ValType=None):
        if message == None:
            message = this.inputMessage
        if ValType == None:
            ValType = this.inputType
        
        while True:
            try:
                val = ValType(input(message))
                # If none, use default
                if val == None:
                    if debug: print(f"DEBUG | using default: {this.inputValue}")
                    val = this.inputValue
                # Set this.inputValue to the latest input
                this.inputValue = val
                return val
            except ValueError:
                print("Invalid type. Please try again.")
                
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
        params = [
            InputParameter("Total Industry: "), #Industry
            InputParameter("Manufacturing Level: "), #Manu
            InputParameter("Current Ships: ", int, 0), #Ships
            InputParameter("How many days to plan for? ", int, 1) #Days
        ]
        
        for p in params:
            p.tryInput()
        manu(paramArray=params)
        
    def researchInput():
        print("input the Total amount of science, current tech level, xp toward next level, Strength/weakness, and how many levels to estimate")
        
        params = [
            InputParameter("Total Science: "), #Science
            InputParameter("Current Tech Level: "), #Research
            InputParameter("Current Exp toward next level: ", int, 0), #Experience Points
            InputParameter("""
            Blessings (aka, Strengths/Weaknesses)
              [0] - No bonuses
              [1] - Strength (it's cheaper to research this)
              [2] - Weakness (it cost more to research this)
Blessing: """, int, 0), #Racial Trait
            InputParameter("How many levels to plan for? ", int, 1)
        ]
        for p in params:
            p.tryInput()
        planResearch(params)
        
    def combatInput():
        print('Standard combat')
        params = [
            InputParameter("Attacker Ships: "),
            InputParameter("Attacker Weapons: "),
            InputParameter("Defender Ships: "),
            InputParameter("Defender Weapons: ")
        ]
        for p in params:
            p.tryInput()
        basicCombat(paramArray=params)
        
    def combatWithDistance():
        # Input
        print("Calculate how many ships will be built by the time of arrival.")
        ticks = InputParameter("How many hours till arrival: ").tryInput()
        industry = InputParameter("Star's Total Industry: ").tryInput()
        manuLevel = InputParameter("Star's Manufacturing Level: ").tryInput()
        weapLevel = InputParameter("Star's Weapons Level: ").tryInput()
        starShips = InputParameter("Star's Current Ships: ").tryInput()
        # Calculate Combat Too?
        
        print(15*'-')
        AttackerShips = InputParameter("Attacker Ships: ").tryInput()
        AttackerWeaps = InputParameter("Attacker Weapons: ").tryInput()
        
        # Calculation
        perTick = manu(industry, manuLevel, 0, 0, None, True)
        # Defender Ships at Arrival
        shipsAtArrival = starShips + (perTick*ticks)
        
        # Display
        print(f"""
            Hours Till Arrival:         {ticks} Hours
            Defender Ships At Arrival:  {shipsAtArrival:.2f} Ships [W{weapLevel}]
""")
        
        print(
f"""Attacker Ships At Arrival:  {AttackerShips:.2f} Ships [W{AttackerWeaps}]
""")
        print(30*'-')
        basicCombat(AttackerShips, AttackerWeaps, shipsAtArrival, weapLevel)
        
        
    
    while keepRunningMenu == True:
        print(f"""
--------------{20*'-'}
              Select a menu option.
              
              [0] Manufacturing
              [1] Research
              [2] Basic Combat Calculator
              [3] Distance Based Combat Calculator
              WIP - How many ships needed to conquer
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
            if menuInput ==  2:
                combatInput()
            if menuInput ==  3:
                combatWithDistance()
        except KeyboardInterrupt:
            print("\nEscaping inner function. Returning to menu.")
        
            


def manu(industry=None, 
         TechLevel=None, 
         currentShips=None, 
         planLevel=None, 
         paramArray=None, 
         returnPerTick=False):
    if(paramArray != None):
        
        industry = paramArray[0].inputValue
        TechLevel = paramArray[1].inputValue
        currentShips = paramArray[2].inputValue
        planLevel = paramArray[3].inputValue
    
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    EstimatedShips = total*planLevel+currentShips
    
    if not returnPerTick:
        print(f"Today : \t{currentShips} Ships")
        for level in range(1,planLevel+1):
            shipPerLevel = total*(level) + currentShips
            levelStr = f"{simplifyDays(level)}: \t{shipPerLevel} Ships"
            print(levelStr)
        
        
        printString = f"""
    Ships Per Production Cycle: \t{total}
    Ships Per Hour Tick:        \t{perTick:.2f}
    Current Ships:              \t{currentShips}
    Ships in {planLevel} days:        \t{EstimatedShips}
    """
        print(printString)
    if returnPerTick:
        return perTick 

def planResearch(paramArray):
    TotalScience = paramArray[0].inputValue
    CurrentLevel = paramArray[1].inputValue
    CurrentExp = paramArray[2].inputValue
    bless = paramArray[3].inputValue
    Levels = paramArray[4].inputValue
    
    if bless ==  0: Blessing = None
    elif bless ==  1: Blessing = True
    elif bless ==  2: Blessing = False
    else: Blessing = None
    
    
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
        print(f"Level {loopLevel+1}:\t{simplifyHours(hoursThisLevel, True)} \t\t| {simplifyHours(totalHours, True)}")
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

#region --- Formatting Functions ---
def simplifyHours(hours, dayFormatting=False):
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
        if(dayFormatting):
            return "1 Day    "
        else:
            return "1 Day  "
    
    # String Return
    return f"{finalDaysStr}{finalHourStr}"

def simplifyDays(days):
    hours = days*24
    return simplifyHours(hours)
#endregion --- Formatting Functions ---
menu()
