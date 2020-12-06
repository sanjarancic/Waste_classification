import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    address = db.Column(db.String)
    score = db.Column(db.Integer)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, password, address, score):
        self.username = username
        self.password = self.__generate_hash(password)
        self.address = address
        self.score = score

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'address': self.address,
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

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    mail = db.Column(db.String)
    site = db.Column(db.String)
    score = db.Column(db.Integer)
    waste_created = db.Column(db.String)
    waste_created_quantity = db.Column(db.Float)
    waste_required = db.Column(db.String)
    waste_required_quantity = db.Column(db.Float)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, password, mail, site, score, waste_created, waste_created_quantity, waste_required, waste_required_quantity):
        self.username = username
        self.password = self.__generate_hash(password)
        self.mail = mail
        self.site = site
        self.score = score
        self.waste_created = waste_created
        self.waste_created_quantity = waste_created_quantity
        self.waste_required = waste_required
        self.waste_required_quantity = waste_required_quantity

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def identity(payload):
        user_id = payload['identity']
        return Company.get(user_id, None)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'mail': self.mail,
            'site': self.site,
            'score': self.score,
            'waste_created': self.waste_created,
            'waste_created_quantity': self.waste_created_quantity,
            'waste_required': self.waste_required,
            'waste_required_quantity': self.waste_required_quantity
        }

    @staticmethod
    def get_by_username(value):
        return Company.query.filter(Company.username == value).first()

    @staticmethod
    def get_by_id(value):
        return Company.query.filter(Company.id == value).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
