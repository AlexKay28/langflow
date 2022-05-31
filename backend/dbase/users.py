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
    __tablename__ = "user_vecrors"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)

    def __init__(self, uuid, english_vec, french_vec, russian_vec, ukrainian_vec):
        self.uuid = uuid
        self.english_vec = english_vec
        self.french_vec = french_vec
        self.russian_vec = russian_vec
        self.ukrainian_vec = ukrainian_vec

    def __repr__(self):
        repr = f"""[{self.uuid}]
        english_vec: {self.english_vec};
        french_vec: {self.french_vec};
        russian_vec: {self.russian_vec};
        ukrainian_vec: {self.ukrainian_vec};
        """
        return
