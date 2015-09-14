#!/usr/bin/env python
import roslib; roslib.load_manifest('glodel')
import rospkg
import time

__builtins__.__openravepy_version__ = '0.9'
import openravepy as rave

from glodel.baseComplex import * 

base = BaseComplex('localhost',9160, 'Model', debug=False)

path = rospkg.RosPack().get_path("glodel") + "/res/"

sensor_list = ["cam", "laser2d", "lidar3d", "gp2d120", "dist"]
for sensor in sensor_list:
    print sensor, base.SENSORS.importSensor(sensor, "xml", path+"sensor/"+sensor+".sen.xml")


#### adding the main building
print base.LOCATIONS.importLocation("building", "stl", path+"location/building.stl")
print base.addComplex("_", "type", base.ident)
print base.addComplex("building", "base", "_")
print base.addComplex("building", "type", base.LOCATIONS.ident)
print base.addComplex("building", "key",  "building")
print base.addComplex("building", "transparency", "0.8")
print base.addComplex("building", "color", "0 0 0.75")

#### locations ....
room_list = ["09", "10", "11", "13", "14", "15", "16",
             "17", "18", "19", "20", "21", "22", "23",
             "24", "25", "26", "27", "back", "floor" ]

for room in room_list:
    print "adding room ", room, "to LOCATIONS ",
    print base.LOCATIONS.importLocation(room, "stl", path+"location/"+room+".stl")

#### adding floors
for n in range(5):
    print base.addComplex(str(n)+"_floor", "base", "building")
    print base.addComplex(str(n)+"_floor", "type", base.LOCATIONS.ident)
    print base.addComplex(str(n)+"_floor", "translation", '0 0 '+str(n*3))
    print base.addComplex(str(n)+"_floor", "transparency", "0.6")
    print base.addComplex(str(n)+"_floor", "key", "floor")

#### adding rooms to floors
for floor in range(5):
    floor = str(floor)
    for room in room_list:
        print base.addComplex(floor+room, "type", base.LOCATIONS.ident)
        print base.addComplex(floor+room, "base", floor+"_floor")
        print base.addComplex(floor+room, "key", room)
        print base.addComplex(floor+room, "transparency", "0.6")

        print base.addComplex("cam_"+floor+room, "base", floor+room)
        print base.addComplex("cam_"+floor+room, "type", base.SENSORS.ident)
        print base.addComplex("cam_"+floor+room, "key",  "lidar3d")
#        print base.addComplex("cam_"+floor+room, "translation", "0 0 2.5")
#        print base.addComplex("cam_"+floor+room, "quat", "0.00008726646233757571 0.9999999979250499 0 0")


    print base.addComplex(floor+"09", "translation", '3.2853 13.756 0')
    print base.addComplex(floor+"10", 'translation', '-5.9544 10.4807 0')
    print base.addComplex(floor+"11", 'translation', '2.6 7.9196 0')
    print base.addComplex(floor+"13", 'translation', '-5.673 3.4283 0')
    print base.addComplex(floor+"14", 'translation', '-5.118 0.0604 0')
    print base.addComplex(floor+"15", 'translation', '-4.68408 -5.2 0')
    print base.addComplex(floor+"16", 'translation', '-0.289 -4.9648 0')
    print base.addComplex(floor+"17", 'translation', '2.9015 0.8888 0')
    print base.addComplex(floor+"18", 'translation', '4.9445 0.5654 0')
    print base.addComplex(floor+"19", 'translation', '3.79 -4.93 0')
    print base.addComplex(floor+"20", 'translation', '10.004 2.0156 0')
    print base.addComplex(floor+"21", 'translation', '8.866 -4.688 0')
    print base.addComplex(floor+"22", 'translation', '13.753 2.1936 0')
    print base.addComplex(floor+"23", 'translation', '15.025 -5.84 0')
    print base.addComplex(floor+"24", 'translation', '18.96 -5.22 0')
    print base.addComplex(floor+"25", 'translation', '18.145 1.3913 0')
    print base.addComplex(floor+"26", 'translation', '22.405 -5.136 0')
    print base.addComplex(floor+"27", 'translation', '21.68 2.528 0')
    print base.addComplex(floor+"back", 'translation', '2.2847 34.7319 0')

# adding point clouds
print "point1", base.OBJECTS.importObject("point_cloud_309_0", "stl", path+"object/tablePointCloud_309.stl")
print "point2", base.OBJECTS.importObject("point_cloud_309_1", "stl", path+"object/robotPointCloud_309.stl")
for n in range(2):
    n=str(n)
    print base.addComplex("kinect_scan_309_"+n, "base", "309")
    print base.addComplex("kinect_scan_309_"+n, "type", base.OBJECTS.ident)
    print base.addComplex("kinect_scan_309_"+n, "key", "point_cloud_309_"+n)
    print base.addComplex("kinect_scan_309_"+n, "transparency", "0.3")
    print base.addComplex("kinect_scan_309_"+n, "color", "0 0 0.75")

print base.addComplex("kinect_scan_309_0", "translation", "-0.27 -1.125 0.0")
print base.addComplex("kinect_scan_309_0", "quat", "0.93493 0. 0. 0.35484")
print base.addComplex("kinect_scan_309_1", "translation", "-0.435 -3.311 0.0")
print base.addComplex("kinect_scan_309_1", "quat", "0.72229 0. 0. -0.69159")

robot_list = ["barrett-wam-sensors",
              "kawada-hironx",
              "man1",
              "neuronics-katana",
              "pumaarm",
              "rotation_stage",
              "shadow-hand",
              "kawada-hironx-parallelfingers",
              "kuka-youbot",
              "mitsubishi-pa10",
              "pr2-beta-static",
              "pumagripper",
              "schunk-lwa3"]

for robot in robot_list:
    print robot, base.ROBOTS.importRobot(robot, "zae", "/usr/local/share/openrave-0.9/robots/"+robot+".zae")


###############################################################################################
print base.OBJECTS.importObject("std_table", "stl", path+"object/table.stl")
print base.OBJECTS.importObject("std_mug", "dae", path+"object/mug.dae")
print base.OBJECTS.importObject("roboCupFrame", "xml", path+"object/roboCupFrame.obj.xml")
print base.OBJECTS.importObject("roboCupPlate", "xml", path+"object/roboCupPlate.obj.xml")

for n in range(8):
    n = str(n)
    print base.addComplex("table_"+n, "base", "315")
    print base.addComplex("table_"+n, "type", base.OBJECTS.ident)
    print base.addComplex("table_"+n, "key", "std_table")

# add tables to room 315
print base.addComplex("table_0", "translation", "1.23908 -1.729 0")
print base.addComplex("table_1", "translation", "-0.285 -1.3 0")
print base.addComplex("table_1", "quat", "0.7211 0. 0. -0.692")
print base.addComplex("table_2", "translation", "0.73908 2.66 0")
print base.addComplex("table_3", "translation", "-0.916 2.66 0")
print base.addComplex("table_4", "translation", "0.374 1.44 0")
print base.addComplex("table_4", "quat", "0.7211 0. 0. -0.692")
print base.addComplex("table_5", "translation", "-0.466 1.44 0")
print base.addComplex("table_5", "quat", "0.7211 0. 0. -0.692")
print base.addComplex("table_6", "translation", "-3.115 -1.9 0")
print base.addComplex("table_6", "quat", "0.398 0 0 0.9169")
print base.addComplex("table_7", "translation", "-1.98792 -2.495 0")
print base.addComplex("table_7", "quat", "-0.38212 0 0 0.92411")

print base.addComplex("roboCup", "base", "table_1")
print base.addComplex("roboCup", "type", base.ident)
print base.addComplex("roboCup", "translation", "0.15 0.35 0.66")
print base.addComplex("roboCup", "quat", "0.7211 0. 0. -0.7211")

print base.addComplex("roboCupPlate", "base", "roboCup")
print base.addComplex("roboCupPlate", "type", base.OBJECTS.ident)
print base.addComplex("roboCupPlate", "key", "roboCupPlate")

print base.addComplex("roboCupFrame", "base", "roboCup")
print base.addComplex("roboCupFrame", "type", base.OBJECTS.ident)
print base.addComplex("roboCupFrame", "key", "roboCupFrame")

#### Kitchen
kitchen_list = ["can", "chair", "coffe_machine", "cup", "knife_block",
                "microwave", "mixer", "pin", "plate", "shaker",
                "table", "toaster"]

for elem in kitchen_list:
    print base.OBJECTS.importObject(elem, "wrl", path+"kitchen/"+elem+".wrl")

print base.LOCATIONS.importLocation("kitchen", "wrl", path+"kitchen/kitchen.wrl")
print base.addComplex("kitchen", "type", base.LOCATIONS.ident)
print base.addComplex("kitchen", "base", "326")
print base.addComplex("kitchen", "quat", "0 0 0 1")
print base.addComplex("kitchen", "translation", "1.28 0.4 0.2")
print base.addComplex("kitchen", "scale", "0.000125")
print base.addComplex("kitchen", "key", "kitchen")

object_list = ["chair_2e39", "chair_12d0", "chair_6b56", "chair_083c",
               "table_34a2",
               "plate_835a", "plate_496f", "plate_fa76", "plate_b4e7",
               "cup_58a2", "cup_b6af", "cup_d441",
               "can", "coffe_machine", "mixer", "toaster", "microwave",
               #"pin_371e", "pin_a091", "pin_c671",
               "knife_block", "shaker" ]

for o in object_list:
    print base.addComplex(o, "type", base.OBJECTS.ident)
    print base.addComplex(o, "base", "kitchen")
    print base.addComplex(o, "scale", "0.000125")

print base.addComplex("chair_2e39", "key", "chair")
print base.addComplex("chair_2e39", "translation", "0.95 -1.15 0")
print base.addComplex("chair_2e39", "quat", ".82402 0 0 .56657")

print base.addComplex("chair_12d0", "key", "chair")
print base.addComplex("chair_12d0", "translation", ".43229 .17536 0")
print base.addComplex("chair_12d0", "quat", ".98286 0 0 -.18433")

print base.addComplex("chair_6b56", "key", "chair")
print base.addComplex("chair_6b56", "translation", "1.34 .27 0")
print base.addComplex("chair_6b56", "quat", "-.08079 0 0 .99673")

print base.addComplex("chair_083c", "key", "chair")
print base.addComplex("chair_083c", "translation", ".52 -0.60 0")

#########################################################################################
print base.addComplex("table_34a2", "key", "table")
print base.addComplex("table_34a2", "translation", ".91704 -.12644 0")

print base.addComplex("plate_835a", "key", "plate")
print base.addComplex("plate_835a", "translation", "1.06 -.73 1")

print base.addComplex("plate_496f", "key", "plate")
print base.addComplex("plate_496f", "translation", "0.67 -.45556 1")

print base.addComplex("plate_fa76", "key", "plate")
print base.addComplex("plate_fa76", "translation", "1.14 0 1")

print base.addComplex("plate_b4e7", "key", "plate")
print base.addComplex("plate_b4e7", "translation", "-1.13 2.01 1.5")

print base.addComplex("cup_58a2", "key", "cup")
print base.addComplex("cup_58a2", "translation", ".61 .45 1")

print base.addComplex("cup_b6af", "key", "cup")
print base.addComplex("cup_b6af", "translation", ".76 .55 1")

print base.addComplex("cup_d441", "key", "cup")
print base.addComplex("cup_d441", "translation", ".97 .58 1")

print base.OBJECTS.addObject("pos_marker", "xml", "<Body type='static'><Geom type='box'><extents>.2 .2 .0005</extents></Geom></Body>")
print base.addComplex("sink_b23a", "key", "pos_marker")
print base.addComplex("sink_b23a", "type", base.OBJECTS.ident)
print base.addComplex("sink_b23a", "base", "kitchen")
print base.addComplex("sink_b23a", "translation", ".35 2.3 0.9")
#base.ROBOTS.importRobot("katana_2222", "xml", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/robot/katana450/katana450sensing.xml")

print base.addComplex("can", "key", "can")
print base.addComplex("can", "translation", "-1.25 -.54 1.055")

print base.addComplex("coffe_machine", "key", "coffe_machine")
print base.addComplex("coffe_machine", "translation", "-1.335 .96 1.055")

print base.addComplex("mixer", "key", "mixer")
print base.addComplex("mixer", "translation", "1.69 2.3 1.05")

print base.addComplex("toaster", "key", "toaster")
print base.addComplex("toaster", "translation", "-1.26 -1.18 1.05")
print base.addComplex("toaster", "quat", ".94893 0 0 .3155")

print base.addComplex("microwave", "key", "microwave")
print base.addComplex("microwave", "translation", "-1.1 2.0 1.055")

#print base.addComplex("pin_371e", "key", "pin")
#print base.addComplex("pin_371e", "translation", "-1.2 1.4 .96")

#print base.addComplex("pin_a091", "key", "pin1")
#print base.addComplex("pin_a091", "translation", "-1.466 2.27 1.67")

#print base.addComplex("pin_c671", "key", "pin")
#print base.addComplex("pin_c671", "translation", "-1.11 2.286 1.67")

print base.addComplex("knife_block", "key", "knife_block")
print base.addComplex("knife_block", "translation", "-0.51 2.3 1.05")

print base.addComplex("shaker", "key", "shaker")
print base.addComplex("shaker", "translation", "2.13 2.26 1.05")

print base.addComplex("fridge_webcam", "type", base.SENSORS.ident)
print base.addComplex("fridge_webcam", "base", "kitchen")
print base.addComplex("fridge_webcam", "key", "lidar3d")
print base.addComplex("fridge_webcam", "translation", "-.87 -2.0 1.5")
print base.addComplex("fridge_webcam", "quat", "0.7071067811865 0 0.7071067811865 0")

print base.addCompleX("motion_detector",
                      base.SENSORS.ident,
                      "dist",
                      "kitchen",
                      "1.98 1.72 .75",
                      ".7071067811865476 0 0 -.7071067811865476")

#===============================================================================
# print base.addComplex("katana_62x", "base", "room309_complex_3")
# print base.addComplex("katana_62x", "type", base.ROBOTS.ident)
# print base.addComplex("katana_62x", "key", "katana_2222")
# print base.addComplex("katana_62x", "translation", "1.9 14.0 0.8")
#
# #print base.addComplex("ir0", "base", "katana_62x")
# #print base.addComplex("ir0", "type", base.SENSORS.ident)
# #print base.addComplex("ir0", "key", "katana_2222")
# #print base.addComplex("ir0", "translation", "1.9 14.0 0.8")


#
#
# #print base.addComplex("kuka_bot", "base", "room309_complex_3")
# #print base.addComplex("kuka_bot", "type", base.ROBOTS.ident)
# #print base.addComplex("kuka_bot", "key", "kuka-youbot")
# #
# #print base.addComplex("kuka_bot", "translation", "1.9 14.0 0.8")
# #print base.addComplex("katana_72", "quat", "0.93493 0. 0. 0.35484")
# #
# #print "floor1",base.OBJECTS.importObject("kinect_pcl1", "ply", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/object/floor_1.ply")
# #print "floor1",base.OBJECTS.importObject("kinect_pcl2", "ply", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/object/floor_2.ply")
# #print "floor1",base.OBJECTS.importObject("kinect_pcl3", "ply", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/object/floor_3.ply")
# #print "floor1",base.OBJECTS.importObject("kinect_pcl4", "ply", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/object/floor_4.ply")
#
# #print "floor1",base.OBJECTS.importObject("kinect_floor", "wrl", "/home/andre/Workspace/Projects/ROS/WoVi/model/base/environment/floor_full.wrl")
#
# #print base.addComplex("floor_wrl", "base", "room3_floor_complex_3")
# #print base.addComplex("floor_wrl", "type", base.OBJECTS.ident)
# #print base.addComplex("floor_wrl", "key", "kinect_floor")
# #print base.addComplex("floor_wrl4", "translation", "-1.7079 14.50587 0.77502")
# #print base.addComplex("floor_wrl4", "quat", "0.30404 0.03025 0.00955 0.95213")
#
# #print base.addComplex("floor_wrl3", "base", "room3_floor_complex_3")
# #print base.addComplex("floor_wrl3", "type", base.OBJECTS.ident)
# #print base.addComplex("floor_wrl3", "key", "kinect_pcl3")
# #print base.addComplex("floor_wrl4", "translation", "-1.7079 14.50587 0.77502")
# #print base.addComplex("floor_wrl4", "quat", "0.30404 0.03025 0.00955 0.95213")
# #print base.addComplex("floor_wrl3", "transparency", "0.5")
#
# #print base.addComplex("floor_wrl2", "base", "room3_floor_model_3")
# #print base.addComplex("floor_wrl2", "type", base.OBJECTS.ident)
# #print base.addComplex("floor_wrl2", "key", "kinectscan_pcl2")
# #print base.addComplex("floor_wrl4", "translation", "-1.7079 14.50587 0.77502")
# #print base.addComplex("floor_wrl4", "quat", "0.30404 0.03025 0.00955 0.95213")
# #print base.addComplex("floor_wrl2", "transparency", "0.5")
#===============================================================================


#env = rave.Environment() # create a new environment
#env.SetViewer('qtcoin')  # open viewer
#env = base.createModel("_", 10, env)  # generate environment of katana_62x (search depth = 10)
#raw_input('press ENTER to continue...')
