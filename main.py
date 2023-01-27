#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from ui.app import app, sqldb, login_manager
from ui.views import monster_castle


@login_manager.user_loader
def load_user(user_id):
    return 1


if __name__ == '__main__':
  with app.app_context():
    app.register_blueprint(monster_castle)

    sqldb.create_all()
    sqldb.session.commit()

  app.run(debug=True)
