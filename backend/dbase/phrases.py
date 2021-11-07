from dbase import db


def update_data_csv(table):
    db.session.query(Phrase).delete()

    for id, row in table.iterrows():
        phrase = Phrase(
            id=id,
            level=row["level"],
            english=row["english"],
            french=row["french"],
            russian=row["russian"],
            ukrainian=row["ukrainian"],
        )
        db.session.add(phrase)
        db.session.commit()
    return 1


class Phrase(db.Model):
    __tablename__ = "phrases"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    level = db.Column(db.Integer)
    english = db.Column(db.String(256), nullable=False)
    french = db.Column(db.String(256), nullable=False)
    russian = db.Column(db.String(256), nullable=False)
    ukrainian = db.Column(db.String(256), nullable=False)

    def __init__(self, id, level, english, french, russian, ukrainian):
        self.id = id
        self.level = level
        self.english = english
        self.french = french
        self.russian = russian
        self.ukrainian = ukrainian

    def __repr__(self):
        return f"({english}]"
