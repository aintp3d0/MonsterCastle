#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from ui.views import monster_castle


app = Flask(__name__)
app.register_blueprint(monster_castle)


if __name__ == '__main__':
  app.run(debug=True)
