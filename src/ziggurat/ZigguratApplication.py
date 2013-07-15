# ZigguratApplication.py
# (C)2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.threading.ThreadUtils import ThreadUtils

from ziggurat.config.StandardConfigurator import StandardConfigurator
from ziggurat.utils.debug.ServerLogger import ServerLogger

#___________________________________________________________________________________________________ ZigguratApplication
class ZigguratApplication(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _TIMECODE_OFFSET = 1293868800

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of ZigguratApplication."""
        self._environ        = None
        self._startResponse  = None
        self._logger         = None
        self._configs        = None
        self._pyramidApp     = None

        rootPath = self.rootPath
        if rootPath is None:
            rootPath = FileUtils.createPath(os.path.expanduser('~'), self.appName, isDir=True)

        self._rootPath = FileUtils.cleanupPath(rootPath)
        if not os.path.exists(self._rootPath):
            os.makedirs(self._rootPath)
            self.logger.write(
                u'WARNING: Created missing application path: ' + unicode(self._rootPath))

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: timecodeOffset
    @property
    def timecodeOffset(self):
        return self._TIMECODE_OFFSET

#___________________________________________________________________________________________________ GS: appName
    @property
    def appName(self):
        return self.__class__.__name__

#___________________________________________________________________________________________________ GS: rootPath
    @property
    def rootPath(self):
        return self._rootPath

#___________________________________________________________________________________________________ GS: environ
    @property
    def environ(self):
        return self._environ

#___________________________________________________________________________________________________ GS: startResponse
    @property
    def startResponse(self):
        return self._startResponse

#___________________________________________________________________________________________________ GS: pyramidApp
    @property
    def pyramidApp(self):
        return self._pyramidApp

#___________________________________________________________________________________________________ GS: threadID
    @property
    def threadID(self):
        return ThreadUtils.getCurrentID()

#___________________________________________________________________________________________________ GS: logPath
    @property
    def logPath(self):
        return FileUtils.createPath(self.rootPath, 'operations', 'logs', isDir=True)

#___________________________________________________________________________________________________ GS: configurator
    @property
    def configurator(self):
        if self._configs is None:
            self._configs = StandardConfigurator(self, settings=self._getConfigSettings())
        return self._configs

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        if self._logger is None:
            self._logger = ServerLogger(self)
        return self._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createApp
    def createApp(self, environ, start_response):
        """Doc..."""
        self._environ       = environ
        self._startResponse = start_response
        self._initialize()

        configs = self.configurator
        configs.populateConfigs()
        self._pyramidApp = configs.make_wsgi_app()
        return self._pyramidApp

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getConfigSettings
    def _getConfigSettings(self):
        return None

#___________________________________________________________________________________________________ _initialize
    def _initialize(self):
        """Doc..."""
        pass

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        return self.createApp(
            ArgsUtils.getAsDict('environ', kwargs, args, 0),
            ArgsUtils.get('start_response', None, kwargs, args, 1))

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

