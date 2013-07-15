# ServerLogger.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.debug.Logger import Logger
from pyaid.threading.ThreadUtils import ThreadUtils

# AS NEEDED: from ziggurat.ZigguratApplication import ZigguratApplication

#___________________________________________________________________________________________________ ServerLogger
class ServerLogger(Logger):
    """A class for logging information in the operations/logs directory."""

#===================================================================================================
#                                                                                       C L A S S

    _INITIALS_RX = re.compile('[^A-Z]+')

#___________________________________________________________________________________________________ __init__
    def __init__(self, name =None, **kwargs):
        """Initializes settings."""
        super(ServerLogger, self).__init__(name, **kwargs)
        self._app = kwargs.get('app', None)
        if self._app is None:
            self._app = self._getApp()
            if self._app is None:
                return

        if self._logPath is None:
            self._logPath = self._app.logPath

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getPrefix
    def getPrefix(self, *args, **kwargs):
        if self._locationPrefix:
            item = self.getStackData()[-1]
            loc  = u' -> %s #%s]' % (item['file'], unicode(item['line']))
        else:
            loc = u']'

        if self._app:
            wsgi     = self._app.environ
            initials = ServerLogger._INITIALS_RX.sub('', wsgi.get('REMOTE_USER', ''))
            if initials:
                initials += u' | '

            domainName  = wsgi.get('SERVER_NAME', '')
            uriPath     = wsgi.get('REQUEST_URI', wsgi.get('HTTP_REQUEST_URI', ''))
            info        = u' <' + initials + domainName + uriPath + u'>'
        else:
            info = u''

        threadID = ThreadUtils.getCurrentID()
        return unicode(
            self._getTime().strftime('[%a %H:%M <%S.%f>') + u'<' + threadID + u'>' + info + loc
        )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getApp
    @classmethod
    def _getApp(cls):
        from ziggurat.ZigguratApplication import ZigguratApplication
        return ZigguratApplication.getMyApp()
