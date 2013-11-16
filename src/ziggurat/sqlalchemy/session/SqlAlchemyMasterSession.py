# SqlAlchemyMasterSession.py
# (C) 2012-2013
# Eric David Wills and Scott Ernst

from ziggurat.sqlalchemy.session.SqlAlchemySlaveSession import SqlAlchemySlaveSession
# AS NEEDED: from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils

#___________________________________________________________________________________________________ SqlAlchemyMasterSession
class SqlAlchemyMasterSession(SqlAlchemySlaveSession):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, sessionClass):
        SqlAlchemySlaveSession.__init__(self, sessionClass)
        self._committedSessions = []

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, model):
        self._getSession().add(model)

#___________________________________________________________________________________________________ remove
    def remove(self, model):
        self._getSession().delete(model)

#___________________________________________________________________________________________________ flush
    def flush(self):
        self._getSession().flush()

#___________________________________________________________________________________________________ commit
    def commit(self, force =False):
        from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils
        if force or not ZigguratModelUtils.isWebEnvironment:
            session = self._getSession()
            session.commit()

            self._committedSessions.append(session)
            self.cleanup()

#___________________________________________________________________________________________________ close
    def close(self):
        self._getSession().close()

