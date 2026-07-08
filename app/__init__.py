from flask import Flask, render_template, request, redirect, url_for


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            print('Login submitted:', email, password)
            return redirect(url_for('dashboard'))

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')

            print('Registration submitted:', full_name, email, phone, password)
            return redirect(url_for('home'))

        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/members')
    def members():
        return render_template('members.html')

    @app.route('/add-member')
    def add_member_page():
        return render_template('add_member.html')

    @app.route('/groups')
    def groups():
        return render_template('groups.html')

    @app.route('/add-group')
    def add_group_page():
        return render_template('add_group.html')

    @app.route('/contributions')
    def contributions():
        return render_template('contributions.html')

    @app.route('/add-contribution')
    def add_contribution_page():
        return render_template('add_contribution.html')

    @app.route('/reports')
    def reports():
        return render_template('reports.html')

    @app.route('/payouts')
    def payouts():
        return render_template('payouts.html')

    @app.route('/add-payout')
    def add_payout_page():
        return render_template('add_payout.html')

    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html')

    @app.route('/send-notification')
    def send_notification_page():
        return render_template('send_notification.html')

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @app.route('/logout')
    def logout():
        # Clear user session (placeholder - actual session logic to be added with authentication)
        return redirect(url_for('login'))

    return app
