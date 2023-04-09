from setup_db import db
from marshmallow import Schema, fields



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(255))


class UserFullSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    name = fields.Str()
    status = fields.Str()