from direct.distributed import DistributedObject

class DistributedPythonTest(DistributedObject.DistributedObject):
  def __init__(self, cr):

      DistributedObject.DistributedObject.__init__(self, cr)

      self.cr = cr
