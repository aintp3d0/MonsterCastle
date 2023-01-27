#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from ui.app import app, sqldb
from ui.views import monster_castle


if __name__ == '__main__':
  with app.app_context():
    app.register_blueprint(monster_castle)

    sqldb.create_all()
    sqldb.session.commit()

  app.run(debug=True)
