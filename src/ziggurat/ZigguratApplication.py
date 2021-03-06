# ZigguratApplication.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.list.ListUtils import ListUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.threading.ThreadUtils import ThreadUtils

from ziggurat.config.StandardConfigurator import StandardConfigurator
from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils
from ziggurat.utils.debug.ServerLogger import ServerLogger

#___________________________________________________________________________________________________ ZigguratApplication
class ZigguratApplication(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _TIMECODE_OFFSET = 1293868800

#___________________________________________________________________________________________________ __init__
    def __init__(
            self, appFilePath =None, appName =None, rootPath =None, configuratorClass =None,
            logPath =None, **kwargs
    ):
        """Creates a new instance of ZigguratApplication."""
        ZigguratModelUtils.isWebEnvironment = True

        self.strEncodeEnviron = ArgsUtils.get('strEncodeEnviron', False, kwargs)

        self._name              = appName
        self._logPath           = logPath
        self._environ           = None
        self._startResponse     = None
        self._logger            = None
        self._configs           = None
        self._pyramidApp        = None
        self._appFilePath       = appFilePath
        self._configuratorClass = configuratorClass
        self._rootPath          = rootPath

        if self._rootPath is None:
            self._rootPath = self.rootPath

        if not os.path.exists(self.logPath):
            os.makedirs(self.logPath)
            self.logger.write('WARNING: Created missing application path: %s' % self._rootPath)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: timecodeOffset
    @property
    def timecodeOffset(self):
        return self._TIMECODE_OFFSET

#___________________________________________________________________________________________________ GS: appName
    @property
    def appName(self):
        return self.__class__.__name__ if self._name is None else self._name

#___________________________________________________________________________________________________ GS: rootPath
    @property
    def rootPath(self):
        if self._rootPath:
            return self._rootPath

        if self._appFilePath:
            return FileUtils.getDirectoryOf(self._appFilePath)

        return FileUtils.createPath(os.path.expanduser('~'), self.appName, isDir=True)

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
        if self._logPath:
            return self._logPath
        return FileUtils.createPath(self.rootPath, 'operations', 'logs', isDir=True)

#___________________________________________________________________________________________________ GS: configuratorClass
    @property
    def configuratorClass(self):
        if self._configuratorClass is None:
            return StandardConfigurator
        return self._configuratorClass

#___________________________________________________________________________________________________ GS: configurator
    @property
    def configurator(self):
        if self._configs is None:
            self._configs = self.configuratorClass(app=self, settings=self._getConfigSettings())
        return self._configs

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        if self._logger is None:
            self._logger = ServerLogger(self, app=self)
        return self._logger

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createApp
    def _createApp(self, environ, start_response):
        """Doc..."""

        self._environ       = environ
        self._startResponse = start_response

        try:
            self._initialize()
        except Exception as err:
            self.logger.writeError([
                'ERROR: Ziggurat App Initialization Failed',
                'ENVIRON: %s' % environ,
                'RESPONSE: %s' % start_response ], err)
            raise

        try:
            configs = self.configurator
            configs.populateConfigs()
        except Exception as err:
            self.logger.writeError('ERROR: Configurator Initialization Failed', err)
            raise

        try:
            self._pyramidApp = configs.make_wsgi_app()
        except Exception as err:
            self.logger.writeError('ERROR: Pyramid Application Creation Failed', err)
            raise

        # Forces values to be strings instead of Unicode values when specified
        if self.strEncodeEnviron:
            for key, value in DictUtils.iter(self._environ):
                if not isinstance(value, str):
                    self._environ[key] = StringUtils.toUnicode(value).encode()

        try:
            return self._pyramidApp(self._environ, self._startResponse)
        except Exception as err:
            self.logger.writeError([
                'ERROR: WSGI Application Creation Failed',
                'CONFIGURATOR: %s' % configs], err)
            raise

#___________________________________________________________________________________________________ _getConfigSettings
    def _getConfigSettings(self):
        """ Override to pass values to the settings object of the Configurator. """
        return dict()

#___________________________________________________________________________________________________ _initialize
    def _initialize(self):
        """ Called after the application has been created with its environment and start response
            values but before the Configurator is created and the app processed. Override this
            method to make adjustments to the application based in request settings that will
            affect the creation of the Configurator. """
        pass

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        try:
            return self._createApp(
                ArgsUtils.getAsDict('environ', kwargs, args, 0),
                ArgsUtils.get('start_response', None, kwargs, args, 1) )
        except Exception as err:
            self.logger.writeError([
                'ERROR: Application Creation Failed',
                'ARGS: %s' % ListUtils.prettyPrint(args),
                'KWARGS: %s' % DictUtils.prettyPrint(kwargs) ], err)
            raise

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

