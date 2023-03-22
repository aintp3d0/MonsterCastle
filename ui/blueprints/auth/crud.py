from typing import Optional

import sqlalchemy as sa

from .models import sqldb, User


class UserQuery:

  @staticmethod
  def create(name: str, token: str) -> None:
    sqldb.session.add(User(name=name, token=token))
    sqldb.session.commit()

  @staticmethod
  def get(token: str) -> Optional[User]:
    return User.query.filter_by(token=token).first()


def get_user_by_image_hash(image_hash: str):
  return MC_User.query.filter_by(image_hash=image_hash).first()


def get_user_by_openid(openid: str):
  return MC_User.query.filter_by(openid=openid).first()


def insert_user_credentials(credentials: dict):
  user_credentials = MC_User(
    openid=credentials.get('openid'),
    image_hash=credentials.get('image_hash')
  )
  sqldb.session.add(user_credentials)
  sqldb.session.commit()


def update_user_credentials(credentials: dict):
  user_credentials = get_user_by_openid(credentials.get('openid'))

  if user_credentials is None:
    return insert_user_credentials(credentials)

  MC_User.query.filter_by(openid=credentials.get('openid')).update(credentials)
  sqldb.session.commit()


def get_all_users():
  return MC_User.query.all()
