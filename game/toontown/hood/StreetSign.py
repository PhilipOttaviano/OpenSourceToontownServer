import os
import shutil
import datetime
from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.showbase import AppRunnerGlobal
from toontown.toonbase import TTLocalizer

class StreetSign(DistributedObject.DistributedObject):
    RedownloadTaskName = 'RedownloadStreetSign'
    StreetSignFileName = config.GetString('street-sign-filename', 'texture.jpg')
    StreetSignBaseDir = config.GetString('street-sign-base-dir', 'sign')
    StreetSignUrl = base.config.GetString('street-sign-url', 'https://ttoffline.com/images/')
    notify = DirectNotifyGlobal.directNotify.newCategory('StreetSign')

    def __init__(self):
        self.downloadingStreetSign = False
        self.percentDownloaded = 0.0
        self.startDownload = datetime.datetime.now()
        self.endDownload = datetime.datetime.now()
        self.notify.info('Street sign url is %s' % self.StreetSignUrl)

    def replaceTexture(self):
        pass

    def redownloadStreetSign(self):
        pass

    def downloadStreetSignTask(self, task):
        pass
