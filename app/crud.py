from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_chat_id(db: Session, chat_id: int):
    return db.query(models.User).filter(models.User.telegram_chat_id == chat_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        telegram_chat_id=user.telegram_chat_id,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user