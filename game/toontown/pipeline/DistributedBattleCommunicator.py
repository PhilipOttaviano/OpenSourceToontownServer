from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from direct.fsm import State
from toontown.battle import BattleBase
from toontown.hood import ZoneUtil


class DistributedBattleCommunicator(DistributedObject.DistributedObject):

    def __init__(self, cr):
        self.cr = cr
        DistributedObject.DistributedObject.__init__(self, cr)
