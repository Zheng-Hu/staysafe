"""StaySafe development configuration."""

import pathlib
import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
STAYSAFE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = STAYSAFE_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/staysafe.sqlite3
DATABASE_FILENAME = STAYSAFE_ROOT/'var'/'staysafe.sqlite3'
