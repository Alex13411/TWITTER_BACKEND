from app.core.database import SessionLocal
from app.models.base import User

DEFAULT_USERS = [
    ("Test", "test"),
    ("Alice", "alice-key-123"),
    ("Bob", "bob-key-456"),
    ("Charlie", "charlie-key-789"),
]

db = SessionLocal()

created = 0
for name, api_key in DEFAULT_USERS:
    if not db.query(User).filter(User.api_key == api_key).first():
        db.add(User(name=name, api_key=api_key))
        created += 1

if created:
    db.commit()
    print(f"Created {created} user(s)")
else:
    print("All default users already exist")

db.close()
