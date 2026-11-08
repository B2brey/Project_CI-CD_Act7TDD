class Config:
    SECRET_KEY = "dev"


class DevelopmentConfig(Config):
    DEBUG = True


class testingconfig(Config):
    TESTING = True
