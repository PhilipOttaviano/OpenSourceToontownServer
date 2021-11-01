from toontown.toonbase.ToontownBattleGlobals import *
from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObjectAI
from direct.fsm import State
from toontown.battle import DistributedBattleBldgAI
from toontown.battle import BattleBase
from direct.task import Timer
import copy


class DistributedBattleCommunicatorAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air):
        self.air = air
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
