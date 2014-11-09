# ModelProperty.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

#___________________________________________________________________________________________________ ModelProperty
class ModelProperty(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, name):
        self._name = name

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ __name__
    def __name__(self):
        """Used by SQLAlchemy during the mapping process."""
        return self._name
