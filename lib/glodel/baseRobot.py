from base import Base

class BaseRobot(Base):
    
    ident = "ROBOT"

    def __init__(self, host, port, keyspace, debug=False):
        Base.__init__(self, host, port, keyspace, BaseRobot.ident, debug)
        
    def addRobot(self, key, format_, description):
        return self.addModel(key, format_, description)
            
    def getRobot(self, key, format_=False):
        robot = self.getModel(key, format_)
        #if not format_:
        #    robot = robot[robot.keys()[0]]
        return robot
    
    def removeRobot(self, key, format_):
        return self.removeModel(key, format_)
        
    def importRobot(self, key, format_, filename):
        robot_def = self.readFile(filename)
        return self.addRobot(key, format_, robot_def)
        
    def importRobotURDF(self, key, filename):
        robot_def = self.readFile(filename)
        return self.addRobot(key, "urdf", robot_def)
    
    def importRobotZAE(self, key, filename):
        robot_def = self.readFile(filename)
        return self.addRobot(key, "zae", robot_def)
    
    def importRobotDAE(self, key, filename):
        robot_def = self.readFile(filename)
        return self.addRobot(key, "dae", robot_def)

