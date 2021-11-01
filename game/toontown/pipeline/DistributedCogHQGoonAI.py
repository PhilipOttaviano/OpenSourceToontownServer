from panda3d.core import *
from direct.task.TaskManagerGlobal import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.suit import GoonGlobals
from direct.task.Task import Task
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.showbase import PythonUtil
from toontown.suit import DistributedGoonAI
import math
import random


class DistributedCogHQGoonAI(DistributedGoonAI.DistributedGoonAI):
    offMask = BitMask32(0)
    onMask = CollisionNode.getDefaultCollideMask()

    id = 0

    def __init__(self, air):
        DistributedGoonAI.DistributedGoonAI.__init__(self, air, 0)
        self.air = air
