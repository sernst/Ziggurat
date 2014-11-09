# ZigguratDataView.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division
from pyaid.string.StringUtils import StringUtils

from pyramid.renderers import render_to_response
from pyramid.response import Response

from ziggurat.view.ZigguratBaseView import ZigguratBaseView

#___________________________________________________________________________________________________ ZigguratDataView
class ZigguratDataView(ZigguratBaseView):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, request, **kwargs):
        """Creates a new instance of ZigguratDataView."""
        super(ZigguratDataView, self).__init__(request, **kwargs)
        self._request.response_content_type = 'application/javascript'
        self._response = dict()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ __call__
    def __call__(self):
        super(ZigguratDataView, self).__call__()
        if isinstance(self._response, Response) or StringUtils.isStringType(self._response):
            return self._response

        return render_to_response('json', self._response, self._request)

#___________________________________________________________________________________________________ _createExplicitResponse
    def _createExplicitResponse(self, responseOverride =None):
        """Doc..."""
        r = responseOverride if responseOverride else self._explicitResponse
        self._response = render_to_response('json', r.toDict(self), self._request)



