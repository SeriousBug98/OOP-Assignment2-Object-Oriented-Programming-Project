# OOP-Assignment2-Object-Oriented-Programming-Project
건국대학교 26년도 1학기 객체지향프로그래밍 과목 Assignment2 구현 소스코드입니다.

## Mini ORM — Python 미니 ORM 구현

> **건국대학교 Object-Oriented Programming Assignment2**  
> Python OOP 개념을 활용하여 SQLAlchemy / Django ORM의 핵심 동작을 재현한 미니 ORM입니다.

---

### 프로젝트 구조

```
mini_orm/
├── fields.py   # Field 추상 클래스 및 타입별 구현체 (IntegerField, StringField, FloatField)
├── db.py       # DatabaseConnection (싱글톤), QuerySet (메서드 체이닝 쿼리 빌더)
├── model.py    # ModelMeta (메타클래스), Model (추상 부모 클래스)
└── demo.py     # 사용자 모델 정의 및 전체 동작 시연
```

---

### 실행 방법

#### 요구사항
- Python 3.7 이상
- 외부 라이브러리 설치 불필요 (표준 라이브러리 `sqlite3`, `abc`만 사용)

#### 실행

```bash
git clone https://github.com/your-username/mini_orm.git
cd mini_orm
python demo.py
```

#### 정상 출력 확인

```
[DB] Connected to 'demo.db'
[ORM] Table 'user' ready.
[ORM] Table 'product' ready.

=== INSERT ===
[ORM] Created User (id=1)
[ORM] Created User (id=2)
[ORM] Created User (id=3)

=== SELECT ALL ===
  <User id=1> | name=SeungWoo, age=25
  <User id=2> | name=Sebin, age=24
  <User id=3> | name=Alice, age=25

=== FILTER ===
  age=25인 유저: [<User id=1>, <User id=3>]

=== FILTER + ORDER BY + FIRST ===
  age=25 중 이름 첫번째: Alice

=== COUNT ===
  age=25인 유저 수: 2

=== UPDATE ===
[ORM] Updated User (id=1)

=== DELETE ===
[ORM] Deleted User (id=3)

=== 삭제 후 전체 조회 ===
  <User id=1> | name=SeungWoo, age=26
  <User id=2> | name=Sebin, age=24
```

---
