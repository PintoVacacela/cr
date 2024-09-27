from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .model import *
from .menu import *
from .user import *
from .profile import *
from .client import *




