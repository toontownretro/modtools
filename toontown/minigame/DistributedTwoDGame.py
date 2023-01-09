import random
from direct.fsm import State
from modtools.tkpanels.FSMInspector import FSMInspector


from modtools.toontown.toonbase import ModularStart
from modtools.toontown.toonbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()
base.generateLocalAvatar()
# base.startConnection()

base.localAvatar.dclass = base.cr.dclassesByName['DistributedToon']
base.cr.doId2do[1] = base.localAvatar
base.localAvatar.hp = 15
base.localAvatar.maxHp = 15
base.localAvatar.laffMeter = None


# client side init
base.cr.playGame.hood = base.cr.playGame
base.cr.playGame.hood.fsm.addState(
    State.State('minigame')
)
base.cr.playGame.hood.id = 2000
# base.ai.repo.minigameSafezoneId = 2000

from toontown.minigame import ToonBlitzGlobals
from toontown.minigame.DistributedTwoDGame import DistributedTwoDGame
DistributedTwoDGame.doId = 69
DistributedTwoDGame.hasLocalToon = 1
DistributedTwoDGame.trolleyZone = 2000
DistributedTwoDGame.numPlayers = 1
targetClient = DistributedTwoDGame(base.cr)
targetClient.setParticipants([1])
targetClient.dclass = base.cr.dclassesByName['DistributedTwoDGame']


## setting up the level ##

# sectionsSelected is a list of tuples sent from the AI. [(), ()]
# Each tuple represents one section.
# Tuple Format: (sectionIndex, [list of enemyIndices], [list of treasureIndices], [list of spawnPointIndices])
# The tuples are in the order we want made and we make sections from sectionsSelected on a one-to-one basis
sectionsSelected = list()
sectionIndexList = []


# ai code, original name: setupSections
def generateSections(szId=2000):
    """
    Make a course by selecting sections based on difficulty and probability of occurrence in that safeZone.

    :param int szId: safezone/hood id, determines difficulty
    """
    sectionWeights = ToonBlitzGlobals.SectionWeights[szId]
    numSections = ToonBlitzGlobals.NumSections[szId]
    difficultyPool = []
    difficultyList = []
    sectionsPool = ToonBlitzGlobals.SectionsPool
    sectionTypes = ToonBlitzGlobals.SectionTypes
    sectionsPoolByDifficulty = [[], [], [], [], [], []]
    sectionsSelectedByDifficulty = [[], [], [], [], [], []]
    sectionIndicesSelected = []
    for weight in sectionWeights:
        difficulty, probability = weight
        difficultyPool += [difficulty] * probability

    # Now make a list of difficulty from the difficultyPool
    for i in range(numSections):
        difficulty = random.choice(difficultyPool)
        difficultyList.append(difficulty)
    # Sort the difficultyList so that the more difficult sections appear at the end of the game
    difficultyList.sort()

    # Split SectionsPool into sectionsPoolByDifficulty
    for sectionIndex in sectionsPool:
        difficulty = sectionTypes[sectionIndex][0]
        sectionsPoolByDifficulty[difficulty] += [sectionIndex]

        # Now go through the difficutly list, and select a section from the sectionsPool with that difficulty
    # Do not repeat. If we are out of sections with that difficulty take one from the next difficulty level
    for targetDifficulty in difficultyList:
        whileCount = 0
        difficulty = targetDifficulty
        # If there is no section left to pick from that difficulty level pick one from the next difficulty level
        while not (len(sectionsPoolByDifficulty[difficulty]) > 0):
            difficulty += 1
            if (difficulty >= 5):
                difficulty = 0
                whileCount += 1
                if (whileCount > 1):
                    break
        else:
            sectionIndexChoice = random.choice(sectionsPoolByDifficulty[difficulty])
            # Adding this sectionIndex to the list of selectedSections
            sectionsSelectedByDifficulty[difficulty] += [sectionIndexChoice]
            # Removing this sectionIndex from the list of sectionsPoolByDifficulty
            sectionsPoolByDifficulty[difficulty].remove(sectionIndexChoice)

        if (whileCount > 1):
            print('We need more sections than we have choices. We have to now repeat.')

    # Fill up sectionIndicesSelected from sectionsSelectedByDifficulty to maintain 1 comprehensive list
    for i in range(len(sectionsSelectedByDifficulty)):
        for j in range(len(sectionsSelectedByDifficulty[i])):
            sectionIndicesSelected.append(sectionsSelectedByDifficulty[i][j])

    # Now go through the sectionIndicesSelected and get their properties
    for i in range(len(sectionIndicesSelected)):
        sectionIndex = sectionIndicesSelected[i]
        sectionIndexList.append(sectionIndex)
        attribs = sectionTypes[sectionIndex]
        difficulty = attribs[0]
        length = attribs[1]
        blocksPool = attribs[2]
        enemiesPool = attribs[3]
        treasuresPool = attribs[4]
        spawnPointsPool = attribs[5]
        stompersPool = attribs[6]

        # Select a random list of numEnemies enemyIndices from the enemyIndicesPool
        enemyIndicesPool = []
        enemyIndicesSelected = []
        if (enemiesPool != None):
            minEnemies, maxEnemies = attribs[7]
            for i in range(len(enemiesPool)):
                enemyIndicesPool += [i]
            numEnemies = maxEnemies * ToonBlitzGlobals.PercentMaxEnemies[szId] / 100
            numEnemies = max(numEnemies, minEnemies)
            for j in range(int(numEnemies)):
                if (len(enemyIndicesPool) == 0):
                    break
                enemyIndex = random.choice(enemyIndicesPool)
                enemyIndicesSelected.append(enemyIndex)
                enemyIndicesPool.remove(enemyIndex)
                # Sort the indices in enemyIndicesSelected so that they appear in the right order of location in a
                # section
            enemyIndicesSelected.sort()

        # Select a random list of numTreasures treasureIndices from the treasureIndicesPool
        treasureIndicesPool = []
        # 1 value treasures have a 40% chance of getting picked and the 4 value treasures have only a 10% chance of
        # getting picked.
        treasureValuePool = []
        for value in range(1, 5):
            treasureValuePool += [value] * ToonBlitzGlobals.TreasureValueProbability[value]
        treasureIndicesSelected = []
        if (treasuresPool != None):
            minTreasures, maxTreasures = attribs[8]
            for i in range(len(treasuresPool)):
                treasureIndicesPool += [i]
            numTreasures = maxTreasures * ToonBlitzGlobals.PercentMaxTreasures[szId] / 100
            numTreasures = max(numTreasures, minTreasures)
            for i in range(int(numTreasures)):
                if (len(treasureIndicesPool) == 0):
                    break
                treasureIndex = random.choice(treasureIndicesPool)
                treasureValue = random.choice(treasureValuePool)
                treasure = (treasureIndex, treasureValue)
                treasureIndicesPool.remove(treasureIndex)
                treasureIndicesSelected.append(treasure)
            # Sort the indices in treasureIndicesSelected so that they appear in the right order of location in a
            # section
            treasureIndicesSelected.sort()

        # Select a random list of numSpawnPoints spawnPointIndices from the spawnPointIndicesPool
        spawnPointIndicesPool = []
        spawnPointIndicesSelected = []
        if (spawnPointsPool != None):
            minSpawnPoints, maxSpawnPoints = attribs[9]
            for i in range(len(spawnPointsPool)):
                spawnPointIndicesPool += [i]
            numSpawnPoints = maxSpawnPoints * ToonBlitzGlobals.PercentMaxSpawnPoints[szId] / 100
            numSpawnPoints = max(numSpawnPoints, minSpawnPoints)
            for i in range(int(numSpawnPoints)):
                if (len(spawnPointIndicesPool) == 0):
                    break
                spawnPoint = random.choice(spawnPointIndicesPool)
                spawnPointIndicesSelected.append(spawnPoint)
                spawnPointIndicesPool.remove(spawnPoint)
            # Sort the spawnPoints in a section so that they appear in the right order in the section
            spawnPointIndicesSelected.sort()

        # Select a random list of numStompers stomperIndices from the stomperIndicesPool
        stomperIndicesPool = []
        stomperIndicesSelected = []
        if (stompersPool != None):
            minStompers, maxStompers = attribs[10]
            for i in range(len(stompersPool)):
                stomperIndicesPool += [i]
            numStompers = maxStompers * ToonBlitzGlobals.PercentMaxStompers[szId] / 100
            numStompers = max(numStompers, minStompers)
            for i in range(int(numStompers)):
                if (len(stomperIndicesPool) == 0):
                    break
                stomper = random.choice(stomperIndicesPool)
                stomperIndicesSelected.append(stomper)
                stomperIndicesPool.remove(stomper)
            # Sort the indices in stomperIndicesSelected so that they appear in the right order of location in a section
            stomperIndicesSelected.sort()

        # Change these attribs and make a tuples: (sectionIndex, enemyIndicesSelected, treasureIndicesSelected,
        # spawnPointIndicesPool)
        # The clients can take the length and the blockList from ToonBlitzGlobals.SectionTypes
        sctionTuple = (
        sectionIndex, enemyIndicesSelected, treasureIndicesSelected, spawnPointIndicesSelected, stomperIndicesSelected)
        sectionsSelected.append(sctionTuple)

    # sectionsSelected is the finalised list of sections along with enemyIndices, treasureIndices,
    # spawnPointIndices of each section.


generateSections()
targetClient.sectionsSelected = sectionsSelected  # given by the AI
targetClient.load()

targetClient.onstage()
targetClient.setGameReady()
targetClient.setGameStart(1)

base.run()
