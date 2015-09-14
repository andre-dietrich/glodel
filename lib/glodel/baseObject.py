from base import Base

class BaseObject(Base):
    
    ident = "OBJECT"

    def __init__(self, host, port, keyspace, debug=False):
        Base.__init__(self, host, port, keyspace, BaseObject.ident, debug)
        
    def addObject(self, key, format_, description):
        return self.addModel(key, format_, description)
            
    def getObject(self, key, format_=False):
        return self.getModel(key, format_)
    
    def removeObject(self, key, format_=False):
        return self.removeModel(key, format_)
        
    def importObject(self, key, format_, filename):
        robot_def = self.readFile(filename)
        return self.addObject(key, format_, robot_def)
        
    def importObjectURDF(self, key, filename):
        robot_def = self.readFile(filename)
        return self.addObject(key, "urdf", robot_def)    

