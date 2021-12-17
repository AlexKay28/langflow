from dbase import db


class TransitionShift(db.Model):
    __tablename__ = "transition_shift"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    language = db.Column(db.String, nullable=False)
    phrase_from = db.Column(db.Integer, nullable=False)
    phrase_to = db.Column(db.Integer, nullable=False)
    shift_vector = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(self, id, language, phrase_from, phrase_to, shift_vector):
        self.id = id
        self.language = language
        self.phrase_from = phrase_from
        self.phrase_to = phrase_to
        self.shift_vector = shift_vector

    def __repr__(self):
        return f"{language}, {phrase_from}, {phrase_to}, {shift_vector}"


class TransitionSuccess(db.Model):
    __tablename__ = "transition_success"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    language = db.Column(db.String, nullable=False)
    user_group = db.Column(db.Integer, nullable=False)
    phrase_from = db.Column(db.Integer, nullable=False)
    phrase_to = db.Column(db.Integer, nullable=False)
    n_updates = db.Column(db.Integer, nullable=True)
    average_success = db.Column(db.Float, nullable=True)

    def __init__(
        self,
        id,
        language,
        user_group,
        phrase_from,
        phrase_to,
        n_updates,
        average_success,
        transition_id,
    ):
        self.id = id
        self.language = language
        self.user_group = user_group
        self.phrase_from = phrase_from
        self.phrase_to = phrase_to
        self.n_updates = n_updates
        self.average_success = average_success

    def __repr__(self):
        return (
            f"{language}, {user_group}, {n_updates}, {average_success}, {transition_id}"
        )
