# ApiRouterView.py
# (C)2011-2014
# Scott Ernst and Eric David Wills

import inspect

from pyaid.ArgsUtils import ArgsUtils
from pyaid.ClassUtils import ClassUtils
from pyaid.json.JSON import JSON
from pyaid.time.TimeUtils import TimeUtils

from ziggurat.view.ZigguratDataView import ZigguratDataView
from ziggurat.view.response.ViewResponse import ViewResponse

#___________________________________________________________________________________________________ ApiRouterView
class ApiRouterView(ZigguratDataView):
    """Base class for request routing."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, request, rootPackage =None, **kwargs):
        """ Creates a new ApiRouterView instance.
            @param rootPackage - The root package in which the router will import views. By default
                the module will look in same package as the router class. Packages can be absolute,
                or relative to the current package. """

        super(ApiRouterView, self).__init__(request, **kwargs)

        # Determine root package
        self._root = rootPackage if rootPackage else ClassUtils.getModulePackage(self.__class__, 1)

        zargs = self.getArg('zargs', None)
        if zargs:
            try:
                self._zargs = JSON.fromString(zargs)
            except Exception, err:
                self._zargs = None
        else:
            self._zargs = None
        self._signature = self.getArg('sig', '')

        self._incomingTimestamp = None
        self._outgoingTimestamp = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiID
    @property
    def apiID(self):
        return self.category + u'-' + self.action

#___________________________________________________________________________________________________ GS: requestCategory
    @property
    def category(self):
        try:
            return self._request.matchdict['category']
        except Exception, err:
            return None

#___________________________________________________________________________________________________ GS: action
    @property
    def action(self):
        try:
            reqID = self._request.matchdict['action']
            if reqID.startswith('_'):
                return None
            return reqID
        except Exception, err:
            return None

#___________________________________________________________________________________________________ GS: incomingTimecode
    @property
    def incomingTimecode(self):
        if not self._incomingTimestamp:
            self._incomingTimestamp = TimeUtils.timecodeToDatetime(
                self.fetchApiZarg('__tcode__', u''),
                self._request.ziggurat.timecodeOffset)
        return self._incomingTimestamp

#___________________________________________________________________________________________________ GS: signature
    @property
    def signature(self):
        return self._signature

#___________________________________________________________________________________________________ GS: zargs
    @property
    def zargs(self):
        return self._zargs

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addToResponse
    def addToResponse(self, **kwargs):
        for n,v in kwargs.iteritems():
            self._response[n] = v

#___________________________________________________________________________________________________ fetchApiZarg
    def fetchApiZarg(self, name, default =None, zargType =None):
        """ Returns the value of the specified argument if it exists, or the default value if it
            does not.

            @param name:string
                Argument name to retrieve.
            @param default:mixed
                default value returned if the argument does not exist.
            @return mixed """

        if not self._zargs:
            return None

        if zargType is not None:
            return ArgsUtils.getAs(name, default, self._zargs, zargType)
        return ArgsUtils.get(name, default, self._zargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createResponse
    def _createResponse(self):
        super(ApiRouterView, self)._createResponse()

        controllerClass = self.category + 'Controller'
        package         = self._root + '.' + controllerClass

        try:
            # Filter illegal actions
            if not self.category or not self.action or self.action.startswith('_'):
                retuls = self._createErrorResponse(
                    ident=u'ERROR:' + self.apiID,
                    label=u'Invalid Action',
                    message=u'The specified action is invalid')

            # Import the Controller class
            res        = __import__(package, globals(), locals(), [controllerClass])
            controller = getattr(res, controllerClass)(self)

            # If authorized execute the action method, otherwise create a invalid request response
            method = getattr(controller, self.action)
            result = None
            if inspect.ismethod(method) and controller(method):
                result = method()
            else:
                if not self._explicitResponse and not isinstance(result, ViewResponse):
                    result = self._createErrorResponse(
                        ident=u'ERROR:' + self.apiID,
                        label=u'Unauthorized Request',
                        message=u'This unauthorized request was rejected')

            if isinstance(result, ViewResponse):
                self._explicitResponse = result

            # If an explicit response is set render that instead:
            if self._explicitResponse:
                self._createExplicitResponse()
                return

        except Exception, err:
            try:
                zargs = unicode(self.zargs)
            except Exception, err:
                zargs = u'[Unable to display as unicode string]'

            self._logger.writeError([
                u'API ROUTING FAILURE: ' + unicode(self.__module__.split('.')[-1]),
                u'Package: ' + unicode(package),
                u'Controller: ' + unicode(controllerClass),
                u'Category: ' + unicode(self.category),
                u'Zargs: ' + zargs,
                u'Action: ' + unicode(self.action) ], err)

            self._explicitResponse = self._createErrorResponse(
                ident=u'ERROR:' + self.apiID,
                label=u'Invalid Request',
                message=u'This unknown or invalid request was aborted')
            self._createExplicitResponse()
            return

        self._response['__ztime__'] = self.outgoingTimecode

#___________________________________________________________________________________________________ _createErrorResponse
    def _createErrorResponse(self, ident, **kwargs):
        """_createErrorResponse doc..."""
        return ViewResponse(ident, **kwargs)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '[%s: %s.%s]' % (str(self.__class__.__name__), str(self.category), str(self.action))
