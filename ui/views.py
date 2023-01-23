import os
import hashlib
import functools
from typing import Union, List, Dict

from flask import (
  Blueprint, render_template,
  request, session,
  redirect, url_for
)
from werkzeug.utils import secure_filename

from ..src.user.login import UserCredentials

from .query import (
  get_user_by_image_hash, get_user_by_openid, update_user_credentials,
  get_all_users,
)
from .forms import MC_User_Form


monster_castle = Blueprint(
  'monster_castle', __name__,
  template_folder='templates/monster_castle',
  static_folder='static/monster_castle'
)


MC_USER_LOGIN_FLAG = 'MC_USER'
MC_USER_IMAGE_FOLDER = os.path.join(
  monster_castle.static_folder,
  'images', 'users'
)

if not os.path.isdir(MC_USER_IMAGE_FOLDER):
  os.makedirs(MC_USER_IMAGE_FOLDER)


def logged_in():
  image_hash = session.get(MC_USER_LOGIN_FLAG)

  if all((image_hash is not None,
          isinstance(image_hash, str),
          get_user_by_image_hash(image_hash) is not None)):
    return True

  return False


# TODO: remove, use random hash instead
def get_image_hash(image_path: str):
  # SEE: https://www.adamsmith.haus/python/answers/how-to-generate-an-md5-hash-for-large-files-in-python
  md5 = hashlib.md5()
  block_size = 128 * md5.block_size

  file = open(image_path, 'rb')
  chunk = file.read(block_size)

  while chunk:
    md5.update(chunk)
    chunk = file.read(block_size)

  return md5.hexdigest()


def validate_user_credentials(file) -> Dict[str, Union[int, str]]:
  file_path = os.path.join(MC_USER_IMAGE_FOLDER, secure_filename(file.filename))
  file.save(file_path)
  file_extension = os.path.splitext(file.filename)[-1]

  uc = UserCredentials(file_path)
  image_username, image_openid = uc.get_username_and_openid()
  text_openid = uc.validate_image_openid(image_openid)

  def remove_exist(file_path: str):
    if os.path.exists(file_path):
      os.remove(file_path)

  if text_openid is None:
    remove_exist(file_path)
    return {'error': 1, 'message': 'Invalid OpenID'}

  image_hash = get_image_hash(file_path)
  image_path = os.path.join(MC_USER_IMAGE_FOLDER, image_hash)

  def openid_and_username_filepath(image_path: str) -> List[str]:
    return [
      '_'.join((image_path, add_extension(i))) for i in ('openid', 'username')
    ]

  def add_extension(file_path: str) -> str:
    return file_path + file_extension

  image_openid_path, image_username_path = openid_and_username_filepath(image_path)

  uc.save_credential_image(image_openid_path, image_openid)
  uc.save_credential_image(image_username_path, image_username)

  user_credentials = get_user_by_openid(text_openid)

  if user_credentials is not None:
    if image_hash != user_credentials.image_hash:
      prev_image_path = os.path.join(MC_USER_IMAGE_FOLDER, user_credentials.image_hash)
      image_openid_path, image_username_path = openid_and_username_filepath(prev_image_path)

      remove_exist(prev_image_path)
      remove_exist(image_openid_path)
      remove_exist(image_username_path)

  os.rename(file_path, add_extension(image_path))

  return {'image_hash': image_hash, 'openid': text_openid}


@monster_castle.route('/login', methods=['GET', 'POST'])
def login():
  """Simple login page with mc_user image
  """
  if logged_in():
    return redirect(url_for('monster_castle.index'))

  form = MC_User_Form(meta={'csrf': False})

  if form.validate_on_submit():
    validation_status = validate_user_credentials(form.image.data)

    if validation_status.get('error') is None:
      session[MC_USER_LOGIN_FLAG] = validation_status.get('image_hash')
      update_user_credentials(validation_status)
      return redirect(url_for('monster_castle.index'))

  return render_template('login.html', form=form)


@monster_castle.route('/logout', methods=['GET'])
def logout():
  if logged_in():
    del session[MC_USER_LOGIN_FLAG]

  return redirect(url_for('monster_castle.login'))


@monster_castle.route('/')
def index():
  """
  Registered Users    (accounts)
  Registered Guilds   ()
  """
  if not logged_in():
    return redirect(url_for('monster_castle.login'))

  return render_template('index.html')


@monster_castle.route('/guild')
def guild():
  return f"<h1>guild:: {get_all_users()}</h1>"
