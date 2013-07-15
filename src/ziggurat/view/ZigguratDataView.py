# ZigguratDataView.py
# (C)2013
# Scott Ernst

from pyramid.renderers import render_to_response

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
        self._response          = dict()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createExplicitResponse
    def _createExplicitResponse(self, responseOverride =None):
        """Doc..."""
        r = responseOverride if responseOverride else self._explicitResponse
        self._response = render_to_response('json', r.toDict(self), self._request)



