#!/usr/bin/env python
import roslib; roslib.load_manifest('glodel')
import rospkg
import time

from glodel.plugOpenrave import plugOpenrave

__builtins__.__openravepy_version__ = '0.9'
import openravepy as rave

from glodel.baseComplex import *

base = BaseComplex('localhost',9160, 'Model', debug=False)
plug = plugOpenrave(base)


print base.typeOf("326"), "  ",base.baseOf("326")

env = rave.Environment() # create a new environment
env.SetViewer('qtcoin')  # open viewer
env = plug.createEnvironment("3_floor", 10, env)  # generate environment of katana_62x (search depth = 10)

for sensor in env.GetSensors():
    sensor.Configure(rave.Sensor.ConfigureCommand.PowerOn)
    sensor.Configure(rave.Sensor.ConfigureCommand.RenderDataOn)


raw_input('press ENTER to continue...')
