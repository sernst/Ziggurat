# ExternalKeyProperty.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

#___________________________________________________________________________________________________ ExternalKeyProperty
class ExternalKeyProperty(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(
            self, localColumnName, externalModelName, externalColumnName ='i',
            externalIsMaster =None
    ):
        self._localColumnName    = localColumnName
        self._externalModelName  = externalModelName
        self._externalColumnName = externalColumnName
        self._externalIsMaster   = externalIsMaster
        self._externalModel      = None

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedSelf):
        if self._externalIsMaster is None:
            self._externalIsMaster = wrappedSelf.IS_MASTER

        if not self._externalModel:
            raise Exception, 'ERROR: Unknown model specification'

        externalColumn = getattr(self._externalModel, self._externalColumnName)
        localColumn    = getattr(wrappedSelf, self._localColumnName)
        query          = self._externalModel.createQuery()
        query          = query.filter(externalColumn == localColumn)
        return self._externalModel.createResult(query).first()

