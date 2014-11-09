# SqlAlchemyResult.py
# (C) 2012-2013
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import time

from sqlalchemy.orm import exc

# AS NEEDED: from ziggurat.sqlalchemy.meta.AbstractModelsMeta import AbstractModelsMeta

#___________________________________________________________________________________________________ SqlAlchemyResult
class SqlAlchemyResult(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, modelClass, query, lock =False):
        self._modelClass = modelClass
        self._query      = query
        self._lock       = lock

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ count
    def count(self):
        return self._getResult(self._query.count)

#___________________________________________________________________________________________________ scalar
    def scalar(self):
        try:
            return self._getResult(self._query.scalar, exc.MultipleResultsFound)
        except Exception:
            return None

#___________________________________________________________________________________________________ one
    def one(self):
        try:
            return self._getResult(self._query.one, (exc.NoResultFound, exc.MultipleResultsFound))
        except Exception:
            return None

#___________________________________________________________________________________________________ first
    def first(self):
        return self._getResult(self._query.first)

#___________________________________________________________________________________________________ all
    def all(self):
        return self._getResult(self._query.all)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getResult
    def _getResult(self, function, passErrors =None):
        # SLAVE models are read-only, so make sure to lock the table in read mode only to prevent
        # lock collisions. MASTER models query for updates, so use the stronger update lockmode
        # to prevent read collisions.

        # 3 iterations is significant to SQLAlchemy.
        for i in range(3):
            try:
                result = function()
                if self._lock:
                    if self._modelClass.IS_MASTER:
                        result = result.with_lockmode("update")
                    else:
                        result = result.with_lockmode("read")
                return result
            except passErrors as err:
                raise err
            except Exception as err:
                from ziggurat.sqlalchemy.meta.AbstractModelsMeta import AbstractModelsMeta
                AbstractModelsMeta.logger.writeError(
                    '[%s] BAD CURSOR ACTION: %s' % (str(i), str(function)), err)

        # Sleeps away collisions
        time.sleep(1)

        try:
            result = function()
            if self._lock:
                if self._modelClass.IS_MASTER:
                    result = result.with_lockmode("update")
                else:
                    result = result.with_lockmode("read")
            return result
        except passErrors as err:
            raise err
        except Exception as err:
            from ziggurat.sqlalchemy.meta.AbstractModelsMeta import AbstractModelsMeta
            AbstractModelsMeta.logger.writeError('FAILED CURSOR ACTION: %s'% str(function), err)

        return None

