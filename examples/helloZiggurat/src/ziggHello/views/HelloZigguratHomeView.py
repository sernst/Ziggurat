# HelloZigguratHomeView.py
# (C)2013
# Scott Ernst

from ziggurat.view.ZigguratDisplayView import ZigguratDisplayView

#___________________________________________________________________________________________________ HelloZigguratHomeView
class HelloZigguratHomeView(ZigguratDisplayView):
    """ An example view class for the Hello Ziggurat application. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, request, **kwargs):
        """Creates a new instance of HelloZigguratHomeView."""
        super(HelloZigguratHomeView, self).__init__(
            request=request,
            template='hello.mako',
            **kwargs)


