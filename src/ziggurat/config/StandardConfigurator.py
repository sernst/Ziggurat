# StandardConfigurator.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import re

from pyaid.string.StringUtils import StringUtils
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
        'pyramid.includes':'pyramid_tm',
        'mako.input_encoding':'utf-8' }

#___________________________________________________________________________________________________ __init__
    def __init__(self, app, rootViewPackage =None, **kwargs):
        """Creates a new instance of StandardConfigurator."""
        super(StandardConfigurator, self).__init__(**kwargs)

        self._isPopulated     = False
        self._app             = app
        self._rootViewPackage = rootViewPackage
        self.add_request_method(
            self._getMyAppRequestProperty,
            StringUtils.toStrStr('ziggurat'), reify=True)

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
        return FileUtils.createPath(self._app.rootPath, 'operations', 'mako', isDir=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ populateConfigs
    def populateConfigs(self):
        if self._isPopulated:
            return

        self._isPopulated = True
        self._populateRoutes()

        settings = dict(self._DEFAULT_SETTINGS.items())

        p = self.makoRootTemplatePath
        if p:
            settings['mako.directories'] = p

            p = self.makoModuleDirectory
            if p:
                settings['mako.module_directory'] = p

        self._populateSettings(settings)
        self.add_settings(settings)

#___________________________________________________________________________________________________ addRouteItem
    def addRouteItem(self, name, pattern, className, renderer =None, package =None, subpackage =None):
        """Adds a route to the registry."""

        # Adds optional end slash argument to URLs that don't enforce an end slash themselves
        if not pattern.endswith('/'):
            if self._REST_PATTERN.search(pattern) is None:
                pattern += '{endSlash:[/]*}'

        importDef = [className, className]
        if subpackage:
            importDef.insert(0, subpackage)
        importDef.insert(0, package if package else self.rootViewPackage)

        self.add_route(name, pattern)
        self.add_view('.'.join(importDef), route_name=name, renderer=renderer)

#___________________________________________________________________________________________________ addStaticRouteItem
    def addStaticRouteItem(self, name, path):
        self.add_static_view(name=name, path=path)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getMyAppRequestProperty
    def _getMyAppRequestProperty(self, request):
        return self._app

#___________________________________________________________________________________________________ _populateSettings
    def _populateSettings(self, settings):
        pass

#___________________________________________________________________________________________________ _populateRoutes
    def _populateRoutes(self):
        """Doc..."""
        pass

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
