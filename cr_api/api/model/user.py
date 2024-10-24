from . import db
from enum import Enum
from .model import *

class UserState(Enum):
    ACTIVO = 1
    INACTIVO = 2
    REGISTRADO = 3



class ApplicationUser(BasicModel):
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastname = db.Column(db.String(100))     
    documentType_id = db.Column(db.Integer, db.ForeignKey("document_type.id"))
    documentType = db.relationship("DocumentType", back_populates="users")
    identification = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    designation = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(15), nullable=False)
    userState = db.Column(db.Enum(UserState), default='REGISTRADO')
    userType_id = db.Column(db.Integer, db.ForeignKey("user_type.id"))
    userType = db.relationship("UserType", back_populates="users")
    photo_url = db.Column(db.String(200))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    profile = db.relationship("Profile", back_populates="users")
    notifications = db.relationship('UserNotification')
    events = db.relationship('Event', secondary='event_user', back_populates='users')
    



class UserType(BasicModel):
    name = db.Column(db.String(50))
    users = db.relationship('ApplicationUser')
    profiles = db.relationship('Profile', secondary='profile_user_types', back_populates='userTypes')

class DocumentType(BasicModel):
    name = db.Column(db.String(50))
    users = db.relationship('ApplicationUser')








