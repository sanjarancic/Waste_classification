import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    adress = db.Column(db.String)
    score = db.Column(db.Integer)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, password, adress, score):
        self.username = username
        self.password = self.__generate_hash(password)
        self.adress = adress
        self.score = score

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'adress': self.adress,
            'score': self.score
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_username(value):
        return User.query.filter(User.username == value).first()

    @staticmethod
    def get_by_id(value):
        return User.query.filter(User.id == value).first()
