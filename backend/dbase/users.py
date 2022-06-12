import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID

from dbase import db


class UserAuthorized(db.Model):
    __tablename__ = "authorized_users"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    session_token = db.Column(db.String(16), unique=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    created_date = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.utcnow
    )

    def __init__(self, username, password, email, uuid, session_token):
        self.username = username
        self.password = password
        self.email = email
        self.uuid = uuid
        self.session_token = session_token
        self.created_date = datetime.datetime.now()

    def __repr__(self):
        return f"({self.username})[{self.uuid}]"


class UserAnon(db.Model):
    __tablename__ = "anon_users"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    session_token = db.Column(db.String(16), unique=True)
    created_date = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.utcnow
    )

    def __init__(self, username, uuid, session_token):
        self.username = username
        self.uuid = uuid
        self.session_token = session_token
        self.created_date = datetime.datetime.now()

    def __repr__(self):
        return f"({self.username})[{self.uuid}]"


class UserVector(db.Model):
    __tablename__ = "user_vectors"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    english = db.Column(db.ARRAY(db.Float), nullable=False)
    french = db.Column(db.ARRAY(db.Float), nullable=False)
    russian = db.Column(db.ARRAY(db.Float), nullable=False)
    ukrainian = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(self, uuid, english, french, russian, ukrainian):
        self.uuid = uuid
        self.english = english
        self.french = french
        self.russian = russian
        self.ukrainian = ukrainian

    def __repr__(self):
        repr = f"""[{self.uuid}]
        english: {self.english};
        french: {self.french};
        russian: {self.russian};
        ukrainian: {self.ukrainian};
        """
        return
