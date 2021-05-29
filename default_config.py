import os

DEBUG = True

SECRET_KEY = "whoops-secret-key"

SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

PROPAGATE_EXCEPTIONS = True

# root folder of all the uploads
UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True

# allow blacklisting for access and refresh tokens
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
