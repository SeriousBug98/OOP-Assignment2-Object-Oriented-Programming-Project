import sqlite3


class DatabaseConnection:
    """싱글톤 패턴 - DB 커넥션을 하나만 유지"""

    _instance = None
    _connection = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            if db_path is None:
                raise ValueError("First initialization requires db_path.")
            cls._instance = super().__new__(cls)
            cls._connection = sqlite3.connect(db_path, check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
            print(f"[DB] Connected to '{db_path}'")
        return cls._instance

    @property
    def connection(self):
        return self._connection

    def execute(self, sql, params=()):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        self._connection.commit()
        return cursor

    def close(self):
        if self._connection:
            self._connection.close()
            DatabaseConnection._instance = None
            DatabaseConnection._connection = None
            print("[DB] Connection closed.")


class QuerySet:
    """메서드 체이닝을 지원하는 쿼리 빌더"""

    def __init__(self, model_class):
        self._model = model_class
        self._filters = []
        self._order = None
        self._limit_val = None

    def filter(self, **kwargs):
        """WHERE 조건 추가"""
        clone = self._clone()
        for key, value in kwargs.items():
            clone._filters.append((key, value))
        return clone

    def order_by(self, field: str):
        """ORDER BY 추가 (앞에 '-' 붙이면 DESC)"""
        clone = self._clone()
        if field.startswith("-"):
            clone._order = f"{field[1:]} DESC"
        else:
            clone._order = f"{field} ASC"
        return clone

    def limit(self, n: int):
        """LIMIT 추가"""
        clone = self._clone()
        clone._limit_val = n
        return clone

    def _build_query(self):
        table = self._model._table_name()
        sql = f"SELECT * FROM {table}"
        params = []

        if self._filters:
            conditions = " AND ".join([f"{k} = ?" for k, _ in self._filters])
            params = [v for _, v in self._filters]
            sql += f" WHERE {conditions}"

        if self._order:
            sql += f" ORDER BY {self._order}"

        if self._limit_val:
            sql += f" LIMIT {self._limit_val}"

        return sql, params

    def all(self):
        """전체 결과 반환 (list)"""
        sql, params = self._build_query()
        db = DatabaseConnection()
        rows = db.execute(sql, params).fetchall()
        return [self._model._from_row(row) for row in rows]

    def first(self):
        """첫 번째 결과만 반환"""
        results = self.limit(1).all()
        return results[0] if results else None

    def count(self):
        """결과 개수 반환"""
        table = self._model._table_name()
        sql = f"SELECT COUNT(*) FROM {table}"
        params = []
        if self._filters:
            conditions = " AND ".join([f"{k} = ?" for k, _ in self._filters])
            params = [v for _, v in self._filters]
            sql += f" WHERE {conditions}"
        db = DatabaseConnection()
        return db.execute(sql, params).fetchone()[0]

    def _clone(self):
        clone = QuerySet(self._model)
        clone._filters = self._filters[:]
        clone._order = self._order
        clone._limit_val = self._limit_val
        return clone

    def __repr__(self):
        return f"<QuerySet [{', '.join(str(obj) for obj in self.all())}]>"
