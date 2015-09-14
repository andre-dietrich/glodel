from base import Base

class BaseSensor(Base):

    ident = "SENSOR"

    def __init__(self, host, port, keyspace, debug=False):
        Base.__init__(self, host, port, keyspace, BaseSensor.ident, debug)
        
    def addSensor(self, key, format_, description):
        return self.addModel(key, format_, description)
            
    def getSensor(self, key, format_=False):
        return self.getModel(key, format_)
    
    def removeSensor(self, key, format_):
        return self.removeModel(key, format_)
        
    def importSensor(self, key, format_, filename):
        sensor_def = self.readFile(filename)
        return self.addSensor(key, format_, sensor_def)
        
    def importSensorURDF(self, key, filename):
        sensor_def = self.readFile(filename)
        return self.addSensor(key, "urdf", sensor_def)
    
    def importSensorMosaic(self, key, filename):
        sensor_def = self.readFile(filename)
        return self.addSensor(key, "mosaic", sensor_def)
