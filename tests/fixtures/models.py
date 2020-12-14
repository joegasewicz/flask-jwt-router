from tests.fixtures.main_fixture import db


class TeacherModel(db.Model):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
