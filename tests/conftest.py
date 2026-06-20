import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.base import User, Tweet, Media, likes, followers
from sqlalchemy.pool import StaticPool
# Тестовая БД в памяти
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    """Создаёт чистую БД перед каждым тестом."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    """HTTP-клиент с подменённой БД."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def alice(db):
    """Тестовый пользователь Alice."""
    user = User(name="Alice", api_key="alice-key-123")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@pytest.fixture()
def bob(db):
    """Тестовый пользователь Bob."""
    user = User(name="Bob", api_key="bob-key-456")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user