# AbstractModelsMeta.py
# (C)2012-2014
# Scott Ernst and Eric David Wills

from __future__ import print_function, absolute_import, unicode_literals, division

from sqlalchemy import Column
from sqlalchemy import orm
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property

from ziggurat.sqlalchemy.meta.ExternalKeyProperty import ExternalKeyProperty
from ziggurat.sqlalchemy.meta.ModelPropertyExpression import ModelPropertyExpression
from ziggurat.sqlalchemy.meta.ModelPropertyGetter import ModelPropertyGetter
from ziggurat.sqlalchemy.meta.ModelPropertySetter import ModelPropertySetter
from ziggurat.utils.debug.ServerLogger import ServerLogger


#___________________________________________________________________________________________________ AbstractModelsMeta
class AbstractModelsMeta(DeclarativeMeta):

#===================================================================================================
#                                                                                       C L A S S

    _registry = dict()
    logger    = ServerLogger('SqlAlchemyModels')

#___________________________________________________________________________________________________ __new__
    def __new__(mcs, name, bases, attrs):
        for n, v in attrs.items():
            attrName = n[1:]
            if isinstance(v, Column) and n.startswith('_') and not attrs.has_key(attrName):
                v.key  = attrName
                v.name = attrName

                # Add dynamic property
                setter = ModelPropertySetter(n)

                attrs[attrName] = hybrid_property(
                    ModelPropertyGetter(n), setter, None, ModelPropertyExpression(n) )

                # Add external-key property
                info = getattr(v, 'info')
                if info and 'model' in info:
                    columnName = info['column'] if 'column' in info else 'i'
                    attrs[info['get']] = property(
                        ExternalKeyProperty(attrName, info['model'], columnName) )

        return DeclarativeMeta.__new__(mcs, name, bases, attrs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: MASTER
    @property
    def MASTER(cls):
        return cls.getModel('MASTER')

#___________________________________________________________________________________________________ GS: SLAVE
    @property
    def SLAVE(cls):
        return cls.getModel('SLAVE')

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getModel
    def getModel(cls, modelType =None):
        this     = AbstractModelsMeta
        isMaster = (modelType == 'MASTER')
        name     = cls.__name__ + ('_Master' if isMaster else '_Slave')

        if name in this._registry:
            return this._registry[name]

        # New method to be wrapped as the ORM reconstructor
        def reconstructor(self):
            self.ormInit()

        from ziggurat.sqlalchemy.meta.ConcreteModelsMeta import ConcreteModelsMeta
        this._registry[name] = ConcreteModelsMeta(
            name, (cls,), {
                '__module__':cls.__module__,
                'IS_MASTER':isMaster,
                'ormReconstructor':orm.reconstructor(reconstructor) })

        return this._registry[name]

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __str__
    def __str__(cls):
        return '<ModelClass %s>' % cls.__name__

