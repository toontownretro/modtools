from direct.fsm import State

from modtools.toontown.toonbase import ModularStart
from modtools.toontown.toonbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()
base.generateLocalAvatar()
# base.startConnection()

base.localAvatar.dclass = base.cr.dclassesByName['DistributedToon']
base.localAvatar.laffMeter = None  # required to prevent an AttributeError

# client side init
base.cr.playGame.hood = base.cr.playGame
base.cr.playGame.hood.fsm.addState(
    State.State('minigame')
)
base.cr.playGame.hood.id = 2000
# base.ai.repo.minigameSafezoneId = 2000


from toontown.minigame.DistributedVineGame import DistributedVineGame

# pre-load preparation
DistributedVineGame.doId = 69
DistributedVineGame.hasLocalToon = 1
DistributedVineGame.trolleyZone = 2000
DistributedVineGame.numPlayers = 1
vineClient = DistributedVineGame(base.cr)
# targetClient.setTrolleyZone(1)
vineClient.defineConstants()
vineClient.setParticipants([1])
vineClient.dclass = base.cr.dclassesByName['DistributedVineGame']

vineClient.vineSections = [9, 9, 9, 9]  # test specific parameters
# vineClient.vineSections = [0,0,0,0] # test really easy
# vineClient.vineSections = [3,2,1,0] # test easy
# vineClient.vineSections = [7,6,5,4] # test hard
# vineClient.vineSections = [8,7,6,5] # test hardest

from direct.showbase import RandomNumGen

rng = RandomNumGen.RandomNumGen(42069)
vineClient.randomNumGen = rng

# game load
vineClient.load()
# targetClient.setTargetSeed(targetSeed = 12345)
base.cr.doId2do[1] = base.localAvatar
vineClient.onstage()
vineClient.setGameReady()
vineClient.setGameStart(1)

# from direct.tkpanels.FSMInspector import FSMInspector
# minigameFSM_insp = FSMInspector(vineClient.gameFSM)

# from toontown.minigame.DistributedTargetGameAI import DistributedTargetGameAI
# targetAI = DistributedTargetGameAI(base.ai.repo, 10)
# targetAI.trolleyZone = 2000
# targetAI.doId = 69
# targetAI.setGameReady()


# base.oobe()
base.run()
