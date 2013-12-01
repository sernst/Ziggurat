# ZigguratModelsBase.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import orm

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
    @orm.reconstructor
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

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        modelInfo = self._getReprString()
        return u'<%s[%s] cts[%s] upts[%s]%s>' % (
            self.__class__.__name__,
            unicode(self.i),
            unicode(self.cts.strftime('%m-%d-%y %H:%M:%S') if self.cts else u'None'),
            unicode(self.upts.strftime('%m-%d-%y %H:%M:%S') if self.upts  else u'None'),
            (u' ' + unicode(modelInfo)) if modelInfo else u'')

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

