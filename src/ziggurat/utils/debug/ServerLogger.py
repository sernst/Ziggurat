# ServerLogger.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils
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
        self._app = ArgsUtils.extract('app', None, kwargs)
        if self._app is None:
            super(ServerLogger, self).__init__(name, printOut=True, **kwargs)
            return

        super(ServerLogger, self).__init__(
            name=name,
            printOut=True,
            logFolder=self._app.logPath,
            **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getPrefix
    def getPrefix(self, *args, **kwargs):
        if self._locationPrefix:
            item = self.getStackData()[-1]
            loc  = u' -> %s #%s]' % (item['file'], unicode(item['line']))
        else:
            loc = u']'

        if self._app and self._app.pyramidApp:
            wsgi     = self._app.environ
            initials = self._INITIALS_RX.sub('', wsgi.get('REMOTE_USER', ''))
            if initials:
                initials += u' | '

            domainName  = wsgi.get('SERVER_NAME', '')
            uriPath     = wsgi.get('REQUEST_URI', wsgi.get('HTTP_REQUEST_URI', ''))
            info        = u' <' + initials + domainName + uriPath + u'>'
        else:
            info = u''

        threadID = ThreadUtils.getCurrentID()
        return unicode(
            self._getTime().strftime('[%a %H:%M <%S.%f>') + u'<' + threadID + u'>' + info + loc)
