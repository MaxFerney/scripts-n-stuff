#region imports
import math
#endregion imports

global debug, Players

#region -- Class Definitions --

# Stores player stats to cut down on number of inputs.
class Player:
    PlayerName:str = "Player Name"
    Banking = 1
    Experimentation = 1
    Manufacturing = 1
    Range = 1
    Weapons = 1
    
    TotalEconomy = 1
    TotalScience = 1
    TotalIndustry = 1
    
    def __init__(self, name="Player Name", 
                 bank=1,
                 exp=1,
                 manu=1,
                 range=1,
                 weap=1,
                 TotalEco=1,
                 TotalInd=1,
                 TotalSci=1):
        self.PlayerName = name
        self.Banking = bank
        self.Experimentation = exp
        self.Manufacturing = manu
        self.Range = range
        self.Weapons = weap
        self.TotalEconomy = TotalEco
        self.TotalIndustry = TotalInd
        self.TotalScience = TotalSci
    
    def InputResearch(self):
        self.Banking = InputParameter("Banking Level: ", int, 1).tryInput()
        self.Experimentation = InputParameter("Experimentation Level: ", int, 1).tryInput()
        self.Manufacturing = InputParameter("Manufacturing Level: ", int, 1).tryInput()
        self.Range = InputParameter("Range Level: ", int, 1).tryInput()
        self.Weapons = InputParameter("Weapons Level: ", int, 1).tryInput()
        
    def InputTotals(self):
        self.TotalEconomy = InputParameter("Total Economy: ", int, 1).tryInput()
        self.TotalIndustry = InputParameter("Total Industry: ", int, 1).tryInput()
        self.TotalScience = InputParameter("Total Science: ", int, 1).tryInput()
    
    def InputInfo(self):
        self.PlayerName = InputParameter("PlayerName").tryInput()
    
    def __str__(self):
        return f"""
    ====================================
    Player Overview: [{self.PlayerName}]
    
    Banking:            {self.Banking}
    Experimentation:    {self.Experimentation}
    Manufacturing:      {self.Manufacturing}
    Range:              {self.Range}
    Weapons:            {self.Weapons}
    
    Total Economy:      {self.TotalEconomy}
    Total Industry:     {self.TotalIndustry}
    Total Science:      {self.TotalScience}
    ====================================
    """

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
    inputType:type = int
    
    def __init__(self, message, type:type=int, defaultValue=None):
        self.inputMessage = message
        self.inputType = type
        self.inputValue = defaultValue
        
        # self.tryInput()
    
    def tryInput(self, message=None, ValType=None):
        if message == None:
            message = self.inputMessage
        if ValType == None:
            ValType = self.inputType
        
        while True:
            try:
                val = input(message)
                # If none, use default
                if val == '':
                    #If no default, throw error
                    if (self.inputValue == None):
                        raise ValueError()
                    if debug: print(f"DEBUG | using default: {self.inputValue}")
                    val = self.inputValue
                
                else: #Run Conversion
                    val = ValType(val)
                # Set self.inputValue to the latest input
                self.inputValue = val
                return val
            except ValueError:
                print("Invalid type. Please try again.")

# for state handling in attack planner
class AttackPlanEntity:
    starName:str
    timeToArrive:int
    planetIndustry:int
    planetShips:int
    DefenderPlayer:Player
    AttackerPlayer:Player
    
    shipsAtArrival:int|None
    delayHours:int|None #NOT YET IMPLEMENTED
    minShipsToWin:int|None
    suggestedShipsToWin:int|None #calculated buffer, like +5 industry and +1 weapons on a planet.
    
    def __init__(self, StarName:str, ArrivalTime:int, Industry:int, Ships:int, defender:Player, attacker:Player):
        self.starName = StarName
        self.timeToArrive = ArrivalTime
        self.planetIndustry = Industry
        self.planetShips = Ships
        self.DefenderPlayer = defender
        self.AttackerPlayer = attacker
        
        self.shipsAtArrival = self.estimateShipsAtArrival()
        self.estimateMinShipsToWin()
        self.estimateWithMoreTech()
    
    # Estimates ships at arrival time based on manufacturing and industry.
    # Manu:int = Manufacturing level
    def estimateShipsAtArrival(self, Manu=None):
        if(Manu==None):
            Manu = self.DefenderPlayer.Manufacturing
        # Calculation
        perTick:int = int(manu(self.planetIndustry, Manu, 0, 0, None, True))
        # Defender Ships at Arrival
        shipsAtArrival = self.planetShips + (perTick*self.timeToArrive)
        return shipsAtArrival

    # Estimate minimum ships to win
    def estimateMinShipsToWin(self):
        shipsAtArrival = self.estimateShipsAtArrival()
        self.minShipsToWin = shipsToWin(shipsAtArrival, self.DefenderPlayer.Weapons, self.AttackerPlayer.Weapons, False)
    
    # Estimates minimum ships to win with defender bonus of [manu+1] and [weapons+1]
    def estimateWithMoreTech(self):
        shipsAtArrival = self.estimateShipsAtArrival(self.DefenderPlayer.Manufacturing+1)
        self.suggestedShipsToWin = shipsToWin(shipsAtArrival, self.DefenderPlayer.Weapons+1, self.AttackerPlayer.Weapons, False)

    def __str__(self):
        return f"{self.suggestedShipsToWin}\t\t{self.minShipsToWin}\t{self.timeToArrive}\t{self.shipsAtArrival}\t{self.starName}[W{self.DefenderPlayer.Weapons}]"

#endregion -- Class Definitions --

#region -- Global Definitions --
# Global Definitions
debug = False
Players = [
    Player("Dovah Kro",
           33,22,49,23,37,
           1828,1423,607),
    Player("HelloLuke",
           23,18,24,16,34,
           1224,975,226),
    Player("Homeless man",
           23,19,25,15,24,
           1224,975,226),
    Player("AlbertMungus",
           39,22,44,19,35,
           603,982,255)
]
#endregion -- Global Definitions --

#region -- MENU --

def menu():
    #region ---- Initial Display ----
    keepRunningMenu = True
    ATTACKER = Players[0]
    print("#"*20)
    print(f"Attacker: {ATTACKER.PlayerName}")
    DEFENDER = Players[3]
    print(f"Defender: {DEFENDER.PlayerName}")
    print("#"*20)
    #endregion ---- Initial Display ----
    
    #region ---- input functions ----
    def PlayerInput():
        newPlayer = Player()
        newPlayer.InputInfo()
        newPlayer.InputResearch()
        newPlayer.InputTotals()
        Players.append(newPlayer)
    
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
        pSet = False
        # Input
        UsePlayerSettings = InputParameter("Use Player Settings? ([y]/n)",str,'y').tryInput()
        if UsePlayerSettings == 'y':
            pSet = True
        print("Calculate how many ships will be built by the time of arrival.")
        ticks = InputParameter("How many hours till arrival: ").tryInput()
        industry = InputParameter("Star's Total Industry: ").tryInput()
        if(not pSet):
            manuLevel = InputParameter("Star's Manufacturing Level: ").tryInput()
            weapLevel = InputParameter("Star's Weapons Level: ").tryInput()
        else:
            manuLevel = DEFENDER.Manufacturing
            weapLevel = DEFENDER.Weapons
        starShips = InputParameter("Star's Current Ships: ").tryInput()
        # Calculate Combat Too?
        
        print(15*'-')
        # AttackerShips = InputParameter("Attacker Ships: ").tryInput()
        if(not pSet):
            AttackerWeaps = InputParameter("Attacker Weapons: ").tryInput()
        else:
            AttackerWeaps = ATTACKER.Weapons
        
        # Calculation
        perTick = manu(industry, manuLevel, 0, 0, None, True)
        # Defender Ships at Arrival
        shipsAtArrival = starShips + (perTick*ticks)
        # Attacker Ships needed to win
        shipsToConquer = shipsToWin(shipsAtArrival, weapLevel, AttackerWeaps)
        # Display
        print(f"""
            Hours Till Arrival:         {ticks} Hours
            Defender Ships At Arrival:  {shipsAtArrival:.2f} Ships [W{weapLevel}]
            Ships to Conquer (1 ship)   {shipsToConquer} Ships [W{AttackerWeaps}]
""")
        print(30*'v')
        basicCombat(shipsToConquer, AttackerWeaps, shipsAtArrival, weapLevel)
        
    def roleInput():
        global attacker, defender
        getPlayers()
        print("Players [Index] | Player Name")
        for index, p in enumerate(Players):
            print(f"[{index}] | {p.PlayerName}")
        attacker = getPlayer(Index=InputParameter("Attacker | Player Index: ", int).tryInput())
        defender = getPlayer(Index=InputParameter("Defender | Player Index: ", int).tryInput())
    
    def shipsToAttackInput():
        defShip = InputParameter("Defender's Total Ships: ").tryInput() 
        defWeap = InputParameter("Defender's Weapons Level: ").tryInput() 
        atkWeap = InputParameter("Attacker's Weapons Level: ").tryInput()
        
        shipsToWin(defShip,defWeap,atkWeap)
    
    def attackPlanner():
        print(f"""
{20*'*'}
For each attack, need Distance, Industry, and Ships.
[Uses Player Settings!]
{20*'*'}
""")
        AttacksToPlan = InputParameter("How many Attacks to coordinate? ", int, 1).tryInput()
        
        AllAttacks = []
        for a in range(AttacksToPlan):
            # Plan Inputs
            starName = InputParameter("Name of star: ", str, "Star Name").tryInput()
            ticks = InputParameter("How many hours till arrival: ").tryInput()
            industry = InputParameter("Star's Total Industry: ").tryInput()
            starShips = InputParameter("Star's Current Ships: ").tryInput()
            print()
            initialPlan = AttackPlanEntity(starName, ticks, industry, starShips, DEFENDER, ATTACKER)
            AllAttacks.append(initialPlan)
#return f"{self.suggestedShipsToWin}\t{self.minShipsToWin}\t{self.timeToArrive}\t{self.shipsAtArrival}\t{self.starName}[W{self.DefenderPlayer.Weapons}]"
        LongestAttack = None 
        print(60*"*")
        print("Tech + 1 | MinShips | ETA | AtArrival |  Star Name[Weapon]")
        for Attack in AllAttacks:
            print(Attack)
        print(60*"*")
        # get max distance from set.
        # go through each attack - modify delay to account for longest
        # run simulations based on delay
            #this can be handled within the AttackPlanEntity class
        # display grid of finalized calculations (stored in each attack entity)
            #custom function to do a 1 line print for loop display.
    #endregion ---- input functions ----
    
    #region ---- menu loop ----
    while keepRunningMenu == True:
#         print("""
# #name: ships industry hours (delay hours) shipsToSend #ROUTE
# #death sweet embrace: 912 11 20 (x) 900
# #small child: 205 7 24 (x) 350 #DEATH
# #alamo: 2735 7 16 (x) 2050.0
# #college: 4838 10 17 (x) 3600.0
# #low star: 191 2 24 (x) 200.0 #COMMUNITY
# #runecrafting: 3898 10 29 (x) 3000.0 #COMMUNITY
# #doodlebros: 650 10 29 (x) 750.0 #DEATH
# """)
        print(f"""
--------------{20*'-'}
              Select a menu option.
              
              [0] Manufacturing
              [1] Research
              [2] Basic Combat Calculator
              [3] Distance Based Combat Calculator
              [4] Player Input (WIP)
              [5] Role Input (WIP) (who is attacker or defender)
              [6] Ships To Conquer
              [7] Attack Planner
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
            if menuInput ==  4:
                PlayerInput()
            if menuInput ==  5:
                roleInput()
            if menuInput ==  6:
                shipsToAttackInput()
            if menuInput ==  7:
                attackPlanner()
        except KeyboardInterrupt:
            print("\nEscaping inner function. Returning to menu.")
    #endregion ---- menu loop ----

#endregion -- MENU --

#region -- FUNCTIONS --

#region --- Helper Functions ---
def getPlayers():
    for player in Players:
        print(player)
        
def getPlayer(playerName=None, Index=None):
    if playerName != None:
        for p in Players:
            if p.PlayerName.lower() == playerName.lower():
                return p
    if Index != None:
        return Players[Index]
    else:
        return NotImplementedError

def tryInput(message="", ValType=int):
    while True:
        try:
            return ValType(input(message))
        except ValueError:
            print("Invalid type. Please try again.")
#endregion --- Helper Functions ---

#region --- Calculation Functions ---
def basicCombat(atkShips:int=0, atkWeap:int=0, defShips:int=0, defWeap:int=0, paramArray=None, ShowCombatLogs=True):
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
            if ShowCombatLogs: defender.winString()
            return defender
            # print(f'\nDefender wins with {defender.ships:.2f} ships remaining!')
        if not defender.isAlive():
            if ShowCombatLogs: attacker.winString()
            return attacker
            # print(f'\nAttacker wins with {attacker.ships:.2f} ships remaining!')

def shipsToWin(DefShips:int, DefWeap:int, AtkWeap:int, Print=True):
    StarterAtkShips = ((DefShips * (DefWeap+1)) // AtkWeap) + (DefWeap+1) #Thanks Coret
    
    while True:
        winner = basicCombat(StarterAtkShips, AtkWeap, DefShips, DefWeap,ShowCombatLogs=False)
        if (type(winner)==CombatEntity):
            if winner.title == "Defender": #Defender Wins. Try Again.
                if Print: print(f"[{StarterAtkShips}] + {AtkWeap} = {StarterAtkShips+AtkWeap}")
                StarterAtkShips += AtkWeap
            else: # Attacker Wins. Return Ship Margin of Victory.
                if Print: print(f"It took around {StarterAtkShips} Ships to Win!")
                winMargin = basicCombat(StarterAtkShips, AtkWeap, DefShips, DefWeap,ShowCombatLogs=Print)
                if (type(winMargin)==CombatEntity):
                    SingleShipRemaining = (StarterAtkShips - winMargin.ships) + 1
            
    #         print(f"\nTherefore, the absolute minimum number of \n\
    # ships to win is [{SingleShipRemaining}] with a single ship remaining!")
            # basicCombat(SingleShipRemaining, AtkWeap, DefShips, DefWeap,ShowCombatLogs=False)
            return SingleShipRemaining #Should return Minimum number of ships

def manu(industry:int=0, TechLevel:int=0, currentShips:int=0, planLevel:int=0, paramArray=None, returnPerTick=False):
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

def researchTime(TotalScience,CurrentLevel,CurrentExp,blessing=None,PrintStr=True):
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
#endregion --- Calculation Functions ---

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

#endregion -- FUNCTIONS --

menu()
