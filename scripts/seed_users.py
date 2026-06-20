from app.core.database import SessionLocal
from app.models.base import User

db = SessionLocal()

if db.query(User).count() == 0:
    db.add_all([
        User(name="Alice", api_key="alice-key-123"),
        User(name="Bob", api_key="bob-key-456"),
        User(name="Charlie", api_key="charlie-key-789"),
    ])
    db.commit()
    print("Users created")
else:
    print("Users already exist")

db.close()