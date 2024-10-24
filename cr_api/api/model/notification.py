from . import db
from .model import *
from sqlalchemy import func

class type(Enum):
    WARNING = 1
    DANGER = 2
    INFO = 3


class UserNotification(BasicModel):
    type = db.Column(db.Enum(type), default='INFO')
    title = db.Column(db.String(200))
    message = db.Column(db.String(500))
    opened = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("application_user.id"))
    user = db.relationship("ApplicationUser", back_populates="notifications")