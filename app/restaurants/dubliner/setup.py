import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


import json
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database.models import Table, Restaurant


def get_or_create_restaurant(db: Session, name: str) -> int:
    restaurant = db.query(Restaurant).filter_by(name=name).first()
    if restaurant:
        return restaurant.id
    new_restaurant = Restaurant(name=name)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant.id

def setup_tables_for_dubliner():
    db: Session = SessionLocal()
    try:
        restaurant_name = "Dubliner"
        restaurant_id = get_or_create_restaurant(db, restaurant_name)

        with open("app/restaurants/dubliner/tables.json", encoding="utf-8") as f:
            tables = json.load(f)

        for t in tables:
            exists = db.query(Table).filter_by(table_code=t["table_code"], restaurant_id=restaurant_id).first()
            if not exists:
                db.add(Table(
                    table_code=t["table_code"],
                    capacity=t["capacity"],
                    location=t.get("location"),
                    restaurant_id=restaurant_id,
                    is_active=True
                ))
        db.commit()
        print(f"{restaurant_name} için masalar başarıyla eklendi.")
    finally:
        db.close()

if __name__ == "__main__":
    setup_tables_for_dubliner()
