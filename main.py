#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from ui.blueprints.app import app, sqldb, login_manager
from ui.blueprints.auth.views import auth


@login_manager.user_loader
def load_user(user_id):
    return 1


if __name__ == '__main__':
  with app.app_context():
    app.register_blueprint(auth)

    sqldb.create_all()
    sqldb.session.commit()

  app.run(debug=True)
