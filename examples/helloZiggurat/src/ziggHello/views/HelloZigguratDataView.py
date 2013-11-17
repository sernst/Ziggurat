# HelloZigguratDataView.py
# (C)2013
# Scott Ernst

from ziggurat.view.ZigguratDataView import ZigguratDataView

#___________________________________________________________________________________________________ HelloZigguratDataView
class HelloZigguratDataView(ZigguratDataView):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, request, **kwargs):
        """Creates a new instance of HelloZigguratDataView."""
        super(HelloZigguratDataView, self).__init__(request, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _internalMethod
    def _createResponse(self):
        self._response = {
            'hello':'Ziggurat',
            'answer':42,
            'question':['The', 'ultimate', 'answer', 'to', 'life'] }
