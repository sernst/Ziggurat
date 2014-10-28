# ServerLogger.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.threading.ThreadUtils import ThreadUtils

# AS NEEDED: from ziggurat.ZigguratApplication import ZigguratApplication

#___________________________________________________________________________________________________ ServerLogger
from pyaid.time.TimeUtils import TimeUtils


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
            initials = self._INITIALS_RX.sub('', ArgsUtils.get('REMOTE_USER', '', wsgi))
            if initials:
                initials += u' | '

            domainName  = ArgsUtils.get('SERVER_NAME', '', wsgi)
            uriPath = ArgsUtils.get(
                'REQUEST_URI',
                ArgsUtils.get('HTTP_REQUEST_URI', '', wsgi), wsgi)

            info = u' <' + initials + domainName + uriPath + u'>'
        else:
            info = u''

        threadID = ThreadUtils.getCurrentID()
        return unicode(
            TimeUtils.toFormat('[%a %H:%M <%S.%f>') + u'<' + threadID + u'>' + info + loc)
