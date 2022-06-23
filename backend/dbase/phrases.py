from dbase import db


class Phrase(db.Model):
    __tablename__ = "phrases"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    level = db.Column(db.Integer)
    english = db.Column(db.String(256), nullable=False)
    french = db.Column(db.String(256), nullable=False)
    russian = db.Column(db.String(256), nullable=False)
    ukrainian = db.Column(db.String(256), nullable=False)

    def __init__(
        self,
        id,
        level,
        english,
        french,
        russian,
        ukrainian,
    ):
        self.id = id
        self.level = level
        self.english = english
        self.french = french
        self.russian = russian
        self.ukrainian = ukrainian

    def __repr__(self):
        return f"entity: ( id, level, [language, vector] * n_langs )"


class PhraseVector(db.Model):
    __tablename__ = "phrases_vec"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    english = db.Column(db.ARRAY(db.Float), nullable=False)
    french = db.Column(db.ARRAY(db.Float), nullable=False)
    russian = db.Column(db.ARRAY(db.Float), nullable=False)
    ukrainian = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(
        self,
        id,
        english,
        french,
        russian,
        ukrainian,
    ):
        self.id = id
        self.english = english
        self.french = french
        self.russian = russian
        self.ukrainian = ukrainian

    def __repr__(self):
        return f"({self.id})[vec shape: {self.english.shape}]"
