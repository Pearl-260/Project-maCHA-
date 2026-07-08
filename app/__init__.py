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

    return app
