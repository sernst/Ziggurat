# ZigguratModelUtils.py
# (C)2011-2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os

from pyaid.decorators.ClassGetter import ClassGetter

from ziggurat.sqlalchemy.ZigguratDatabaseDefinition import ZigguratDatabaseDefinition
from ziggurat.utils.debug.ServerLogger import ServerLogger

#___________________________________________________________________________________________________ ZigguratModelUtils
class ZigguratModelUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _LOGGER = ServerLogger('ZigguratModels')

    isWebEnvironment = False

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ logger
    @ClassGetter
    def logger(cls):
        return cls._LOGGER

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ modelsInit
    @classmethod
    def initializeModels(cls, initLocalVars):
        initPath = initLocalVars['__path__']
        initName = initLocalVars['__name__']

        for module in os.listdir(initPath[0]):
            if module == '__init__.py' or module[-3:] != '.py' or module.find('_') == -1:
                continue

            n = module[:-3]
            m = initName + '.' + n
            r = __import__(m, locals(), globals(), [n])
            c = getattr(r, n)
            try:
                c.MASTER
                c.SLAVE
            except Exception as err:
                cls.logger.writeError('Model Initialization Failure: ' + str(c.__name__), err)

#___________________________________________________________________________________________________ createDatabaseDefinition
    @classmethod
    def createDatabaseDefinition(cls, **kwargs):
        return ZigguratDatabaseDefinition(**kwargs)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
