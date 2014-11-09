# SqlAlchemySlaveSession.py
# (C) 2012-2013
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.threading.ThreadUtils import ThreadUtils

#___________________________________________________________________________________________________ SqlAlchemySlaveSession
class SqlAlchemySlaveSession(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, sessionClass):
        self._sessionClass = sessionClass
        self._sessions     = dict()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createQuery
    def createQuery(self, *args):
        return self._getSession().query(*args)

#___________________________________________________________________________________________________ cleanup
    def cleanup(self):
        tid = ThreadUtils.getCurrentID()
        if tid in self._sessions:
            del self._sessions[tid]

#___________________________________________________________________________________________________ getRawSession
    def getRawSession(self):
        return self._getSession()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSession
    def _getSession(self):
        # One session per thread
        tid = ThreadUtils.getCurrentID()
        if tid not in self._sessions:
            self._sessions[tid] = self._sessionClass()
        else:
            session = self._sessions[tid]
            if not session.is_active or not session.transaction.is_active:
                self._sessions[tid] = self._sessionClass()
        return self._sessions[tid]

