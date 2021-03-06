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
    def __init__(self, app, **kwargs):
        super(HelloZigguratConfigurator, self).__init__(
            app=app,
            rootViewPackage='ziggHello.views',
            **kwargs)

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
            pattern='/api/{category}/{action}',
            className='HelloZigguratApiView',
            subpackage='api')
