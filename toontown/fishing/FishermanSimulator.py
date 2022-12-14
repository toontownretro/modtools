"""
FishermanSimulator
Author: Loonatic
Date: 13 December 2022

Generator code to run the prototype fishingSim module.
"""

from modtools.toontown.toonbase import ModularStart
from modtools.toontown.toonbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()

# Do not know if there was possibly a base model used for reference.
# testModel = loader.loadModel("phase_4/models/modules/TT_pond")
# testModel.reparentTo(render)

# Create our fishing target
from toontown.fishing.DistributedFishingTarget import DistributedFishingTarget

base.distributedFishingTarget = DistributedFishingTarget(base.cr)
base.distributedFishingTarget.fishingTargetNode = base.distributedFishingTarget
base.distributedFishingTarget.dclass = base.cr.dclassesByName['DistributedFishingTarget']
base.distributedFishingTarget.doId = 420
base.distributedFishingTarget.generate()

# Create our fishingSim module
from toontown.fishing import fishingSim as FishingSim

# Generate Slot Machines

"""
SlotMachine2D is the nx4 matrix on the right side of the screen.
Number of rows by default is 6, can be changed by modifying numLines argument.
Number of columns is fixed at 4, one for each fisherman.

Number on the left is the fisherman's ID
Number on the right is a random int [0-3]

In a fisherman's column, text will turn red if they get the same value three times in a row from casts.
"""
sm2d = FishingSim.SlotMachine2D(numLines = 6)
sm2d.frame.setPos(0.8, 0, 0.6)
sm2d.frame.setScale(.7)

sm = FishingSim.SlotMachine()
sm.frame.setScale(.7)
sm.frame.setPos(2.0, 0, .18)

# Generate Fishermen - They are all Flippy by default.
# Change fishAutonomous = 0 to manually control the fishermen casting.
fisherman1 = FishingSim.Fisherman(0)
fisherman1.setPosHpr(-77.89, 46.82, -3.18, 183.81, 0.00, 0.00)

fisherman2 = FishingSim.Fisherman(1)
fisherman2.setPosHpr(-91.00, 42.83, -3.18, 211.61, 0.00, 0.00)

fisherman3 = FishingSim.Fisherman(2)
fisherman3.setPosHpr(-95.28, 31.55, -3.18, 251.57, 0.00, 0.00)

fisherman4 = FishingSim.Fisherman(3, fAutonomous = 0)
fisherman4.setPosHpr(-97.49, 18.91, -3.48, 270.00, 0.00, 0.00)

fishermanList = [fisherman1, fisherman2, fisherman3, fisherman4]


def kill():
    for f in fishermanList:
        f.destroy()


def stopCasting():
    for f in fishermanList:
        f.stopCasting()


def startCasting():
    for f in fishermanList:
        f.startCasting()


# Adjust Camera
# base.camera.place()
# just to get a better view of our Toons
# base.camera.setPosHprScale(-43.96, 9.86, 2.95, 61.70, 0.00, 0.00, 1.00, 1.00, 1.00)
# base.camera.setPosHprScale(-77.90, -19.24, 21.60, 4.76, 333.43, 0.00, 1.00, 1.00, 1.00)
# top down view
base.camera.setPosHprScale(-85.00, 20.00, 87.07, 240.00, 270.00, 0.00, 1.00, 1.00, 1.00)

base.run()
