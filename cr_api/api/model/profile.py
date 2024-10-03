
from . import db
from .model import *

class Profile(BasicModel):
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('ApplicationUser')
    menus = db.relationship('ApplicationMenu', secondary='profile_menus', back_populates='profiles')
    userTypes = db.relationship('UserType', secondary='profile_user_types', back_populates='profiles')


class ProfileMenus(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id') ,primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('application_menu.id') ,primary_key=True)

class ProfileUserTypes(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id') ,primary_key=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id') ,primary_key=True)
