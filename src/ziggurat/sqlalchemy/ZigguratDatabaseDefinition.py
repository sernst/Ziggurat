# ZigguratDatabaseDefinition.py
# (C)2013
# Scott Ernst

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from pyaid.file.FileUtils import FileUtils
from pyaid.number.IntUtils import IntUtils

#___________________________________________________________________________________________________ ZigguratDatabaseDefinition
class ZigguratDatabaseDefinition(object):
    """ A class that encapsulates all the information for defining a database, which is used
        within Ziggurat applications to establish connections to the specified database
        through the SqlAlchemy ORM."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, copyFrom =None, **kwargs):
        """ Creates a new instance of ZigguratDatabaseDefinition from the specified arguments:

            @param copyFrom - Another ZigguratDatabaseDefinition that should be copied from in
                    cases where no explicit constructor argument was specified. This is a useful
                    way to make similar database definitions by cloning the values of other
                    definition instances.

            @param kwargs - Any number of other attributes, e.g. host or name, which are identical
                    to the property names of the class. """

        self._host       = self._fetchValue('host', u'localhost', kwargs, copyFrom)
        self._name       = self._fetchValue('name', None, kwargs, copyFrom)
        self._user       = self._fetchValue('user', None, kwargs, copyFrom)
        self._password   = self._fetchValue('password', None, kwargs, copyFrom)
        self._certPath   = self._fetchValue('certPath', None, kwargs, copyFrom)
        self._certName   = self._fetchValue('sslName', 'cert.pem', kwargs, copyFrom)
        self._certKey    = self._fetchValue('sslKey', 'key.pem', kwargs, copyFrom)
        self._certAuth   = self._fetchValue('sslAuthority', 'ca.pem', kwargs, copyFrom)
        self._port       = self._fetchValue('port', 3306, kwargs, copyFrom)
        self._useSSL     = self._fetchValue('useSSL', self._certPath is not None, kwargs)
        self._socketPath = self._fetchValue('socketPath', None, kwargs, copyFrom)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: host
    @property
    def host(self):
        """ The host name of the MySQL server where this database resides """
        return self._host

#___________________________________________________________________________________________________ GS: user
    @property
    def user(self):
        """ The account user for connecting to the database """
        return self._user

#___________________________________________________________________________________________________ GS: password
    @property
    def password(self):
        """ The account password used to connect to the database """
        return self._password

#___________________________________________________________________________________________________ GS: port
    @property
    def port(self):
        """ The port to use when connecting to the MySQL server where this database resides """
        return self._port

#___________________________________________________________________________________________________ GS: socketPath
    @property
    def socketPath(self):
        """ The absolute path to the MySQL socket file """
        return self._socketPath

#___________________________________________________________________________________________________ GS: sslCertificatePath
    @property
    def sslCertificatePath(self):
        """ The path to the folder containing the SSL security certificate, key, and authority
            files """
        return FileUtils.cleanupPath(self._certPath, isDir=True) if self._certPath else None

#___________________________________________________________________________________________________ GS: sslClientCertificate
    @property
    def sslClientCertificate(self):
        """ The absolute path to the SSL certificate file """
        p = self.sslCertificatePath
        if p and self._certName:
            return FileUtils.createPath(p, self._certName, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: sslClientCertificateKey
    @property
    def sslClientCertificateKey(self):
        """ The absolute path to the SSL key file """
        p = self.sslCertificatePath
        if p and self._certKey:
            return FileUtils.createPath(p, self._certKey, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: sslClientCertificateAuthority
    @property
    def sslClientCertificateAuthority(self):
        """ The absolute path to the SSL certificate authority file """
        p = self.sslCertificatePath
        if p and self._certAuth:
            return FileUtils.createPath(p, self._certAuth, isFile=True)
        return None

#___________________________________________________________________________________________________ GS: useSSL
    @property
    def useSSL(self):
        """ Specifies whether or not database connection should be using a secure SSL connection """
        return self._useSSL

#___________________________________________________________________________________________________ GS: sslName
    @property
    def sslName(self):
        """ The file name of the SSL certificate, including extension, which must be located in the
            sslCertificatePath """
        return self._certName

#___________________________________________________________________________________________________ GS: sslKey
    @property
    def sslKey(self):
        """ The key file, including extension, which must be located in the sslCertificatePath """
        return self._certKey

#___________________________________________________________________________________________________ GS: sslAuthority
    @property
    def sslAuthority(self):
        """ The certificate authority file name, including extension, which must be located
            in the sslCertificatePath """
        return self._certAuth

#___________________________________________________________________________________________________ GS: name
    @property
    def name(self):
        """ Name of the database """
        return self._name

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        """ The database engine url used to connect to the database """
        return 'mysql+oursql://%s:%s@%s:%s/%s' % (
            self.user, self.password, self.host, str(self.port), self.name)

#___________________________________________________________________________________________________ GS: sslConnectArgs
    @property
    def sslConnectArgs(self):
        """ If SSL arguments were specified, this return the dictionary containing the connection
            arguments as needed by the ORM during creation of the database engine """
        return {
            'cert':self.sslClientCertificate,
            'key' :self.sslClientCertificateKey,
            'ca'  :self.sslClientCertificateAuthority }

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createEngine
    def createEngine(self):
        """ Creates the database engine for this definition """
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
            return kwargData.get(key, None)

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
        return u'<%s[%s]: "%s@%s">' % (self.__class__.__name__, self.name, self.user, self.host)

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return self.__unicode__().decode('utf-8', 'ignore')
