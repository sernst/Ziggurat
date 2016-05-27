# ServerLogger.py
# (C)2012-2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import re

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.string.StringUtils import StringUtils
from pyaid.threading.ThreadUtils import ThreadUtils
from pyaid.time.TimeUtils import TimeUtils

# AS NEEDED: from ziggurat.ZigguratApplication import ZigguratApplication

#___________________________________________________________________________________________________ ServerLogger
class ServerLogger(Logger):
    """A class for logging information in the operations/logs directory."""

#===================================================================================================
#                                                                                       C L A S S

    _INITIALS_RX = re.compile('[^A-Z]+')

#___________________________________________________________________________________________________ __init__
    def __init__(self, name =None, app =None, **kwargs):
        """Initializes settings."""
        self._app = app

        ArgsUtils.addIfMissing('headerless', False, kwargs)
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
            loc  = ' -> %s #%s]' % (item['file'], StringUtils.toUnicode(item['line']))
        else:
            loc = ']'

        if self._app and self._app.pyramidApp:
            wsgi     = self._app.environ
            initials = self._INITIALS_RX.sub('', ArgsUtils.get('REMOTE_USER', '', wsgi))
            if initials:
                initials += ' | '

            domainName  = ArgsUtils.get('SERVER_NAME', '', wsgi)
            uriPath = ArgsUtils.get(
                'REQUEST_URI',
                ArgsUtils.get('HTTP_REQUEST_URI', '', wsgi), wsgi)

            info = ' <' + initials + domainName + uriPath + '>'
        else:
            info = ''

        threadID = ThreadUtils.getCurrentID()
        return StringUtils.toUnicode(
            TimeUtils.toFormat('[%a %H:%M <%S.%f>') + '<' + threadID + '>' + info + loc)
