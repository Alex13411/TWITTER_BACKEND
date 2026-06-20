from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.base import User, Tweet
from app.schemas.tweets import TweetCreate, TweetCreateResponse
from app.core.exceptions import TwitterException
from app.schemas.common import SuccessResponse
router = APIRouter()
@router.post("/tweets", response_model=TweetCreateResponse)
def create_tweet(
    tweet_data: TweetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = Tweet(content=tweet_data.tweet_data, author_id=current_user.id)
    db.add(tweet)
    db.commit()
    db.refresh(tweet)
    return TweetCreateResponse(result=True, tweet_id=tweet.id)
@router.delete("/tweets/{tweet_id}", response_model=SuccessResponse)
def delete_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise TwitterException(status_code=404,
        error_type="TweetNotFound", 
        error_message="Твит не найден"
        )
    if tweet.author_id != current_user.id:
        raise TwitterException(status_code=403,
        error_type="Forbidden", 
        error_message="Вы не можете удалить этот твит"
        )
    db.delete(tweet)
    db.commit()
    return SuccessResponse(result=True)
@router.post("/tweets/{tweet_id}/likes", response_model=SuccessResponse)
def like_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise TwitterException(status_code=404,
        error_type="TweetNotFound", 
        error_message=f"Твит с id={tweet_id} не найден"
        )
    if tweet in current_user.liked_tweets:
        raise TwitterException(
            status_code=400,
            error_type="BadRequest",
            error_message="Вы уже поставили лайк на этот твит.",
        )
    current_user.liked_tweets.append(tweet)
    db.commit()
    return SuccessResponse(result=True)
@router.delete("/tweets/{tweet_id}/likes", response_model=SuccessResponse)
def unlike_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if not tweet:
        raise TwitterException(
            status_code=404,
            error_type="TweetNotFound",
            error_message=f"Твит с id={tweet_id} не найден",
        )

    if tweet not in current_user.liked_tweets:
        raise TwitterException(
            status_code=400,
            error_type="BadRequest",
            error_message="Вы не ставили лайк на этот твит.",
        )

    current_user.liked_tweets.remove(tweet)
    db.commit()

    return SuccessResponse(result=True)