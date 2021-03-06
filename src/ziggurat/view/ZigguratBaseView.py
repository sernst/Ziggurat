# ZigguratBaseView.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from __future__ import print_function, absolute_import, unicode_literals, division
from pyaid.string.StringUtils import StringUtils

import transaction
from pyaid.dict.DictUtils import DictUtils
from pyramid.httpexceptions import HTTPFound, HTTPServerError
from pyaid.ArgsUtils import ArgsUtils
from pyaid.time.TimeUtils import TimeUtils

from ziggurat.view.response.ViewResponse import ViewResponse
from ziggurat.sqlalchemy.meta.ConcreteModelsMeta import ConcreteModelsMeta


#___________________________________________________________________________________________________ ZigguratBaseView
class ZigguratBaseView(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


#___________________________________________________________________________________________________ __init__
    def __init__(self, request, **kwargs):
        """Creates a new instance of ZigguratBaseView."""
        self._request            = request
        self._response           = None
        self._outgoingTimecode   = TimeUtils.getNowTimecode(request.ziggurat.timecodeOffset)
        self._logger             = ArgsUtils.get('logger', self._request.ziggurat.logger, kwargs)
        self._expires            = ArgsUtils.get('expires', 0, kwargs)
        self._lastModified       = None
        self._cacheControlPublic = False
        self._etag               = None
        self._explicitResponse   = None

        # Event called when the response object is ready.
        self._request.add_response_callback(self._handleResponseReady)
        self._request.add_finished_callback(self._handleFinishedCallback)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: ziggurat
    @property
    def ziggurat(self):
        return self._request.ziggurat

#___________________________________________________________________________________________________ GS: request
    @property
    def request(self):
        """The Pyramid request object for this view."""
        return self._request

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        return self._response
    @response.setter
    def response(self, value):
        self._response = value

#___________________________________________________________________________________________________ GS: isSecure
    @property
    def isSecure(self):
        key = 'HTTP_X_FORWARDED_PROTO'
        if key in self._request.environ:
            return self._request.environ[key] == 'https'

        key = 'wsgi.url_scheme'
        if key in self._request.environ:
            return self._request[key] == 'https'

        return False

#___________________________________________________________________________________________________ GS: expires
    @property
    def expires(self):
        return self._expires
    @expires.setter
    def expires(self, value):
        self._expires = value if value else 0

#___________________________________________________________________________________________________ GS: outgoingTimecode
    @property
    def outgoingTimecode(self):
        return self._outgoingTimecode

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        return self._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getArg
    def getArg(self, name, defaultValue =None):
        """ Returns the value of the specified argument if it exists, or the default value"""
        if name in self._request.POST:
            return self._request.POST[name]

        if name in self._request.GET:
            return self._request.GET[name]

        return defaultValue

#___________________________________________________________________________________________________ __call__
    def __call__(self):
        try:
            result = self._createResponse()

            if isinstance(result, ViewResponse):
                self._createExplicitResponse(result)
        except Exception as err:
            self._logger.writeError('FAILED [createResponse]', err)

        return self._response

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderRedirect
    def _renderRedirect(self, redirectURL):
        self._response = HTTPFound(location=redirectURL)

#___________________________________________________________________________________________________ _renderSecureRedirect
    def _renderSecureRedirect(self):
        if self.isSecure:
            return False

        self._renderRedirect('https' + self._request.url[4:])
        return True

#___________________________________________________________________________________________________ _createExplicitResponse
    def _createExplicitResponse(self, responseOverride =None):
        """Doc..."""
        if responseOverride is None:
            self._response = HTTPServerError()
            return

        self._response = HTTPServerError(responseOverride.label, None, responseOverride.message)

#___________________________________________________________________________________________________ _createResponse
    def _createResponse(self):
        """Doc..."""
        pass

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleResponseReady
    def _handleResponseReady(self, request, response):
        """Event handler for the response object being ready for use."""

        if self._cacheControlPublic:
            response.cache_control = 'public'

        #-------------------------------------------------------------------------------------------
        # Cache Expiration: Set the caching values according to the _expires property
        rep = self._explicitResponse
        if rep is None or (isinstance(rep, ViewResponse) and rep.allowCaching):
            response.cache_control.max_age = self.expires if not self.expires is None else 0
        else:
            response.cache_control.max_age = 0

        #-------------------------------------------------------------------------------------------
        # Cache Validators
        if self._etag is not None:
            response.etag = StringUtils.toUnicode(self._etag)

        if self._lastModified is not None:
            response.last_modified = self._lastModified

        # If required encode the response headers as strings to prevent unicode errors. This is
        # necessary for certain WSGI server applications, e.g. flup.
        if self.ziggurat.strEncodeEnviron:
            for n, v in DictUtils.iter(response.headers):
                if StringUtils.isStringType(v):
                    response.headers[n] = StringUtils.toStr2(v)

        # Clean up per-thread sessions.
        ConcreteModelsMeta.cleanupSessions()

#___________________________________________________________________________________________________ _handleFinishedCallback
    def _handleFinishedCallback(self, request):
        """commit or abort the transaction associated with request"""
        if request.exception is not None:
            transaction.abort()
        else:
            transaction.commit()

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
