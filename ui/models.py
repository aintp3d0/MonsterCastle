from ui.app import sqldb


class MC_User(sqldb.Model):
  # TODO
  # - flag
  # - guild.id
  # - fixed strings length
  id = sqldb.Column(sqldb.Integer, primary_key=True)
  openid = sqldb.Column(sqldb.String(20), nullable=False)
  username = sqldb.Column(sqldb.String(50))
  image_hash = sqldb.Column(sqldb.String(32), nullable=False)


# class Guild(db.Model):
#     # TODO: flag, guildID
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
