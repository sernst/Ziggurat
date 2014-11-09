# ViewRedirect.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.ArgsUtils import ArgsUtils

from ziggurat.view.response.ViewResponse import ViewResponse

#___________________________________________________________________________________________________ ViewRedirect
class ViewRedirect(ViewResponse):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, id, url, **kwargs):
        """Creates a new instance of ViewRedirect."""
        self.url          = url
        self.windowTarget = ArgsUtils.extract('windowTarget', '_blank', kwargs)
        super(ViewRedirect, self).__init__(id=id, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _toDictImpl
    def _toDictImpl(self, data, view):
        data['url']    = self.url
        data['target'] = self.windowTarget
        return data

