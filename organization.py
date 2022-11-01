import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db

class Organization(db.Model):
    __tablename__ = "Organization"
    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    # users = db.relationship('User', backref='organization', lazy=True)
    
    def __init__(self, name, phone, city, state, active):
        self.name = name
        self.phone = phone
        self.city = city
        self.state = state
        self.active = active

