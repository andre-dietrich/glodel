from base import Base

class BaseLocation(Base):
    
    ident = "LOCATION"

    def __init__(self, host, port, keyspace, debug=False):
        Base.__init__(self, host, port, keyspace, BaseLocation.ident)
        
    def addLocation(self, key, format_, description):
        return self.addModel(key, format_, description)
            
    def getLocation(self, key, format_=False):
        return self.getModel(key, format_)
    
    def removeLocation(self, key, format_):
        return self.removeModel(key, format_)
        
    def importLocation(self, key, format_, filename):
        robot_def = self.readFile(filename)
        return self.addLocation(key, format_, robot_def)
        
    def importLocationURDF(self, key, filename):
        robot_def = self.readFile(filename)
        return self.addLocation(key, "urdf", robot_def)
 