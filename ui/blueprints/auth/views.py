import os
import hashlib
import functools
from typing import Union, List, Dict
from uuid import uuid4

from flask import (
  Blueprint, render_template,
  request, session,
  redirect, url_for
)
from werkzeug.utils import secure_filename

from src.user.login import UserCredentials

from .crud import (
  get_user_by_image_hash, get_user_by_openid, update_user_credentials,
  get_all_users,
)
from .crud import UserQuery
from .forms import RegisterForm, LoginForm


auth = Blueprint(
  'auth', __name__,
  template_folder='templates',
  static_folder='static'
)


USER_SESSION_TOKEN_KEY = 'USER_SESSION_TOKEN_KEY'


def logged_in():
  user_token = session.get(USER_SESSION_TOKEN_KEY)
  if user_token is None:
    return False

  user = UserQuery.get(token=user_token)
  if user is None:
    # TODO: Token is not valid
    return False

  return True


def gen_user_token():
  """ Returns uuid4.urn id as a token """
  print('Trying to generate')
  return uuid4().urn


@auth.route('/register', methods=['GET', 'POST'])
def register():
  if logged_in():
    return redirect(url_for('auth.index'))

  form = RegisterForm(meta={'csrf': False})

  if request.method == 'POST':
    if form.validate_on_submit():
      token = gen_user_token()
      UserQuery.create(name=form.name.data, token=token)
      session[USER_SESSION_TOKEN_KEY] = token
      return redirect(url_for('auth.index'))

  return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
  """Simple login page with mc_user image
  """
  if logged_in():
    return redirect(url_for('auth.index'))

  form = LoginForm(meta={'csrf': False})

  print('FOR:', form.validate_on_submit())
  if form.validate_on_submit():
    user = UserQuery.get(form.token.data)

    if user is not None:
      session[USER_SESSION_TOKEN_KEY] = form.token.data
      return redirect(url_for('auth.index'))

  return render_template('login.html', form=form, title='Login')


@auth.route('/logout', methods=['GET'])
def logout():
  if logged_in():
    del session[USER_SESSION_TOKEN_KEY]

  return redirect(url_for('auth.login'))


@auth.route('/')
def index():
  """
  Registered Users    (accounts)
  Registered Guilds   ()
  """
  if not logged_in():
    return redirect(url_for('auth.login'))

  return render_template('index.html')


@auth.route('/guild')
def guild():
  return f"<h1>guild:: {get_all_users()}</h1>"
