# ApiRouterView.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from pyramid.renderers import render_to_response

from pyaid.ArgsUtils import ArgsUtils
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
        """ Creates a new DataViewRouter instance.
            @param rootPackage - The root package in which the router will import views. By default
                the module will look in same package as the router class. Packages can be absolute,
                vmi.pyramid...., or relative to the current package.
        """
        super(ApiRouterView, self).__init__(request, **kwargs)

        # Determine root package
        if not rootPackage:
            self._root = '.'.join(self.__module__.split('.')[:-1])
        else:
            self._root = rootPackage

        # Use root package and category to specify import
        self._package           = self._root + '.' + self.category + 'Controller'
        self._signature         = self.getArg('sg', '')
        self._args              = self.getArg('args', None)
        self._incomingTimestamp = None


#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiID
    @property
    def apiID(self):
        return self.category + '-' + self.action

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
                self.getApiArg('__tcode__', u''),
                self._request.ziggurat.timecodeOffset)
        return self._incomingTimestamp

#___________________________________________________________________________________________________ GS: signature
    @property
    def signature(self):
        return self._signature

#___________________________________________________________________________________________________ GS: args
    @property
    def args(self):
        return self._args

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getApiArg
    def getApiArg(self, name, default =None, argType =None):
        """ Returns the value of the specified argument if it exists, or the default value if it
            does not.

            @@@param name:string
                Argument name to retrieve.
            @@@param default:mixed
                default value returned if the argument does not exist.
            @@@return mixed
        """
        if argType is not None:
            return ArgsUtils.getAs(name, default, self._args, argType)
        return ArgsUtils.get(name, default, self._args)

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '[%s: %s.%s]' % (
            str(self.__class__.__name__),
            str(self.category),
            str(self.action))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createResponse
    def _createResponse(self):
        super(ApiRouterView, self)._createResponse()

        try:
            # Import the View Assembly Class (VAC)
            res    = __import__(self._package, globals(), locals(), [self.category])
            Source = getattr(res, self.category)

            # Execute the View Assembly Method (VAM)
            result = getattr(Source, self.action)(self)
            if isinstance(result, ViewResponse):
                self._explicitResponse = result

            # If an explicit response is set render that instead:
            if self._explicitResponse:
                self._createExplicitResponse()
                return

        except Exception, err:
            self._logger.writeError([
                u'API ROUTING FAILURE: ' + unicode(self.__module__.split('.')[-1]),
                u'Package: ' + unicode(self._package),
                u'Category: ' + unicode(self.category),
                u'ID: ' + unicode(self.action)
            ], err)
            self._explicitResponse = ViewResponse(
                'ERROR:' + self.apiID,
                'Invalid Request',
                'This unknown or invalid request was aborted'
            )
            self._createExplicitResponse()
            return

        self._response['__tcode__'] = self.outgoingTimecode
        self._request.response_content_type = 'application/javascript'
        self._response = render_to_response('json', self._response, self._request)

