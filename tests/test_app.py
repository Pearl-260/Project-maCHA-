import os

from app import create_app, db
from app.models import Contribution, Group, Member, Payout, User


def test_dashboard_shows_database_statistics():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(full_name="Jane Doe", email="jane@example.com", phone="0712345678")
        user.set_password("secret")
        db.session.add(user)

        group = Group(group_name="Group A", monthly_contribution=2000, meeting_day="Monday", max_members=10, status="Active")
        db.session.add(group)

        member = Member(full_name="John Doe", email="john@example.com", phone="0722222222", group_name="Group A", join_date="2026-01-01", status="Active")
        db.session.add(member)

        contribution = Contribution(member_name="John Doe", group_name="Group A", amount=1500, payment_date="2026-01-05", payment_status="Completed")
        db.session.add(contribution)

        payout = Payout(beneficiary_name="John Doe", group_name="Group A", amount=500, payout_date="2026-02-01", payment_method="Bank Transfer", status="Pending")
        db.session.add(payout)

        db.session.commit()

        client = app.test_client()
        response = client.get("/dashboard")

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Total Members" in html
        assert "1" in html
        assert "Total Groups" in html
        assert "Total Contributions" in html
        assert "KSh 1,500.00" in html
        assert "Total Payouts" in html
        assert "KSh 500.00" in html
        assert "Loan Summary" in html
        assert "Recent Activity" in html
        assert "John Doe" in html
