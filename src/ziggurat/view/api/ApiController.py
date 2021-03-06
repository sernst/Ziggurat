# ApiController.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

#___________________________________________________________________________________________________ ApiController
class ApiController(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, router):
        """Creates a new instance of ApiController."""
        self._router  = router

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: router
    @property
    def router(self):
        return self._router

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        return self.router.response

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        return self._router.logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ fetchApiZarg
    def _fetchApiZarg(self, name, default =None, zargType =None):
        """fetchApiZarg doc..."""
        return self.router.fetchApiZarg(name, default=default, zargType=zargType)

#___________________________________________________________________________________________________ appendResponse
    def _appendResponse(self, **kwargs):
        """addToResponse doc..."""
        return self.router.addToResponse(**kwargs)

#___________________________________________________________________________________________________ authorizeApiAction
    def _authorizeApiAction(self, actionMethod):
        return True

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, actionMethod):
        """__call__ doc..."""
        return self._authorizeApiAction(actionMethod)

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
