from ui.blueprints.app import sqldb


class User(sqldb.Model):
  # TODO: {flag, guild}
  id = sqldb.Column(sqldb.Integer, primary_key=True)
  name = sqldb.Column(sqldb.String(50), nullable=False)
  token = sqldb.Column(sqldb.String(45), nullable=False)


# class Guild(db.Model):
#     # TODO: flag, guildID
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
