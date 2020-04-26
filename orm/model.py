#coding: utf8
from sweet.utils import *
from sweet.utils.inflection import *

class ModelHasBeenPersisted(Exception): pass
class ModelHasNotBeenPersisted(Exception): pass


class ModelMetaClass(type):

    def __init__(cls, name, bases, attr):
        model = type.__init__(cls, name, bases, attr)
        assert model is None
        if name != 'Model':

            
            # assert model is not None

            # set __tablename__ to Record Class
            if not hasattr(cls, '__tablename__'):
                setattr(cls, '__tablename__', tableize(cls.__name__))

            if not hasattr(cls, '__field_define_dict__'):
                setattr(cls, '__field_define_dict__', {})
                cls._init_fields()

            if not hasattr(cls, '__pk__'):
                setattr(cls, '__pk__', 'id')

            # if cls.__pk__ not in cls.__field_define_dict__:
            #     raise Exception('%s field of %s does not exist' % (cls.__pk__, cls.__name__))

            if getattr(cls, '__timestamp__', True):
                setattr(cls, 'created_at', None)
                setattr(cls, 'updated_at', None)

            # from sweet.relation import Relation
            # for relation in Relation.iter():
            #     relation.inject(cls)

            # # id column must in columns validate
            # if cls.__pk__ not in cls.__field_define_dict__:
            #     raise PKColumnNotInColumns()
            # for c, err in [
            #     (cls.__pk__, PKColumnNotInColumns),
            #     (cls.__created_at__, CreatedAtColumnNotInColumns), 
            #     (cls.__updated_at__, UpdatedAtColumnNotInColumns),
            #     (cls.__created_on__, CreatedOnColumnNotInColumns),
            #     (cls.__updated_on__, UpdatedOnColumnNotInColumns),
            # ]:
            #     if c and  c not in cls.__field_define_dict__:
            #         raise err()

        return model


class Model(metaclass=ModelMetaClass):

    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)
        self._init_field_default_value() # !Very Important

    def _init_field_default_value(self):
        """ set default value of field which does not init 
        """
        cls = self.__class__
        for name, field in cls.__field_define_dict__.items():
            if not hasattr(self, name):
                setattr(self, name, field.default)
        return self

    def column_dict(self):
        return { 
            name:getattr(self, name, field.default) \
                for name, field in self.__field_define_dict__.items() 
        }

    def save(self):
        """ save object. 
        will update the record if it has been persisted else create one.
        """
        if self.persisted():
            self.update()
        else:
            _id = self._rs.insert_getid(**self.column_dict())
            self.set_pk(_id)
        return self

    @classmethod
    def create(cls, **attrs):
        """ create a record in db.
        should raise ModelHasBeenPersisted if it has been persisted
        """
        model = cls(**attrs)
        model.save()
        return model

    def update(self, **attrs):
        """ update a record in db, 
        should raise ModelHasNotBeenPersisted if it has not been persisted
        """
        if not self.persisted():
            raise ModelHasNotBeenPersisted()
        if attrs:
            self._rs.update(**attrs)
            for k, v in attrs.items():
                setattr(self, k, v)
        else:
            self._rs.update(**self.column_dict())
        return self

    @classmethod
    def update_all(cls, **attrs):
        """ delete all record
        """
        cls._rs.update(**attrs)
        return cls

    def delete(self):
        """ delete a record in db and set id is None.
        would do nothing if it has not been persisted
        """
        if self.persisted():
            pk = self.__pk__
            self._rs.where(**{self.__pk__: self.get_pk()}).delete()
            self.set_pk(None)
        return self

    @classmethod
    def delete_all(cls):
        """ delete all record
        """
        cls._rs.delete()
        return cls

    def set_pk(self, value):
        return setattr(self, self.__pk__, value)

    def get_pk(self):
        return getattr(self, self.__pk__, None)

    def persisted(self):
        return True if self.get_pk() else False

    @classmethod
    def count(cls):
        return cls._rs.count()

    @classmethod
    def truncate(self):
        return cls._rs.truncate()

    @classmethod
    def exists(self):
        return cls._rs.exists()

    @classmethod
    def max(self, column, distinct=False):
        return cls._rs.max(column, distinct)

    @classmethod
    def min(self, column, distinct=False):
        return cls._rs.min(column, distinct)

    @classmethod
    def avg(self, column, distinct=False):
        return cls._rs.avg(column, distinct)

    @classmethod
    def sum(self, column, distinct=False):
        return cls._rs.sum(column, distinct)

    @classmethod
    def all(cls):
        return cls._rs.all()

    @classmethod
    def first(cls):
        return cls._rs.first()

    @classmethod
    def last(self):
        return self._rs.last()

    @classmethod
    def find(cls, *ids):
        if len(ids) == 1:
            return cls._rs.where(id=ids).first()
        else:
            return cls._rs.where(id=ids).all()

    @classproperty
    def _rs(cls):
        db = cls.db_manager.new_db()
        return db.records(cls.__tablename__)

    @classmethod
    def _init_fields(cls):
        for c in cls.db_manager.new_db().get_columns(cls.__tablename__):
            cls.__field_define_dict__[c.name] = c
        return cls
