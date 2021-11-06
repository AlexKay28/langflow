import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID

from dbase import db


class Action(db.Model):
    __tablename__ = "actions"

    uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("anon_users.uuid"))
    quid = db.Column(UUID(as_uuid=True), primary_key=True)
    quid_token = db.Column(db.String(16), unique=True, nullable=False)
    phrase_id = db.Column(db.Integer, db.ForeignKey("phrases.id"))
    level = db.Column(db.Integer)
    first_language = db.Column(db.String(16), nullable=False)
    second_language = db.Column(db.String(16), nullable=False)
    user_answer = db.Column(db.String(256), nullable=True)
    score = db.Column(db.Float)
    action_date = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.utcnow
    )

    def __init__(
        self,
        uuid,
        quid,
        quid_token,
        phrase_id,
        level,
        first_language,
        second_language,
        user_answer,
        score,
    ):
        self.uuid = uuid
        self.quid = quid
        self.quid_token = quid_token
        self.phrase_id = phrase_id
        self.level = level
        self.first_language = first_language
        self.second_language = second_language
        self.user_answer = user_answer
        self.score = score
        self.action_date = datetime.datetime.now()

    def __repr__(self):
        return f"{uuid}:{quid}[{first_language}-{second_language}]({phrase_id})"
