# ConcreteModelsMeta.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from sqlalchemy import create_engine, exc, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.pool import Pool
from sqlalchemy.pool import QueuePool

from vmi.config.Config import CONFIG
from vmi.config import Databases
from vmi.config.Environment import ENVIRONMENT
from vmi.models.shared.SQLAlchemyResult import SQLAlchemyResult
from vmi.models.shared.metas.AbstractModelsMeta import AbstractModelsMeta
from vmi.models.shared.metas.ExternalKeyProperty import ExternalKeyProperty
from vmi.models.shared.session.SQLAlchemyMasterSession import SQLAlchemyMasterSession
from pyaid.number.IntUtils import IntUtils

#___________________________________________________________________________________________________ ConcreteModelsMeta
class ConcreteModelsMeta(AbstractModelsMeta):

#===================================================================================================
#                                                                                       C L A S S

    # Stores existing engine and sessions for shared access
    _engines  = {}
    _sessions = {}

#___________________________________________________________________________________________________ __new__
    def __new__(cls, name, bases, attrs):
        module   = attrs['__module__']
        package  = module[:module.rfind('.')]
        res      = __import__(package, globals(), locals(), ['DATABASE'])
        database = getattr(res, 'DATABASE')

        attrs['_DATABASE'] = database

        isMaster  = attrs['IS_MASTER']
        isPyramid = ENVIRONMENT.CURRENT == ENVIRONMENT.PYRAMID_ENV_ID
        isDjango  = ENVIRONMENT.CURRENT == ENVIRONMENT.DJANGO_ENV_ID
        key       = ConcreteModelsMeta._getDatabaseKey(attrs['__module__'], isMaster)
        binding   = ConcreteModelsMeta._engines.get(key)
        if binding is None:
            userGroup = (
                database['users'][0] if isinstance(database['users'], list) else database['users']
            )

            if isMaster and not isPyramid and not isDjango:
                account = userGroup['admin'][0]
            elif isMaster:
                account = userGroup['master'][0]
            else:
                account = userGroup['slave'][0]

            connect_args = {
                'unix_socket':str(Databases.SQL_SOCKET_PATH),
                'charset':'utf8'
            }

            if Databases.USE_SSL:
                connect_args['ssl'] = {
                    'cert':CONFIG.MAIN_PRIVATE_CERT_PATH + CONFIG.CLIENT_CERT_NAME,
                    'key' :CONFIG.MAIN_PRIVATE_CERT_PATH + CONFIG.CLIENT_KEY_NAME,
                    'ca'  :CONFIG.MAIN_PRIVATE_CERT_PATH + CONFIG.CA_CERT_NAME
                }

            url = 'mysql+oursql://%s:%s@%s:%s/%s' % (
                account['user'],
                account['password'],
                database['master'] if isMaster else database['slave'],
                str(Databases.SQL_ACCESS_PORT), database['name']
            )

            engine = create_engine(
                url,
                echo=False,
                poolclass=QueuePool,
                echo_pool=True,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=IntUtils.jitter(1800),
                connect_args=connect_args
            )

            if isPyramid:
                from zope.sqlalchemy import ZopeTransactionExtension
                sessionClass = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
            else:
                sessionClass = scoped_session(sessionmaker())
            sessionClass.configure(bind=engine)

            base               = declarative_base()
            base.metadata.bind = engine
            base.metadata.create_all(engine)

            binding = (engine, sessionClass, base, url)

            ConcreteModelsMeta._engines[key] = binding

        attrs['_ENGINE']        = binding[0]
        attrs['_SESSION_CLASS'] = binding[1]
        attrs['_BASE']          = binding[2]
        attrs['_URL']           = binding[3]
        attrs['_MODEL_NAME']    = name[:name.rfind('_')]

        session = ConcreteModelsMeta._sessions.get(key)
        if session is None:
            if isMaster:
                session = SQLAlchemyMasterSession(attrs['_SESSION_CLASS'])
            else:
                from vmi.models.shared.session.SQLAlchemySlaveSession import SQLAlchemySlaveSession
                session = SQLAlchemySlaveSession(attrs['_SESSION_CLASS'])

            ConcreteModelsMeta._sessions[key] = session

        attrs['_session'] = session

        if not isMaster:
            attrs['masterInstance'] = property(
                ExternalKeyProperty('i', attrs['_MODEL_NAME'], externalIsMaster=True)
            )

        # Add the declarative base to inheritance
        declaredBase = (attrs['_BASE'],)
        try:
            bases = bases + declaredBase
        except Exception, err:
            bases = declaredBase

        return AbstractModelsMeta.__new__(cls, name, bases, attrs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: __databasename__
    @property
    def __databasename__(cls):
        return cls._DATABASE['name']

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
        s  = 'DEBUG: ' + cls.__name__
        s += '\n\tSUPER CLASSES:'
        base = None
        for b in cls.__bases__:
            s += '\n\t\t' + str(b.__name__) + '(' + str(b.__module__) + ')'
            if b.__module__ == 'sqlalchemy.ext.declarative':
                base = b

        if base is None:
            return

        s += '\n\tMODEL REGISTRY:'
        for n,v in base._decl_class_registry.iteritems():
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
        except Exception, err:
            AbstractModelsMeta._logger.writeError(
                'Query Creation Failure: ' + unicode(cls.__name__)
                + '\nMETA: ' + unicode(cls.__base__.metadata)
                + '\nREGISTRY: ' + unicode(cls.__base__._decl_class_registry)
                + '\nENGINES: ' + unicode(ConcreteModelsMeta._engines)
                + '\nSESSIONS: ' + unicode(ConcreteModelsMeta._sessions)
                + '\nABSTRACT REGISTRY: ' + unicode(AbstractModelsMeta._registry), err)
            raise err

#___________________________________________________________________________________________________ createResult
    def createResult(cls, query, lock =False):
        return SQLAlchemyResult(cls, query, lock)

#___________________________________________________________________________________________________ cleanupSessions
    @staticmethod
    def cleanupSessions():
        for session in ConcreteModelsMeta._sessions.values():
            session.cleanup()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createRelationship
    def _createRelationship(cls, backRefName, foreignModelName, foreignJoinColumnName,
            localJoinColumnName ='i'):

        backModelName = foreignModelName + ('_Master' if cls.IS_MASTER else '_Slave')
        return relationship(
            backModelName,
            backref=backRefName,
            primaryjoin=('%s.%s == %s.%s' % (
                cls.__name__, localJoinColumnName, backModelName, foreignJoinColumnName)
            )
        )

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
    except Exception, err:
        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        AbstractModelsMeta._logger.writeError('Cursor FAILED', err)
        print 'CURSOR FAILURE'
        raise exc.DisconnectionError()
    cursor.close()

