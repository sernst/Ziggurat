# ModelPropertyGetter.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

from ziggurat.sqlalchemy.meta.ModelProperty import ModelProperty

#___________________________________________________________________________________________________ ModelPropertyGetter
class ModelPropertyGetter(ModelProperty):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedSelf):
        return getattr(wrappedSelf, self._name)

