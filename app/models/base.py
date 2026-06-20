from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.core.database import Base

# Таблица связи для лайков (Многие-ко-Многим)
likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("tweet_id", Integer, ForeignKey("tweets.id"), primary_key=True)
)

# Таблица связи для подписок (Многие-ко-Многим, самоссылающаяся)
followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)

    # Связи
    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
    liked_tweets = relationship("Tweet", secondary=likes, back_populates="liked_by")
    
    # Настройка подписок с использованием строк (для исключения ошибок с id)
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id==followers.c.follower_id",
        secondaryjoin="User.id==followers.c.following_id",
        backref="followers"
    )

class Tweet(Base):
    __tablename__ = "tweets"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    # Связи
    author = relationship("User", back_populates="tweets")
    medias = relationship("Media", back_populates="tweet", cascade="all, delete-orphan")
    liked_by = relationship("User", secondary=likes, back_populates="liked_tweets")

class Media(Base):
    __tablename__ = "medias"
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)

    # Связь
    tweet = relationship("Tweet", back_populates="medias")