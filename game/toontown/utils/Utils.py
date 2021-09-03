from direct.interval.IntervalGlobal import *


def makeProp(self, propStr):
    prop = loader.loadModel(str(propStr))
    global prop

def getAllProps(self):
    return prop
