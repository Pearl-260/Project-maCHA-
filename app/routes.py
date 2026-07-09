from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Contribution, Group, Member, Payout, User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password", "error")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash("Login successful", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password", "error")

    return render_template("login.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("Please fill in the required fields", "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists", "error")
            return render_template("register.html")

        user = User(full_name=full_name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/dashboard")
def dashboard():
    member_count = Member.query.count()
    group_count = Group.query.count()
    contribution_count = Contribution.query.count()
    payout_count = Payout.query.count()
    contribution_total = db.session.query(db.func.coalesce(db.func.sum(Contribution.amount), 0)).scalar() or 0
    payout_total = db.session.query(db.func.coalesce(db.func.sum(Payout.amount), 0)).scalar() or 0
    pending_payout_count = Payout.query.filter_by(status="Pending").count()
    loan_count = 0
    loan_total = 0.0

    current_user = User.query.order_by(User.id.asc()).first()
    profile_name = current_user.full_name if current_user else "Administrator"
    profile_initials = "".join(part[0].upper() for part in profile_name.split()[:2]) if profile_name else "AD"

    recent_activities = []
    latest_member = Member.query.order_by(Member.id.desc()).first()
    latest_group = Group.query.order_by(Group.id.desc()).first()
    latest_contribution = Contribution.query.order_by(Contribution.id.desc()).first()
    latest_payout = Payout.query.order_by(Payout.id.desc()).first()

    if latest_member:
        recent_activities.append({"title": f"{latest_member.full_name} joined the chama", "meta": latest_member.join_date or "Recently added"})
    if latest_group:
        recent_activities.append({"title": f"{latest_group.group_name} is active", "meta": f"Max members: {latest_group.max_members}"})
    if latest_contribution:
        recent_activities.append({"title": f"Contribution recorded for {latest_contribution.member_name}", "meta": f"KSh {latest_contribution.amount:,.2f}"})
    if latest_payout:
        recent_activities.append({"title": f"Payout queued for {latest_payout.beneficiary_name}", "meta": f"Status: {latest_payout.status}"})

    if not recent_activities:
        recent_activities.append({"title": "No activity yet", "meta": "Create members, groups, contributions, or payouts to see updates here."})

    return render_template(
        "dashboard.html",
        member_count=member_count,
        group_count=group_count,
        contribution_count=contribution_count,
        payout_count=payout_count,
        contribution_total=contribution_total,
        payout_total=payout_total,
        pending_payout_count=pending_payout_count,
        loan_count=loan_count,
        loan_total=loan_total,
        recent_activities=recent_activities,
        profile_name=profile_name,
        profile_initials=profile_initials,
    )


@main.route("/members")
def members():
    members = Member.query.order_by(Member.id.desc()).all()
    return render_template("members.html", members=members)


@main.route("/add-member", methods=["GET", "POST"], endpoint="add_member")
def add_member():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        group_name = request.form.get("group", "").strip()
        join_date = request.form.get("join_date", "").strip()
        status = request.form.get("status", "Active").strip()

        if not full_name or not email:
            flash("Please provide both name and email", "error")
            return render_template("add_member.html")

        if Member.query.filter_by(email=email).first():
            flash("A member with that email already exists", "error")
            return render_template("add_member.html")

        member = Member(
            full_name=full_name,
            email=email,
            phone=phone,
            group_name=group_name,
            join_date=join_date,
            status=status,
        )
        db.session.add(member)
        db.session.commit()

        flash("Member added successfully", "success")
        return redirect(url_for("main.members"))

    return render_template("add_member.html")


@main.route("/groups")
def groups():
    groups = Group.query.order_by(Group.id.desc()).all()
    return render_template("groups.html", groups=groups)


@main.route("/add-group", methods=["GET", "POST"], endpoint="add_group")
def add_group():
    if request.method == "POST":
        group_name = request.form.get("group_name", "").strip()
        monthly_contribution = float(request.form.get("monthly_contribution", 0) or 0)
        meeting_day = request.form.get("meeting_day", "").strip()
        max_members = int(request.form.get("max_members", 0) or 0)
        status = request.form.get("status", "Active").strip()

        if not group_name:
            flash("Please provide a group name", "error")
            return render_template("add_group.html")

        group = Group(
            group_name=group_name,
            monthly_contribution=monthly_contribution,
            meeting_day=meeting_day,
            max_members=max_members,
            status=status,
        )
        db.session.add(group)
        db.session.commit()

        flash("Group added successfully", "success")
        return redirect(url_for("main.groups"))

    return render_template("add_group.html")


@main.route("/contributions")
def contributions():
    contributions = Contribution.query.order_by(Contribution.id.desc()).all()
    return render_template("contributions.html", contributions=contributions)


@main.route("/contributions/<int:contribution_id>/edit", methods=["GET", "POST"], endpoint="edit_contribution")
def edit_contribution(contribution_id):
    contribution = Contribution.query.get_or_404(contribution_id)
    members = Member.query.order_by(Member.full_name.asc()).all()
    groups = Group.query.order_by(Group.group_name.asc()).all()

    if request.method == "POST":
        member_name = request.form.get("member", "").strip()
        group_name = request.form.get("group", "").strip()
        amount = float(request.form.get("amount", 0) or 0)
        payment_date = request.form.get("payment_date", "").strip()
        payment_status = request.form.get("payment_status", "Completed").strip()

        if not member_name or not group_name or not payment_date:
            flash("Please complete the contribution details", "error")
            return render_template("edit_contribution.html", contribution=contribution, members=members, groups=groups)

        member_exists = Member.query.filter_by(full_name=member_name).first()
        group_exists = Group.query.filter_by(group_name=group_name).first()
        if not member_exists or not group_exists:
            flash("Please select a valid member and group", "error")
            return render_template("edit_contribution.html", contribution=contribution, members=members, groups=groups)

        contribution.member_name = member_name
        contribution.group_name = group_name
        contribution.amount = amount
        contribution.payment_date = payment_date
        contribution.payment_status = payment_status
        db.session.commit()

        flash("Contribution updated successfully", "success")
        return redirect(url_for("main.contributions"))

    return render_template("edit_contribution.html", contribution=contribution, members=members, groups=groups)


@main.route("/contributions/<int:contribution_id>/delete", methods=["POST"], endpoint="delete_contribution")
def delete_contribution(contribution_id):
    contribution = Contribution.query.get_or_404(contribution_id)
    db.session.delete(contribution)
    db.session.commit()
    flash("Contribution deleted successfully", "success")
    return redirect(url_for("main.contributions"))


@main.route("/add-contribution", methods=["GET", "POST"], endpoint="add_contribution")
def add_contribution():
    members = Member.query.order_by(Member.full_name.asc()).all()
    groups = Group.query.order_by(Group.group_name.asc()).all()

    if request.method == "POST":
        member_name = request.form.get("member", "").strip()
        group_name = request.form.get("group", "").strip()
        amount = float(request.form.get("amount", 0) or 0)
        payment_date = request.form.get("payment_date", "").strip()
        payment_status = request.form.get("payment_status", "Completed").strip()

        if not member_name or not group_name or not payment_date:
            flash("Please complete the contribution details", "error")
            return render_template("add_contribution.html", members=members, groups=groups)

        member_exists = Member.query.filter_by(full_name=member_name).first()
        group_exists = Group.query.filter_by(group_name=group_name).first()
        if not member_exists or not group_exists:
            flash("Please select a valid member and group", "error")
            return render_template("add_contribution.html", members=members, groups=groups)

        contribution = Contribution(
            member_name=member_name,
            group_name=group_name,
            amount=amount,
            payment_date=payment_date,
            payment_status=payment_status,
        )
        db.session.add(contribution)
        db.session.commit()

        flash("Contribution recorded successfully", "success")
        return redirect(url_for("main.contributions"))

    return render_template("add_contribution.html", members=members, groups=groups)


@main.route("/reports")
def reports():
    return render_template("reports.html")


@main.route("/payouts")
def payouts():
    payouts = Payout.query.order_by(Payout.id.desc()).all()
    return render_template("payouts.html", payouts=payouts)


@main.route("/payouts/<int:payout_id>/edit", methods=["GET", "POST"], endpoint="edit_payout")
def edit_payout(payout_id):
    payout = Payout.query.get_or_404(payout_id)
    members = Member.query.order_by(Member.full_name.asc()).all()
    groups = Group.query.order_by(Group.group_name.asc()).all()

    if request.method == "POST":
        beneficiary_name = request.form.get("beneficiary", "").strip()
        group_name = request.form.get("group", "").strip()
        amount = float(request.form.get("amount", 0) or 0)
        payout_date = request.form.get("payout_date", "").strip()
        payment_method = request.form.get("payment_method", "Bank Transfer").strip()
        status = request.form.get("status", "Pending").strip()

        if not beneficiary_name or not group_name or not payout_date:
            flash("Please complete the payout details", "error")
            return render_template("edit_payout.html", payout=payout, members=members, groups=groups)

        member_exists = Member.query.filter_by(full_name=beneficiary_name).first()
        group_exists = Group.query.filter_by(group_name=group_name).first()
        if not member_exists or not group_exists:
            flash("Please select a valid member and group", "error")
            return render_template("edit_payout.html", payout=payout, members=members, groups=groups)

        payout.beneficiary_name = beneficiary_name
        payout.group_name = group_name
        payout.amount = amount
        payout.payout_date = payout_date
        payout.payment_method = payment_method
        payout.status = status
        db.session.commit()

        flash("Payout updated successfully", "success")
        return redirect(url_for("main.payouts"))

    return render_template("edit_payout.html", payout=payout, members=members, groups=groups)


@main.route("/payouts/<int:payout_id>/delete", methods=["POST"], endpoint="delete_payout")
def delete_payout(payout_id):
    payout = Payout.query.get_or_404(payout_id)
    db.session.delete(payout)
    db.session.commit()
    flash("Payout deleted successfully", "success")
    return redirect(url_for("main.payouts"))


@main.route("/add-payout", methods=["GET", "POST"], endpoint="add_payout_page")
def add_payout_page():
    members = Member.query.order_by(Member.full_name.asc()).all()
    groups = Group.query.order_by(Group.group_name.asc()).all()

    if request.method == "POST":
        beneficiary_name = request.form.get("beneficiary", "").strip()
        group_name = request.form.get("group", "").strip()
        amount = float(request.form.get("amount", 0) or 0)
        payout_date = request.form.get("payout_date", "").strip()
        payment_method = request.form.get("payment_method", "Bank Transfer").strip()
        status = request.form.get("status", "Pending").strip()

        if not beneficiary_name or not group_name or not payout_date:
            flash("Please complete the payout details", "error")
            return render_template("add_payout.html", members=members, groups=groups)

        member_exists = Member.query.filter_by(full_name=beneficiary_name).first()
        group_exists = Group.query.filter_by(group_name=group_name).first()
        if not member_exists or not group_exists:
            flash("Please select a valid member and group", "error")
            return render_template("add_payout.html", members=members, groups=groups)

        if amount <= 0:
            member_contributions = Contribution.query.filter_by(member_name=beneficiary_name, group_name=group_name).all()
            amount = sum(item.amount for item in member_contributions)

        payout = Payout(
            beneficiary_name=beneficiary_name,
            group_name=group_name,
            amount=amount,
            payout_date=payout_date,
            payment_method=payment_method,
            status=status,
        )
        db.session.add(payout)
        db.session.commit()

        flash("Payout saved successfully", "success")
        return redirect(url_for("main.payouts"))

    return render_template("add_payout.html", members=members, groups=groups)


@main.route("/notifications")
def notifications():
    return render_template("notifications.html")


@main.route("/send-notification")
def send_notification_page():
    return render_template("send_notification.html")


@main.route("/settings")
def settings():
    return render_template("settings.html")


@main.route("/logout")
def logout():
    return redirect(url_for("main.login"))
