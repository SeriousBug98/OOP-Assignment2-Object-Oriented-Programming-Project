import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from db import DatabaseConnection
from model import Model
from fields import IntegerField, StringField, FloatField

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=50, nullable=False)
    age = IntegerField()
    email = StringField(max_length=100)


class Product(Model):
    id = IntegerField(primary_key=True)
    title = StringField(max_length=100, nullable=False)
    price = FloatField(nullable=False)
    stock = IntegerField()

if __name__ == "__main__":
    DatabaseConnection("demo.db")

    User.create_table()
    Product.create_table()

    print("\n=== INSERT ===")
    u1 = User.create(name="SeungWoo", age=25, email="sw@example.com")
    u2 = User.create(name="Sebin", age=24, email="sb@example.com")
    u3 = User.create(name="Alice", age=25, email="alice@example.com")

    p1 = Product.create(title="Laptop", price=1200.0, stock=10)
    p2 = Product.create(title="Mouse", price=25.5, stock=100)
    p3 = Product.create(title="Monitor", price=350.0, stock=15)

    print("\n=== SELECT ALL ===")
    all_users = User.all().all()
    for u in all_users:
        print(f"  {u} | name={u.name}, age={u.age}")

    print("\n=== FILTER ===")
    age25 = User.filter(age=25).all()
    print(f"  age=25인 유저: {age25}")

    print("\n=== ORDER BY ===")
    ordered = Product.all().order_by("price").all()
    for p in ordered:
        print(f"  {p} | {p.title} = ${p.price}")

    print("\n=== FILTER + ORDER BY + FIRST ===")
    result = User.filter(age=25).order_by("name").first()
    print(f"  age=25 중 이름 첫번째: {result.name}")

    print("\n=== COUNT ===")
    cnt = User.filter(age=25).count()
    print(f"  age=25인 유저 수: {cnt}")

    print("\n=== UPDATE ===")
    u1.age = 26
    u1.save()

    print("\n=== DELETE ===")
    u3.delete()

    print("\n=== 삭제 후 전체 조회 ===")
    for u in User.all().all():
        print(f"  {u} | name={u.name}, age={u.age}")

    DatabaseConnection().close()
    if os.path.exists("demo.db"):
        os.remove("demo.db")
