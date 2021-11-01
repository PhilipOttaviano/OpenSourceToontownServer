from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import GoonGlobals
from direct.task.Task import Task
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.showbase import PythonUtil
from toontown.suit import DistributedGoon


class DistributedCogHQGoon(DistributedGoon.DistributedGoon):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCogHQGoon')

    def __init__(self, cr):
        DistributedGoon.DistributedGoon.__init__(self, cr)
        self.cr = cr
        self.doId = 0
        self.name = 'goon-%s' % self.doId
        self.undead()
        self.reparentTo(render)
        self.setPos(0, 0, 0)

    def generate(self):
        DistributedGoon.DistributedGoon.generate(self)

    def announceGenerate(self):
        DistributedGoon.DistributedGoon.announceGenerate(self)
        self.setName(self.name)
        self.setTag('doId', str(self.doId))
        self.reparentTo(render)

    def disable(self):
        DistributedGoon.DistributedGoon.disable(self)
