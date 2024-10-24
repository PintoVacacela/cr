from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .model import *
from .menu import *
from .user import *
from .profile import *
from .client import *
from .client_service import *
from .product import *
from .notification import *



