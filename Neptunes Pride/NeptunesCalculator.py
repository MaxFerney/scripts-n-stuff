#region imports
import math
import requests #`pip install requests`. make sure you select the correct interpreter.
import json
import configparser
#endregion imports

#TODO: look into investment costs on planets:
#https://www.reddit.com/r/neptunespride/comments/2h8i5x/does_anyone_know_where_to_find_the_equations_for/

global debug, Players, GAMEID, APIKEY, SELF_PLAYER

#region -- API Connection Setup --
config = configparser.ConfigParser()
config.read('Neptunes Pride/GameConfig.ini')
GAMEID = config.get('CONNECTION', 'GameId')
APIKEY = config.get('CONNECTION', 'ApiKey')
#endregion -- API Connection Setup --

#region -- Class Definitions --
# Stores player stats to cut down on number of inputs.
class Player:
    PlayerName:str = "Player Name"
    PlayerId:int = 0
    Banking = 1
    Experimentation = 1
    Manufacturing = 1
    Range = 1
    Weapons = 1
    Terraforming = 1
    RaceInfo = [0, 0]
    RawResearchInfo:object = None
    
    TotalStars = 1
    TotalFleets = 1
    
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
                 TotalSci=1,
                 totalFleets=1,
                 totalStars=1,
                 terra=1,
                 playerId=0,
                 raceInfo=[0, 0],
                 rawResearchInfo=None):
        self.PlayerName = name
        self.Banking = bank
        self.Experimentation = exp
        self.Manufacturing = manu
        self.Range = range
        self.Weapons = weap
        self.TotalEconomy = TotalEco
        self.TotalIndustry = TotalInd
        self.TotalScience = TotalSci
        self.TotalStars = totalStars
        self.TotalFleets = totalFleets
        self.Terraforming = terra
        self.PlayerId = playerId
        self.RaceInfo = raceInfo
        self.RawResearchInfo = rawResearchInfo
    
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
    
    def GetTechInfo(self, techIdentifier:int):
        selectedTech = self.RawResearchInfo[str(techIdentifier)] # pyright: ignore[reportIndexIssue]
        return selectedTech
    
    def __str__(self):
        return f"""
    ====================================
    Player Overview: [{self.PlayerName}] [ID: {self.PlayerId}]
    
    Banking:            {self.Banking}
    Experimentation:    {self.Experimentation}
    Manufacturing:      {self.Manufacturing}
    Range:              {self.Range}
    Weapons:            {self.Weapons}
    Terraforming:       {self.Terraforming}
    
    Total Economy:      {self.TotalEconomy}
    Total Industry:     {self.TotalIndustry}
    Total Science:      {self.TotalScience}
    
    Total Stars:        {self.TotalStars}
    Total Fleets:       {self.TotalFleets}
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
        perTick:float = float(manu(self.planetIndustry, Manu, 0, 0, None, True))
        # Defender Ships at Arrival
        actualShipsPerTick = perTick*self.timeToArrive
        roundedShipsPerTick = math.ceil(actualShipsPerTick)
        shipsAtArrival = self.planetShips + roundedShipsPerTick
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

#region -- Data Loading --
def fetchData(api):
    return json.loads(requests.get(api).text)

def loadPlayers(inputData):
    global SELF_PLAYER
    playerArray = inputData['scanning_data']['players']
    outputArray = []
    numPlayers = inputData['scanning_data']['config']['players']
    Self_player_id = inputData['scanning_data']['playerUid']
    for playerNum in range(1,numPlayers+1):
        playerInfo = playerArray[str(playerNum)]
        
        # print(playerInfo['race'])
        player = Player (
            name=playerInfo['alias'],
            TotalEco=playerInfo['totalEconomy'],
            TotalInd=playerInfo['totalIndustry'],
            TotalSci=playerInfo['totalScience'],
            totalFleets=playerInfo['totalFleets'],
            totalStars=playerInfo['totalStars'],
            bank=playerInfo['tech']['0']['level'],
            exp=playerInfo['tech']['1']['level'],
            manu=playerInfo['tech']['2']['level'],
            range=playerInfo['tech']['3']['level'],
            weap=playerInfo['tech']['5']['level'],
            terra=playerInfo['tech']['6']['level'],
            playerId=playerInfo['uid'],
            raceInfo=playerInfo['race'],
            rawResearchInfo=playerInfo['tech']
        )
        if playerInfo['uid'] == Self_player_id: #or playerInfo['uid'] == 3 or playerInfo['uid'] == 4:
            SELF_PLAYER = player
            print("------ SELF INFORMATION ------")
            print(json.dumps(playerInfo, indent=4))
            # print(SELF_PLAYER)
        outputArray.append(player)
        
    return outputArray

ApiString = f'https://np.ironhelmet.com/api?game_number={GAMEID}&code={APIKEY}'
mainData = fetchData(ApiString)
# print(json.dumps(mainData, indent=4))

# API mapping for research indexes
RESEARCH_INDEXES={ #0, 0 is no blessing
    0:'Banking', #4, cheap banking. 11 costly banking.
    1:'Experimentation', #6, cheap exp. 13 costly exp.
    2:'Manufacturing', #5, cheap manu. 12 costly manu.
    3:'Range', #2, cheap range. 9, costly range.
    # 4:'Scanning', #3, cheap scanning. 10, costly scanning.
    5:'Weapons', #1, cheap weap. 8, costly weap.
    6:'Terraforming', #7: cheap terra. 14: costly terra. 
}

RESEARCH_TUPLES = [
    ('Banking', 0, 4, 11),
    ('Experimentation', 1, 6, 13),
    ('Manufacturing', 2, 5, 12),
    ('Range', 3, 2, 9),
    # ('Scanning', 4, 3, 10),
    ('Weapons', 5, 1, 8),
    ('Terraforming', 6, 7, 14)
]
#endregion -- Data Loading --

#region -- Global Definitions --
# Global Definitions
debug = False
# Players = [
#     Player("Dovah Kro",
#            33,22,52,23,39,
#            1828,1423,607),
#     Player("HelloLuke",
#            23,18,24,16,34,
#            1224,975,226),
#     Player("Homeless man",
#            23,19,25,15,24,
#            1224,975,226),
#     Player("AlbertMungus",
#            39,22,51,19,36,
#            603,982,255),
#     Player("Earthworm Jim",
#            35,23,51,19,36,
#            3551,2564,513)
# ]

Players = loadPlayers(mainData)

#endregion -- Global Definitions --

#region -- MENU --


def menu():
    global ATTACKER, DEFENDER
    #region ---- Initial Display ----
    keepRunningMenu = True
    ATTACKER = SELF_PLAYER
    # print("#"*20)
    # print(f"Attacker: {ATTACKER.PlayerName}")
    # DEFENDER = None
    # # print(f"Defender: {DEFENDER.PlayerName}")
    # print("#"*20)
    #endregion ---- Initial Display ----
    
    #region ---- input functions ----
    #region -- List Players --
    def ListPlayers():
        getPlayers()
    #endregion -- List Players --
    
    #region -- Refresh Data --
    def refreshData():
        global Players
        mainData = fetchData(ApiString)
        Players = loadPlayers(mainData)
        print("Data Refreshed!")
    #endregion -- Refresh Data --
    
    #region -- Manu Input --
    def manuInput():
        print("Input the total manufacturing for a star, and the technology level.")
        params = [
            InputParameter("Total Industry: "), #Industry
            InputParameter("Manufacturing Level: "), #Manu
            InputParameter("Current Ships: ", int, 0), #Ships
            InputParameter("How many hours to plan for? ", int, 1) #Hours
        ]
        
        for p in params:
            p.tryInput()
        manu(paramArray=params)
    #endregion -- Manu Input --
    
    #region -- Research Input --
    def researchInput():
        print("Player selection or manual input?")
        playerSelection = InputParameter("Player Section? ([y]/n)", str, 'y').tryInput()
        
        if playerSelection == 'y':
            
            # Select Player
            print("\nPlayers [Index]: Name")
            for p in Players:
                isSelfPlayer = p.PlayerId == SELF_PLAYER.PlayerId
                print(f"[{Players.index(p)}]: {p.PlayerName} { '(You)' if isSelfPlayer else '' }")
            playerIndex = InputParameter("\nSelect Player by Index: ", int).tryInput()
            SelectedPlayer = Players[playerIndex]
            
            # Select Research Type
            print("\nResearch Types [Index] | Type Name")
            for r in RESEARCH_TUPLES:
                print(f"[{RESEARCH_TUPLES.index(r)}] | {r[0]}")
            researchIndex = InputParameter("\nSelect Research Type by Index: ", int).tryInput()
            selectedResearch = RESEARCH_TUPLES[researchIndex]
            
            # {'kind': 3, 'level': 1, 'research': 121, 'cost': 144}
            PlayerResearchInfo = SelectedPlayer.GetTechInfo(selectedResearch[1])
            PlayerTotalScience = SelectedPlayer.TotalScience            
            currentResearchLevel = PlayerResearchInfo['level']
            
            # Current research experience - if not found nor input, default to 0.
            try:
                currentResearchExp = PlayerResearchInfo['research']
            except KeyError:
                currentResearchExp = InputParameter("Current Exp toward next level: ", int, 0).tryInput()
            
            # Blessing Logic            
            if SelectedPlayer.RaceInfo[0] == selectedResearch[2]: # if the player's blessing matches the research type
                blessing = 1 # strength
            elif SelectedPlayer.RaceInfo[1] == selectedResearch[3]: # if the player's weakness matches the research type
                blessing = 2 # weakness
            else:
                blessing = 0 # no blessing
            
            plannedLevels = InputParameter("How many levels to plan for? ", int, 1).tryInput()
            
            params = [
                InputParameter('', int, PlayerTotalScience),
                InputParameter('', int, currentResearchLevel),
                InputParameter('', int, currentResearchExp),
                InputParameter('', int, blessing),
                InputParameter('', int, plannedLevels)
            ]
            
            planResearch(params)
        else: 
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
    #endregion -- Research Input --
    
    #region -- Combat Input --
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
    #endregion -- Combat Input --
    
    #region -- Combat With Distance Input --
    def combatWithDistance():
        pSet = False
        # Input
        if DEFENDER != None and ATTACKER != None:
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
            manuLevel = DEFENDER.Manufacturing # pyright: ignore[reportOptionalMemberAccess]
            weapLevel = DEFENDER.Weapons # pyright: ignore[reportOptionalMemberAccess]
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
    #endregion -- Combat With Distance Input --
    
    #region -- Role Input --
    def roleInput():
        global ATTACKER, DEFENDER
        getPlayers()
        print("Players [Index] | Player Name")
        for index, p in enumerate(Players):
            print(f"[{index}] | {p.PlayerName}")
        ATTACKER = getPlayer(Index=InputParameter("Attacker | Player Index: ", int).tryInput())
        DEFENDER = getPlayer(Index=InputParameter("Defender | Player Index: ", int).tryInput())
        
        print(f"Attacker: {ATTACKER.PlayerName} | Defender: {DEFENDER.PlayerName}")
        print(ATTACKER)
        print(DEFENDER)
    #endregion -- Role Input --
    
    #region -- Ships To Attack Input --
    def shipsToAttackInput():
        defShip = InputParameter("Defender's Total Ships: ").tryInput() 
        defWeap = InputParameter("Defender's Weapons Level: ").tryInput() 
        atkWeap = InputParameter("Attacker's Weapons Level: ").tryInput()
        
        shipsToWin(defShip,defWeap,atkWeap)
    #endregion -- Ships To Attack Input --
    
    #region -- Attack Planner --
    def attackPlanner():
        if DEFENDER == None and ATTACKER == None:
            print("Please set Attacker and Defender roles in the [5] Role Input menu before using the Attack Planner.")
            return
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
    #endregion -- Attack Planner --
    
    #endregion ---- input functions ----
    
    #region ---- menu loop ----
    while keepRunningMenu == True:
        print(f"""
--------------{20*'-'}
              Select a menu option.
              
              [r] Refetch Data from API
              [0] Manufacturing
              [1] Research
              [2] Basic Combat Calculator
              [3] Distance Based Combat Calculator
              [4] List Players
              [5] Role Input (attacker and defender)
              [6] Ships To Conquer
              [7] Attack Planner
              WIP - How many ships needed to conquer
              """)
        
        try:
            menuInput = tryInput("Menu Option: ", str) # pyright: ignore[reportArgumentType]
        except KeyboardInterrupt:
            print("Leaving the main function.")
            keepRunningMenu = False
            return
        try:
            if menuInput ==  'r':
                refreshData()
            if menuInput ==  '0':
                manuInput()
            if menuInput ==  '1':
                researchInput()
            if menuInput ==  '2':
                combatInput()
            if menuInput ==  '3':
                combatWithDistance()
            if menuInput ==  '4':
                ListPlayers()
            if menuInput ==  '5':
                roleInput()
            if menuInput ==  '6':
                shipsToAttackInput()
            if menuInput ==  '7':
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


def getPlayer(playerName=None, Index=None) -> Player:
    """Retrieves the player object from the game state.
    
    Returns:
        Player: The active player instance, or None if no player is initialized.
    
    Raises:
        NotImplementedError: If player data is corrupted.
    """
    if playerName != None:
        for p in Players:
            if p.PlayerName.lower() == playerName.lower():
                return p
    if Index != None:
        return Players[Index]
    else:
        raise NotImplementedError("No valid input provided for player retrieval.")

def tryInput(message="", ValType=int):
    """Attempts to get a valid input of a specified type from the user. Repeats until a valid input is received.

    Args:
        message (str, optional): Message for the input. Defaults to "".
        ValType (_type_, optional): Type of the input value. Defaults to int.

    Returns:
        _type_: The input value of the specified type (ValType).
    """
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

def manu(industry:int=0, TechLevel:int=0, currentShips:int=0, planLevel:int=0, paramArray=None, returnPerTick=False)->float:
    """
    Manufacturing Calculator. Estimates ship production based on industry, manufacturing level, and time. 
    Can also return just the per tick production for use in other calculations.
    """
    
    if(paramArray != None):
        
        industry = paramArray[0].inputValue
        TechLevel = paramArray[1].inputValue
        currentShips = paramArray[2].inputValue
        planLevel = paramArray[3].inputValue
    
    total = industry * (TechLevel+4)
    perTick = (total / 24)
    EstimatedShips = perTick*planLevel+currentShips
    
    if not returnPerTick:
        print(f"Today : \t{currentShips} Ships")
        for timeSpan in range(1,planLevel+1):
            shipPerLevel = perTick*(timeSpan) + currentShips
            levelStr = f"{simplifyHours(timeSpan)}: \t{shipPerLevel:.2f} Ships"
            print(levelStr)
        
        
        printString = f"""
    Ships Per Production Cycle: \t{total}
    Ships Per Hour Tick:        \t{perTick:.2f}
    Current Ships:              \t{currentShips}
    Ships in {planLevel} hours:        \t\t{EstimatedShips:.2f}
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
