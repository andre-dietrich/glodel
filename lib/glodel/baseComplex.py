from base import Base
from baseLocation import BaseLocation
from baseObject import BaseObject
from baseRobot import BaseRobot
from baseSensor import BaseSensor

from numpy import array

import openravepy as rave
import tf.transformations as tf

import pycassa

class BaseComplex(Base):
    
    ident = "COMPLEX"
    
    element = {BaseObject.ident:    '1', 
               BaseRobot.ident:     '2', 
               BaseSensor.ident:    '3', 
               BaseLocation.ident:  '4', 
               ident:   '5'}
    
    attribute = ['base',
                 'direction',
                 'link',
                 'offset',
                 'quat',
                 'rotationaxis',
                 'rotationmat',
                 'scale',
                 'translation',
                 'transparency' ]
    
    def __init__(self, host, port, keyspace, debug=False):
        Base.__init__(self, host, port, keyspace, BaseComplex.ident, debug)
        
        self.ROBOTS     = BaseRobot     (host, port, keyspace, debug)
        self.OBJECTS    = BaseObject    (host, port, keyspace, debug)
        self.SENSORS    = BaseSensor    (host, port, keyspace, debug)
        self.LOCATIONS  = BaseLocation  (host, port, keyspace, debug)
        
#    def getColumn(self, key, col):
#        return self

    def typeOf(self, key):
        return self.getComplex(key, "type")
        
    def getComplex(self, key, format_=False):
        return self.getModel(key, format_)
    
    def addComplex(self, key, value, data):
        return self.addModel(key, value, data)
    
    def getComplexURDF(self, key, base=None):
        pass
    
    def baseOf(self, key):
        return self.getModel(key, "base")
    
    def addObject(self, key, format_, description):
        self.OBJECTS.addObject(key, format_, description)

    def importObject(self, key, format_, filename):
        self.OBJECTS.importObject(key, format_, filename)

    def addRobot(self, key, format_, description):
        self.ROBOTS.addRobot(key, format_, description)

    def importRobot(self, key, format_, filename):
        self.ROBOTS.importRobot(key, format_, filename)

    def addCompleX(self, id_, type_, key, base, translation="", quat=""):
        self.addModel(id_, "type", type_)
        self.addModel(id_, "key", key)
        self.addModel(id_, "base", base)
        if translation!="":
            self.addModel(id_, "translation", translation)
        if quat != "":
            self.addModel(id_, "quat", quat)
    
        
        