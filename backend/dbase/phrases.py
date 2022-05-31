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
    __tablename__ = "phrases_vecs"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    english_vec = db.Column(db.ARRAY(db.Float), nullable=False)
    french_vec = db.Column(db.ARRAY(db.Float), nullable=False)
    russian_vec = db.Column(db.ARRAY(db.Float), nullable=False)
    ukrainian_vec = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(
        self,
        id,
        level,
        english_vec,
        french_vec,
        russian_vec,
        ukrainian_vec,
    ):
        self.id = id
        self.english_vec = english_vec
        self.french_vec = french_vec
        self.russian_vec = russian_vec
        self.ukrainian_vec = ukrainian_vec

    def __repr__(self):
        return f"({self.id})[vec shape: {self.english_vec.shape}]"
