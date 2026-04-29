from fields import Field, IntegerField
from db import DatabaseConnection, QuerySet


class ModelMeta(type):
    """메타클래스 - 클래스 선언 시 Field 자동 인식"""

    def __new__(mcs, name, bases, namespace):
        fields = {}

        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)

        for attr_name, value in namespace.items():
            if isinstance(value, Field):
                value.name = attr_name
                fields[attr_name] = value

        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ModelMeta):
    """모든 테이블 클래스의 추상 부모"""

    def __init__(self, **kwargs):
        for field_name, field_obj in self._fields.items():
            raw_value = kwargs.get(field_name, None)
            validated = field_obj.validate(raw_value)
            setattr(self, field_name, validated)

    @classmethod
    def _table_name(cls) -> str:
        """테이블 이름 = 클래스 이름 소문자"""
        return cls.__name__.lower()

    @classmethod
    def _pk_field(cls):
        """Primary Key 필드 반환"""
        for name, field in cls._fields.items():
            if field.primary_key:
                return name, field
        return None, None

    @classmethod
    def create_table(cls):
        """CREATE TABLE IF NOT EXISTS 실행"""
        columns = [field.to_sql_definition() for field in cls._fields.values()]
        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name()} ({', '.join(columns)});"
        DatabaseConnection().execute(sql)
        print(f"[ORM] Table '{cls._table_name()}' ready.")

    @classmethod
    def create(cls, **kwargs):
        """INSERT - 새 레코드 삽입"""
        pk_name, _ = cls._pk_field()
        data = {k: v for k, v in kwargs.items() if k != pk_name}

        instance = cls(**kwargs)

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())

        sql = f"INSERT INTO {cls._table_name()} ({columns}) VALUES ({placeholders})"
        db = DatabaseConnection()
        cursor = db.execute(sql, values)

        if pk_name:
            setattr(instance, pk_name, cursor.lastrowid)

        print(f"[ORM] Created {cls.__name__} (id={getattr(instance, pk_name, '?')})")
        return instance

    @classmethod
    def filter(cls, **kwargs) -> QuerySet:
        """QuerySet 반환 - 메서드 체이닝 시작점"""
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def all(cls) -> QuerySet:
        """전체 레코드 QuerySet 반환"""
        return QuerySet(cls)

    def save(self):
        """UPDATE - 기존 레코드 수정"""
        pk_name, _ = self._pk_field()
        pk_value = getattr(self, pk_name)

        if pk_value is None:
            raise ValueError("Cannot save: primary key is None. Use create() instead.")

        data = {k: getattr(self, k) for k in self._fields if k != pk_name}
        set_clause = ', '.join([f"{k} = ?" for k in data])
        values = list(data.values()) + [pk_value]

        sql = f"UPDATE {self._table_name()} SET {set_clause} WHERE {pk_name} = ?"
        DatabaseConnection().execute(sql, values)
        print(f"[ORM] Updated {self.__class__.__name__} (id={pk_value})")

    def delete(self):
        """DELETE - 레코드 삭제"""
        pk_name, _ = self._pk_field()
        pk_value = getattr(self, pk_name)

        sql = f"DELETE FROM {self._table_name()} WHERE {pk_name} = ?"
        DatabaseConnection().execute(sql, [pk_value])
        print(f"[ORM] Deleted {self.__class__.__name__} (id={pk_value})")

    @classmethod
    def _from_row(cls, row):
        """DB row → Model 인스턴스 변환"""
        return cls(**dict(row))

    def __repr__(self):
        pk_name, _ = self._pk_field()
        pk_val = getattr(self, pk_name, '?') if pk_name else '?'
        return f"<{self.__class__.__name__} id={pk_val}>"
