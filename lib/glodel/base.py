from RosCassandra.Cassandra import Cassandra

import pycassa
import pickle
import time

class Base(Cassandra):

    def __init__(self, host, port, keyspace, column, debug=False):
        self.DEBUG = debug
        Cassandra.__init__(self, host, port)

        if self.connectToKeyspace(keyspace):
            self.columnName = column

            self.col = self.getColumn(column)

    def addModel(self, key, column, value):
        self.debug("addModel("+key+", "+str(column)[:50]+", "+str(value)+" )")
        try:
            self.col.insert(key, {column: value})
            time.sleep(0.05)
        except:
            return False
        return True

    def getModel(self, key, column=False):
        if column == False:
            self.debug("getModel: %s, %s ..." % (key, str(self.col.get(key))[:50]))
            return self.col.get(key)
        else:
            self.debug("getModel: %s, %s, %s ..." % (key, column, str(self.col.get(key))[:50]))
            return self.col.get(key)[column]

    def removeModel(self, key, column=False):
        self.debug("removeModel("+str(key)+", "+str(column)[:50]+" )")
        try:
            if column == False:
                self.col.remove(key)
            else:
                self.col.remove(key, column)
        except:
            return False
        return True

    def catalogue(self):
        keys = []
        gen = self.col.get_range("","")

        for key,_ in gen:
            keys.append(key)

        return keys

    def getAllColumnNames(self):
        names = []

        return names

    def readFile(self, filename):
        self.debug("readFile("+filename+" )")
        fp = open(filename,"rb")
        content = ""
        try:
            while True:
                fBuffer = fp.read(1024)
                if fBuffer=="":
                    break
                else:
                    content += fBuffer
        finally:
            fp.close()
        return content#pickle.dumps(content)

    def debug(self, msg):
        if self.DEBUG :
            print msg
