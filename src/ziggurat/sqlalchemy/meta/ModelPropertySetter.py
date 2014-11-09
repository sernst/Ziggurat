# ModelPropertySetter.py
# (C)2012-2014
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.string.StringUtils import StringUtils

from ziggurat.sqlalchemy.meta.ModelProperty import ModelProperty

#___________________________________________________________________________________________________ ModelPropertySetter
class ModelPropertySetter(ModelProperty):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedSelf, value):
        if StringUtils.isStringType(value):
            value = StringUtils.toUnicode(value)

        setattr(wrappedSelf, self._name, value)
