# ZigguratDatabaseDefinition.py
# (C)2013
# Scott Ernst

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from pyaid.file.FileUtils import FileUtils
from pyaid.number.IntUtils import IntUtils

#___________________________________________________________________________________________________ ZigguratDatabaseDefinition
class ZigguratDatabaseDefinition(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, copyFrom =None, **kwargs):
        """Creates a new instance of ZigguratDatabaseDefinition."""
        self._host       = self._fetchValue('host', u'localhost', kwargs, copyFrom)
        self._name       = self._fetchValue('name', None, kwargs, copyFrom)
        self._user       = self._fetchValue('user', None, kwargs, copyFrom)
        self._password   = self._fetchValue('password', None, kwargs, copyFrom)
        self._certPath   = self._fetchValue('certPath', None, kwargs, copyFrom)
        self._certName   = self._fetchValue('sslName', '???', kwargs, copyFrom)
        self._certKey    = self._fetchValue('sslKey', '???', kwargs, copyFrom)
        self._certAuth   = self._fetchValue('sslAuthority', '???', kwargs, copyFrom)
        self._port       = self._fetchValue('port', 3306, kwargs, copyFrom)
        self._useSSL     = self._fetchValue('useSSL', self._certPath is not None, kwargs)
        self._socketPath = self._fetchValue('socketPath', None, kwargs, copyFrom)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: host
    @property
    def host(self):
        return self._host

#___________________________________________________________________________________________________ GS: user
    @property
    def user(self):
        return self._user

#___________________________________________________________________________________________________ GS: password
    @property
    def password(self):
        return self._password

#___________________________________________________________________________________________________ GS: port
    @property
    def port(self):
        return self._port

#___________________________________________________________________________________________________ GS: socketPath
    @property
    def socketPath(self):
        return self._socketPath

#___________________________________________________________________________________________________ GS: sslCertificatePath
    @property
    def sslCertificatePath(self):
        return FileUtils.cleanupPath(self._certPath, isDir=True) if self._certPath else None

#___________________________________________________________________________________________________ GS: sslClientCertificate
    @property
    def sslClientCertificate(self):
        p = self.sslCertificatePath
        if p and self._certName:
            return FileUtils.createPath(p, self._certName, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: sslClientCertificateKey
    @property
    def sslClientCertificateKey(self):
        p = self.sslCertificatePath
        if p and self._certKey:
            return FileUtils.createPath(p, self._certKey, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: sslClientCertificateAuthority
    @property
    def sslClientCertificateAuthority(self):
        p = self.sslCertificatePath
        if p and self._certAuth:
            return FileUtils.createPath(p, self._certAuth, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: useSSL
    @property
    def useSSL(self):
        return self._useSSL

#___________________________________________________________________________________________________ GS: sslName
    @property
    def sslName(self):
        return self._certName

#___________________________________________________________________________________________________ GS: sslKey
    @property
    def sslKey(self):
        return self._certKey

#___________________________________________________________________________________________________ GS: sslAuthority
    @property
    def sslAuthority(self):
        return self._certAuth

#___________________________________________________________________________________________________ GS: name
    @property
    def name(self):
        return self._name

#___________________________________________________________________________________________________ GS: getUrl
    @property
    def url(self):
        return 'mysql+oursql://%s:%s@%s:%s/%s' % (
            self.user, self.password, self.host, str(self.port), self.name)

#___________________________________________________________________________________________________ GS: sslConnectArgs
    @property
    def sslConnectArgs(self):
        return {
            'cert':self.sslClientCertificate,
            'key' :self.sslClientCertificateKey,
            'ca'  :self.sslClientCertificateAuthority }

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createEngine
    def createEngine(self):
        connectArgs = {'charset':'utf8'}

        if self.socketPath:
            connectArgs['unix_socket'] = str(self.socketPath)

        if self.useSSL:
            connectArgs['ssl'] = self.sslConnectArgs

        return create_engine(
            self.url,
            echo=False,
            poolclass=QueuePool,
            echo_pool=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=IntUtils.jitter(1800),
            connect_args=connectArgs )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _fetchValue
    def _fetchValue(self, key, defaultValue =None, kwargData =None, source =None, sourceProp =None):
        if kwargData and key in kwargData:
            return key.get(kwargData, None)

        if source is None:
            return defaultValue

        return getattr(source, sourceProp if sourceProp else key, defaultValue)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
