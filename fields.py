from abc import ABC, abstractmethod


class Field(ABC):
    """추상 필드 클래스 - 모든 컬럼 타입의 부모"""

    def __init__(self, primary_key=False, nullable=True):
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = None

    @abstractmethod
    def sql_type(self) -> str:
        """SQL 타입 문자열 반환"""
        pass

    @abstractmethod
    def validate(self, value):
        """값 유효성 검사"""
        pass

    def to_sql_definition(self) -> str:
        definition = f"{self.name} {self.sql_type()}"
        if self.primary_key:
            definition += " PRIMARY KEY AUTOINCREMENT"
        if not self.nullable:
            definition += " NOT NULL"
        return definition


class IntegerField(Field):
    """INTEGER 컬럼"""

    def sql_type(self) -> str:
        return "INTEGER"

    def validate(self, value):
        if value is None and not self.nullable:
            raise ValueError(f"Field '{self.name}' cannot be null.")
        if value is not None and not isinstance(value, int):
            raise TypeError(f"Field '{self.name}' expects int, got {type(value).__name__}.")
        return value


class StringField(Field):
    """VARCHAR 컬럼"""

    def __init__(self, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def sql_type(self) -> str:
        return f"VARCHAR({self.max_length})"

    def validate(self, value):
        if value is None and not self.nullable:
            raise ValueError(f"Field '{self.name}' cannot be null.")
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Field '{self.name}' expects str, got {type(value).__name__}.")
        if value and len(value) > self.max_length:
            raise ValueError(f"Field '{self.name}' exceeds max_length={self.max_length}.")
        return value


class FloatField(Field):
    """REAL 컬럼"""

    def sql_type(self) -> str:
        return "REAL"

    def validate(self, value):
        if value is None and not self.nullable:
            raise ValueError(f"Field '{self.name}' cannot be null.")
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(f"Field '{self.name}' expects float, got {type(value).__name__}.")
        return float(value) if value is not None else None
