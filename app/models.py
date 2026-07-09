from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    __table_args__ = {"sqlite_autoincrement": True}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.full_name}>"


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    monthly_contribution = db.Column(db.Float, nullable=False, default=0.0)
    meeting_day = db.Column(db.String(50), nullable=False)
    max_members = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="Active")

    def __repr__(self):
        return f"<Group {self.group_name}>"


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    group_name = db.Column(db.String(100), nullable=True)
    join_date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Active")

    def __repr__(self):
        return f"<Member {self.full_name}>"


class Contribution(db.Model):
    __tablename__ = "contributions"

    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_date = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default="Completed")

    def __repr__(self):
        return f"<Contribution {self.member_name}: {self.amount}>"


class Payout(db.Model):
    __tablename__ = "payouts"

    id = db.Column(db.Integer, primary_key=True)
    beneficiary_name = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    payout_date = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default="Bank Transfer")
    status = db.Column(db.String(20), nullable=False, default="Pending")

    def __repr__(self):
        return f"<Payout {self.beneficiary_name}: {self.amount}>"

