def generateDCOBJclient():
    with open('TestPython.py', 'w') as writer:
        writer.write("from direct.distributed import DistributedObject\n")
        writer.write("\n")
        writer.write("class DistributedPythonTest(DistributedObject.DistributedObject):\n")
        writer.write("  def __init__(self, cr):\n")
        writer.write("\n")
        writer.write("      DistributedObject.DistributedObject.__init__(self, cr)\n")
        writer.write("\n")
        writer.write("      self.cr = cr\n")

def generate

def generateFromComment():
    with open('TestPython.py', 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:
            if line == "# Make a distributed object for client":
                generateDCOBJclient()
                print("Coding")



generateFromComment()
