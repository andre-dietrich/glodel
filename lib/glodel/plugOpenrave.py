from baseComplex import BaseComplex

#from numpy import array

import openravepy as rave
import tf.transformations as tf

import pycassa

class plugOpenrave():
    
    def __init__(self, base):
        self.env = rave.Environment()
        self.base = base
        
        self.count = 1
        
    def createEnvironment(self, key, iter=0, env=None):
        if env != None:
            self.env = env
        else:
            self.env = rave.Environment()
        
        ee = self.getEnv(key, iter, True)
        with self.env:
            for e in ee:
                self.env.Add(e)
                                
        return self.env
        
    def getEnv(self, key, iter=0, first=False):
        
        val = self.base.getModel(key)
        
        print key, val
        
        obj = None
        obj_list = []
        parent_tf = tf.identity_matrix()
        
        if self.base.typeOf(key) == self.base.ROBOTS.ident:
            obj = self._getRobot(key)
            obj_list.append(obj)
            parent_tf = obj.GetTransform()
        
        elif self.base.typeOf(key) == self.base.OBJECTS.ident:
            obj = self._getObject(key)
            obj_list.append(obj)
            parent_tf = obj.GetTransform()
                
        elif self.base.typeOf(key) == self.base.LOCATIONS.ident:
            obj = self._getLocation(key)
            obj_list.append(obj)
            parent_tf = obj.GetTransform()
            
        elif self.base.typeOf(key) == self.base.SENSORS.ident:
            obj = self._getSensor(key)
            obj_list.append(obj)
            parent_tf = obj.GetTransform()
            
        else:
            if val.has_key("translation"):
                translation = map(lambda x: float(x), val["translation"].split(" "))
                parent_tf = tf.concatenate_matrices(parent_tf, tf.compose_matrix(translate = translation))
            if val.has_key("quat"):
                quat = map(lambda x: float(x), val["quat"].split(" "))
                rot = rave.axisAngleFromQuat(quat)
                m2 = tf.compose_matrix(angles = rot)
                parent_tf = tf.concatenate_matrices(parent_tf, m2)     
        
        if first:
            parent_tf = tf.identity_matrix()
            if obj != None:
                obj.SetTransform(parent_tf)
        
        if iter==0:
            return obj_list            
        
        # search for ancestors
        child_expr   = pycassa.create_index_expression('base', key)
        clild_clause = pycassa.create_index_clause([child_expr])
        
        for child_key, _ in self.base.col.get_indexed_slices(clild_clause):
            child_obj = self.getEnv(child_key, iter-1)
            for obj in child_obj:
                if type(obj) != type(None):
                    obj.SetTransform(tf.concatenate_matrices(parent_tf, obj.GetTransform()))
                    obj_list.append(obj)
            
        return obj_list
    
    def _getRobot(self, key):
        
        complex = self.base.getModel(key)
        color = scale = transparency = ""
                
        if complex.has_key("color"):        color = complex["color"]
        if complex.has_key("scale"):        scale = complex["scale"]
        if complex.has_key("transparency"): transparency = complex["transparency"]
        
        obj = self.base.ROBOTS.getRobot( complex["key"] )
        rave_obj = self.toOpenrave(obj, key, complex['type'], color, transparency, scale)
        rave_obj = self.transformOpenrave(rave_obj, complex)

        return rave_obj
    
    def _getObject(self, key):
        
        complex = self.base.getModel(key)
        color = scale = transparency = ""
                
        if complex.has_key("color"):        color = complex["color"]
        if complex.has_key("scale"):        scale = complex["scale"]
        if complex.has_key("transparency"): transparency = complex["transparency"]
        
        obj = self.base.OBJECTS.getObject( complex["key"] )
        rave_obj = self.toOpenrave(obj, key, complex['type'], color, transparency, scale)
        rave_obj = self.transformOpenrave(rave_obj, complex)

        return rave_obj
    
    def _getLocation(self, key):
        
        complex = self.base.getModel(key)
        color = scale = transparency = ""
                
        if complex.has_key("color"):        color = complex["color"]
        if complex.has_key("scale"):        scale = complex["scale"]
        if complex.has_key("transparency"): transparency = complex["transparency"]
        
        obj = self.base.LOCATIONS.getLocation( complex["key"] )
        rave_obj = self.toOpenrave(obj, key, complex['type'], color, transparency, scale)
        rave_obj = self.transformOpenrave(rave_obj, complex)

        return rave_obj

    def _getSensor(self, key):
        
        complex = self.base.getModel(key)
        color = scale = transparency = ""
                
        if complex.has_key("color"):        color = complex["color"]
        if complex.has_key("scale"):        scale = complex["scale"]
        if complex.has_key("transparency"): transparency = complex["transparency"]
        
        obj = self.base.SENSORS.getSensor( complex["key"] )
        rave_obj = self.toOpenrave(obj, key, complex['type'], color, transparency, scale)
        rave_obj = self.transformOpenrave(rave_obj, complex)

        return rave_obj
    
    def transformOpenrave(self, openrave_obj, complex_data):
        if complex_data.has_key("translation"):
            translation = map(lambda x: float(x), complex_data["translation"].split(" "))
            m1 = openrave_obj.GetTransform()
            m2 = tf.compose_matrix(translate = translation)
            openrave_obj.SetTransform(tf.concatenate_matrices(m1, m2))
        if complex_data.has_key("quat"):
            quat = map(lambda x: float(x), complex_data["quat"].split(" "))
            m1 = openrave_obj.GetTransform()
            rot = rave.axisAngleFromQuat(quat)
            m2 = tf.compose_matrix(angles = rot)
            openrave_obj.SetTransform(tf.concatenate_matrices(m1, m2))    
        return openrave_obj
    
     
    def toOpenrave(self, obj, name, type_, color="", transparency="", scale=""):
        
        self.count = str(int(self.count)+1)
        
        formatFile = ("zae", "dae", "stl")
        formatXML  = ("xml", "urdf")
        formatRen  = ("wrl")
        
        format_ = None
                        
        if len(color) > 0:
            color = "<diffusecolor>" + color + "</diffusecolor>"
        if len(transparency) > 0:
            transparency = "<transparency>" + transparency + "</transparency>"
        
        # check for valid formats
        for key in obj.keys():            
            if key in formatFile or key in formatRen:
                format_ = key
                f = open('/tmp/obj_'+self.count+"."+format_, 'wb')
                f.write(obj[format_])
                f.close()
                break
            if key in formatXML:
                format_ = key
                break
        
        #######################################################################################################
        if type_ == self.base.OBJECTS.ident:
            if format_ in formatFile:
                description = "<kinbody name='"+name+"'><body type='dynamic' name='"+name+"'><geom type='trimesh'>"+color+transparency+"<data>/tmp/obj_"+self.count+"."+format_+" "+scale+"</data></geom></body></kinbody>"
            elif format_ in formatXML:
                description = "<kinbody name='"+name+"'>"+color+transparency+obj[format_]+"</kinbody>"
            elif format_ in formatRen:
                description = "<kinbody name='"+name+"'><body type='dynamic' name='"+name+"'><geom type='trimesh'><render>/tmp/obj_"+self.count+"."+format_+" "+scale+"</render></geom></body></kinbody>"
            kinBody = self.env.ReadKinBodyXMLData(description)
            print description
            return kinBody
        #######################################################################################################
        elif type_ == self.base.LOCATIONS.ident:
            if format_ in formatFile:
                description = "<kinbody name='"+name+"'><body type='static' name='"+name+"'><geom type='trimesh'>"+color+transparency+"<data>/tmp/obj_"+self.count+"."+format_+" "+scale+"</data></geom></body></kinbody>"
            elif format_ in formatRen:
                description = "<kinbody name='"+name+"'><body type='static' name='"+name+"'><geom type='trimesh'><render>/tmp/obj_"+self.count+"."+format_+" "+scale+"</render></geom></body></kinbody>"
            kinBody = self.env.ReadKinBodyXMLData(description)
            print description
            return kinBody
        #######################################################################################################
        elif type_ == self.base.ROBOTS.ident:
            if format_ in formatFile:
                robot = self.env.ReadRobotXMLFile("/tmp/obj_"+self.count+"."+format_)
                robot.SetName(name)
            elif format_ in formatXML:
                robot = self.env.ReadRobotXMLData(obj[format_])
                robot.SetName(name)
            return robot
        #######################################################################################################
        elif type_ == self.base.SENSORS.ident:
            f = open('/tmp/obj_'+self.count+"."+format_, 'wb')
            f.write(obj[format_])
            f.close()
            if format_ in formatXML:
                sensor = self.env.ReadInterfaceXMLFile("/tmp/obj_"+self.count+"."+format_, {"name": name})
            return sensor
        
        return False
