#!/usr/bin/env python
import roslib; roslib.load_manifest('glodel')

import pycassa
from RosCassandra.Cassandra import Cassandra

from glodel.baseLocation import BaseLocation
from glodel.baseObject import BaseObject
from glodel.baseSensor import BaseSensor
from glodel.baseRobot import BaseRobot
from glodel.baseComplex import BaseComplex

host = "localhost"
port = 9160
keyspace = 'Model'

base = Cassandra(host, port)

base.dropKeyspace(keyspace)

if not base.connectToKeyspace(keyspace):
    print "try to create new keyspace ...",
    base.createKeyspace(keyspace)
    print "done"
else:
    print "keyspace already exists"

if not base.existColumn(BaseObject.ident):
    print "try to create new ColumnFamily", BaseObject.ident, "..."
    base.createColumn(BaseObject.ident)
    print "done"
else:
    print "ColumnFamily ", BaseObject.ident, "already exists"

if not base.existColumn(BaseSensor.ident):
    print "try to create new ColumnFamily", BaseSensor.ident, "..."
    base.createColumn(BaseSensor.ident)
    print "done"
else:
    print "ColumnFamily ", BaseSensor.ident, "already exists"

if not base.existColumn(BaseRobot.ident):
    print "try to create new ColumnFamily", BaseRobot.ident, "..."
    base.createColumn(BaseRobot.ident)
    print "done"
else:
    print "ColumnFamily ", BaseRobot.ident, "already exists"

if not base.existColumn(BaseLocation.ident):
    print "try to create new ColumnFamily", BaseLocation.ident, "..."
    base.createColumn(BaseLocation.ident)
    print "done"
else:
    print "ColumnFamily ", BaseLocation.ident, "already exists"

if not base.existColumn(BaseComplex.ident):
    print "try to create new ColumnFamily", BaseComplex.ident, "..."
    base.createColumn(BaseComplex.ident, super=False, column_validation_classes={"base":pycassa.UTF8_TYPE,
                                                       "key": pycassa.UTF8_TYPE,
                                                       "type":pycassa.UTF8_TYPE})
    print "done"

    print "creating index for base ..."
    base.sysManager.create_index(keyspace, BaseComplex.ident, "base", pycassa.UTF8_TYPE, index_name='base_index')
    print "done"
    print "creating index for key ..."
    base.sysManager.create_index(keyspace, BaseComplex.ident, "key",  pycassa.UTF8_TYPE, index_name='key_index')
    print "done"
    print "creating index for type ..."
    base.sysManager.create_index(keyspace, BaseComplex.ident, "type", pycassa.UTF8_TYPE, index_name='type_index')
    print "done"
else:
    print "ColumnFamily ", BaseComplex.ident, "already exists"
