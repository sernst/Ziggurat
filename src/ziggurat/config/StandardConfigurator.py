# StandardConfigurator.py
# (C)2013
# Scott Ernst

import re

from pyramid.config import Configurator

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ StandardConfigurator
class StandardConfigurator(Configurator):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _REST_PATTERN = re.compile('\*[A-Za-z0-9]+$')

    _DEFAULT_SETTINGS = {
        'host':'0.0.0.0',
        'port':6543,
        'pyramid.reload_templates':True,
        'pyramid.debug_authorization':False,
        'pyramid.debug_notfound':False,
        'pyramid.debug_routematch':False,
        'pyramid.debug_templates':True,
        'pyramid.default_locale_name':'en',
        'pyramid.includes':'pyramid_tm'
    }

#___________________________________________________________________________________________________ __init__
    def __init__(self, app, rootViewPackage =None, **kwargs):
        """Creates a new instance of StandardConfigurator."""
        super(StandardConfigurator, self).__init__(**kwargs)

        self._app = app
        self._rootViewPackage = rootViewPackage
        self.add_request_method(self._getMyAppRequestProperty, 'ziggurat', reify=True)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: rootViewPackage
    @property
    def rootViewPackage(self):
        return self._rootViewPackage

#___________________________________________________________________________________________________ GS: makoRootTemplatePath
    @property
    def makoRootTemplatePath(self):
        return FileUtils.createPath(self._app.rootPath, 'templates', 'mako', isDir=True)

#___________________________________________________________________________________________________ GS: makoModuleDirectory
    @property
    def makoModuleDirectory(self):
        return FileUtils.createPath(self._app.self.rootPath, 'operations', 'mako', isDir=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ populateConfigs
    def populateConfigs(self):
        self._createRoutes()

        existingSettings = self.get_settings()
        settings = dict()
        for key,value in self._DEFAULT_SETTINGS:
            if key not in existingSettings:
                settings[key] = value

        p = self.makoRootTemplatePath
        if p:
            settings['mako.directories']    = p
            settings['mako.input_encoding'] = 'utf-8'
            p = self.makoModuleDirectory
            if p:
                settings['mako.module_directory'] = p

        self._populateSettings(existingSettings, settings)
        self.add_settings(settings)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _addRouteItem
    def _addRouteItem(self, name, uriPattern, className, renderer =None, package =None):
        """Adds a route to the registry."""

        # Adds optional end slash argument to URLs that don't enforce an end slash themselves
        if not uriPattern.endswith('/'):
            if self._REST_PATTERN.search(uriPattern) is None:
                uriPattern += '{endSlash:[/]*}'

        if package:
            package += '.' + className + '.' + className
        else:
            package = self._app.rootViewPackage + '.' + className + '.' + className

        self.add_route(name, uriPattern)
        self.add_view(package, route_name=name, renderer=renderer)

#___________________________________________________________________________________________________ _addStaticRouteItem
    def _addStaticRouteItem(self, name, path):
        self.add_static_view(name=name, path=path)

#___________________________________________________________________________________________________ _getMyAppRequestProperty
    def _getMyAppRequestProperty(self, request):
        return self._app

#___________________________________________________________________________________________________ _populateSettings
    def _populateSettings(self, existingSettings, newSettings):
        pass

#___________________________________________________________________________________________________ _populateRoutes
    def _populateRoutes(self):
        """Doc..."""
        return []

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__