class BaseConfig:
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
  DEBUG = True


class ProductionConfig(BaseConfig):
  pass
