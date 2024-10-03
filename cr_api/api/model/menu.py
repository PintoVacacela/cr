from . import db
from .model import *


class ApplicationMenu(BasicModel):
    code = db.Column(db.String(4))
    name = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    code_parent = db.Column(db.String(4))
    position = db.Column(db.Integer)
    route = db.Column(db.String(100))
    profiles = db.relationship('Profile', secondary='profile_menus', back_populates='menus')


