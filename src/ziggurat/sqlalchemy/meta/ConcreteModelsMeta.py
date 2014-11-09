# ConcreteModelsMeta.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from pyaid.dict.DictUtils import DictUtils
from pyaid.string.StringUtils import StringUtils
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.pool import Pool

from ziggurat.sqlalchemy.ExternalKeyProperty import ExternalKeyProperty
from ziggurat.sqlalchemy.SqlAlchemyResult import SqlAlchemyResult
from ziggurat.sqlalchemy.meta.AbstractModelsMeta import AbstractModelsMeta
from ziggurat.sqlalchemy.session.SqlAlchemyMasterSession import SqlAlchemyMasterSession

# AS NEEDED: from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils
# AS NEEDED: from ziggurat.sqlalchemy.session.SqlAlchemySlaveSession import SqlAlchemySlaveSession

#___________________________________________________________________________________________________ ConcreteModelsMeta
class ConcreteModelsMeta(AbstractModelsMeta):

#===================================================================================================
#                                                                                       C L A S S

    # Stores existing engine and sessions for shared access
    _engines  = dict()
    _sessions = dict()

#___________________________________________________________________________________________________ __new__
    def __new__(cls, name, bases, attrs):
        from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils

        module      = attrs['__module__']
        package     = module[:module.rfind('.')]
        res         = __import__(package, globals(), locals(), ['DATABASE'])
        masterDbDef = getattr(res, 'MASTER_DATABASE_DEF', None)
        slaveDbDef  = getattr(res, 'SLAVE_DATABASE_DEF', None)
        adminDbDef  = getattr(res, 'ADMIN_DATABASE_DEF', None)
        databaseDef = getattr(res, 'DATABASE', None)

        isMaster = attrs['IS_MASTER']
        if isMaster and masterDbDef:
            if not ZigguratModelUtils.isWebEnvironment and adminDbDef:
                databaseDef = adminDbDef
            else:
                databaseDef = masterDbDef
        elif slaveDbDef:
            databaseDef = slaveDbDef

        if not databaseDef:
            raise Exception('ERROR: No database definition specified!')

        attrs['_DATABASE'] = databaseDef

        key       = ConcreteModelsMeta._getDatabaseKey(attrs['__module__'], isMaster)
        binding   = ConcreteModelsMeta._engines.get(key)
        if binding is None:
            engine = databaseDef.createEngine()

            if ZigguratModelUtils.isWebEnvironment:
                from zope.sqlalchemy import ZopeTransactionExtension
                sessionClass = scoped_session(sessionmaker(
                    bind=engine, extension=ZopeTransactionExtension()))
            else:
                sessionClass = scoped_session(sessionmaker(bind=engine))

            base = declarative_base()
            base.metadata.bind = engine
            base.metadata.create_all(engine)

            binding = (engine, sessionClass, base, databaseDef.url)

            ConcreteModelsMeta._engines[key] = binding

        attrs['_ENGINE']        = binding[0]
        attrs['_SESSION_CLASS'] = binding[1]
        attrs['_BASE']          = binding[2]
        attrs['_URL']           = binding[3]
        attrs['_MODEL_NAME']    = name[:name.rfind('_')]

        session = ConcreteModelsMeta._sessions.get(key)
        if session is None:
            if isMaster:
                session = SqlAlchemyMasterSession(attrs['_SESSION_CLASS'])
            else:
                from ziggurat.sqlalchemy.session.SqlAlchemySlaveSession import SqlAlchemySlaveSession
                session = SqlAlchemySlaveSession(attrs['_SESSION_CLASS'])

            ConcreteModelsMeta._sessions[key] = session

        attrs['_session'] = session

        if not isMaster:
            attrs['masterInstance'] = property(
                ExternalKeyProperty('i', attrs['_MODEL_NAME'], externalIsMaster=True) )

        # Add the declarative base to inheritance
        declaredBase = (attrs['_BASE'],)
        try:
            bases = bases + declaredBase
        except Exception as err:
            bases = declaredBase

        return AbstractModelsMeta.__new__(cls, name, bases, attrs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: __databasename__
    @property
    def __databasename__(cls):
        return cls._DATABASE.name

#___________________________________________________________________________________________________ GS: __modelname__
    @property
    def __modelname__(cls):
        return cls._MODEL_NAME

#___________________________________________________________________________________________________ GS: session
    @property
    def session(cls):
        return cls._session if cls.IS_MASTER else None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getDebugInfo
    def getDebugInfo(cls):
        s    = 'DEBUG: %s\n\tSUPER CLASSES:' % cls.__name__
        base = None
        for b in cls.__bases__:
            s += '\n\t\t%s(%s)' % (str(b.__name__), str(b.__module__))
            if b.__module__ == 'sqlalchemy.ext.declarative':
                base = b

        if base is None:
            return

        s += '\n\tMODEL REGISTRY:'
        for n,v in DictUtils.iter(base._decl_class_registry):
            s += '\n\t\t' + str(n) + '(' + str(v.__module__) + ')'

        return s

#___________________________________________________________________________________________________ query
    def query(cls, modelFilter =None, modelOrderBy =None, limit =None, offset =None,
              joinModels =None):
        query = cls.createQuery()
        if joinModels is not None:
            for model in joinModels:
                query = query.join(model)

        if modelFilter is not None:
            query = query.filter(modelFilter)
        if modelOrderBy is not None:
            query = query.order_by(modelOrderBy)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return cls.createResult(query)

#___________________________________________________________________________________________________ createQuery
    def createQuery(cls, *args):
        try:
            return cls._session.createQuery(*args if args else [cls])
        except Exception as err:
            AbstractModelsMeta.logger.writeError([
                'Query Creation Failure: ' + StringUtils.toUnicode(cls.__name__),
                'META: ' + StringUtils.toUnicode(cls.__base__.metadata),
                'REGISTRY: ' + StringUtils.toUnicode(cls.__base__._decl_class_registry),
                'ENGINES: ' + StringUtils.toUnicode(ConcreteModelsMeta._engines),
                'SESSIONS: ' + StringUtils.toUnicode(ConcreteModelsMeta._sessions),
                'ABSTRACT REGISTRY: ' + StringUtils.toUnicode(AbstractModelsMeta._registry) ], err)
            raise err

#___________________________________________________________________________________________________ createResult
    def createResult(cls, query, lock =False):
        return SqlAlchemyResult(cls, query, lock)

#___________________________________________________________________________________________________ cleanupSessions
    @staticmethod
    def cleanupSessions():
        for session in ConcreteModelsMeta._sessions.values():
            session.cleanup()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createRelationship
    def _createRelationship(
            cls, backRefName, foreignModelName, foreignJoinColumnName, localJoinColumnName ='i'
    ):

        backModelName = foreignModelName + ('_Master' if cls.IS_MASTER else '_Slave')
        return relationship(
            backModelName,
            backref=backRefName,
            primaryjoin=('%s.%s == %s.%s' % (
                cls.__name__, localJoinColumnName, backModelName, foreignJoinColumnName) ))

#___________________________________________________________________________________________________ _getDatabaseKey
    @staticmethod
    def _getDatabaseKey(module, isMaster):
        # Get the database name from the module path.
        prefix  = module[:module.rfind('.')]
        package = prefix[prefix.rfind('.') + 1:]
        return (package, isMaster)

#===================================================================================================
#                                                                                   P A C K A G E

#___________________________________________________________________________________________________ ping_connection
@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except Exception as err:
        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        AbstractModelsMeta.logger.writeError('Cursor FAILED', err)
        print('CURSOR FAILURE')
        raise exc.DisconnectionError()
    cursor.close()

