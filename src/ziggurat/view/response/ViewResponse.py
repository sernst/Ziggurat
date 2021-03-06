# ViewResponse.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.ArgsUtils import ArgsUtils

#___________________________________________________________________________________________________ ViewResponse
class ViewResponse(object):
    """A class for reusable API response formats."""

#===================================================================================================
#                                                                                       C L A S S

    DEFAULT_KIND = 'MESSAGE'

#___________________________________________________________________________________________________ __init__
    def __init__(self, ident, label =None, message =None, **kwargs):
        """Creates a new instance of ViewResponse."""
        self._id      = ident
        self._label   = label
        self._message = message
        self._kind    = ArgsUtils.get('kind', self.DEFAULT_KIND, kwargs)
        self._allowCaching = ArgsUtils.get('allowCaching', False, kwargs)
        self._data = ArgsUtils.getAsDict('data', kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: kind
    @property
    def kind(self):
        return self._kind

#___________________________________________________________________________________________________ GS: id
    @property
    def id(self):
        return self._id

#___________________________________________________________________________________________________ GS: data
    @property
    def data(self):
        return self._data

#___________________________________________________________________________________________________ GS: label
    @property
    def label(self):
        return self._label

#___________________________________________________________________________________________________ GS: message
    @property
    def message(self):
        return self._message

#___________________________________________________________________________________________________ GS: allowCaching
    @property
    def allowCaching(self):
        return self._allowCaching

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ toDict
    def toDict(self, view):
        """Converts the object to a dictionary for rendering to a JSON response."""
        return self._toDictImpl(dict(
            __kind__=self.kind,
            id=self.id,
            data=self.data,
            label=self.label,
            message=self.message,
            timecode=view.outgoingTimecode), view)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _toDictImpl
    def _toDictImpl(self, data, view):
        return data

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
