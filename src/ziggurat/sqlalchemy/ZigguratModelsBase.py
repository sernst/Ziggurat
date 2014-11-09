# ZigguratModelsBase.py
# (C)2012-2014
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import datetime

from pyaid.string.StringUtils import StringUtils
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from pyaid.radix.Base36 import Base36
from pyaid.radix.Base64 import Base64

from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils
from ziggurat.sqlalchemy.meta.AbstractModelsMeta import AbstractModelsMeta


#___________________________________________________________________________________________________ ZigguratModelsBase
class ZigguratModelsBase(object):

#===================================================================================================
#                                                                                       C L A S S

    __metaclass__  = AbstractModelsMeta
    __abstract__   = True

    _i      = Column(Integer, primary_key=True)
    _upts   = Column(DateTime, default=datetime.datetime.utcnow())
    _cts    = Column(DateTime, default=datetime.datetime.utcnow())

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        super(ZigguratModelsBase, self).__init__()
        self.ormInit()

#___________________________________________________________________________________________________ ormInit
    def ormInit(self):
        pass

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: i16
    @property
    def i16(self):
        return hex(self.i)[2:]

#___________________________________________________________________________________________________ GS: i36
    @property
    def i36(self):
        return Base36.to36(self.i)

#___________________________________________________________________________________________________ GS: i64
    @property
    def i64(self):
        return Base64.to64(self.i)

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        return ZigguratModelUtils.logger

#___________________________________________________________________________________________________ GS: session
    @property
    def session(self):
        return self.createSession()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getValue
    def getValue(self, name):
        """Returns the value of the specified property, or None if the property is not specified.

        @@@param name:string
            The name of the property to retrieve. """

        return getattr(self, name)

#___________________________________________________________________________________________________ createSession
    @classmethod
    def createSession(cls):
        return cls._session.getRawSession()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getReprString
    def _getReprString(self):
        return None

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        modelInfo = self._getReprString()
        return '<%s[%s] cts[%s] upts[%s]%s>' % (
            self.__class__.__name__,
            StringUtils.toUnicode(self.i),
            StringUtils.toUnicode(self.cts.strftime('%m-%d-%y %H:%M:%S') if self.cts else 'None'),
            StringUtils.toUnicode(self.upts.strftime('%m-%d-%y %H:%M:%S') if self.upts  else 'None'),
            (' ' + StringUtils.toUnicode(modelInfo)) if modelInfo else '')


