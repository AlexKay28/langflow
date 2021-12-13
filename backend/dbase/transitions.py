from dbase import db


class TransitionShift(db.Model):
    __tablename__ = "transition_shift"

    # columns
    transition_id = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String, nullable=False)
    phrase_from = db.Column(db.Integer, nullable=False)
    phrase_to = db.Column(db.Integer, nullable=False)
    shift_vector = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(self, transition_id, language, phrase_from, phrase_to, shift_vector):
        self.transition_id = transition_id
        self.language = language
        self.phrase_from = phrase_from
        self.phrase_to = phrase_to
        self.shift_vector = shift_vector

    def __repr__(self):
        return (
            f"{transition_id}, {language}, {phrase_from}, {phrase_to}, {shift_vector}"
        )


class TransitionSuccess(db.Model):
    __tablename__ = "transition_success"

    # columns
    transition_id = db.Column(db.Integer)
    user_group = db.Column(db.Integer, nullable=False)
    n_updates = db.Column(db.Integer, nullable=True)
    average_success = db.Column(db.Float, nullable=True)

    def __init__(self, user_group, n_updates, average_success, transition_id):
        self.user_group = user_group
        self.n_updates = n_updates
        self.average_success = average_success
        self.transition_id = transition_id

    def __repr__(self):
        return f"{user_group}, {n_updates}, {average_success}, {transition_id}"
