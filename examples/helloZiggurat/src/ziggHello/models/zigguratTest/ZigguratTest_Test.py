# ZigguratTest_Test.py
# (C)2013
# Scott Ernst

from sqlalchemy import Column
from sqlalchemy import UnicodeText

from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ ZigguratTest_Test
class ZigguratTest_Test(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _info = Column(UnicodeText, default=u'')

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: infoData
    @property
    def infoData(self):
        if self.info:
            return JSON.fromString(self.info)
        return dict()
    @infoData.setter
    def infoData(self, value):
        self.info = JSON.asString(value) if value else u''
