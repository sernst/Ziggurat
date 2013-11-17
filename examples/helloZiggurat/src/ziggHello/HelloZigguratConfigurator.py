# HelloZigguratConfigurator.py
# (C)2013
# Scott Ernst

from ziggurat.config.StandardConfigurator import StandardConfigurator

#___________________________________________________________________________________________________ HelloZigguratConfigurator
class HelloZigguratConfigurator(StandardConfigurator):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, app):
        super(HelloZigguratConfigurator, self).__init__(app, rootViewPackage='ziggHello.views')

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _populateRoutes
    def _populateRoutes(self):
        self.addRouteItem(
            name='home',
            pattern='/',
            className='HelloZigguratHomeView')

        self.addRouteItem(
            name='data',
            pattern='/data',
            className='HelloZigguratDataView')

        self.addRouteItem(
            name='api',
            pattern='/api',
            className='HelloZigguratApiView',
            subpackage='api')
