from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager, db
from application.forms import LoginForm
from application.models import User  

auth = Blueprint('auth', __name__)

ADMIN_EMAIL = "ksanjay034@gmail.com"
ADMIN_PASSWORD = "sanjay@2003"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password')  
        
        user = User.query.filter_by(email=email).first()  
        print(f"Attempting to log in user: {email}")
        
        if user:
            print(f"User found: {user.username}")
            if check_password_hash(user.password_hash, password):
                print("Password is correct.")
                login_user(user)
                flash('Login successful!', 'success') 

                if user.email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                    return redirect(url_for('main.show_all_users'))  
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                return redirect(url_for('main.show_users'))  
            else:
                print("Password is incorrect.")
        else:
            print("User not found.")

        flash('Login failed. Check your email and password.', 'danger')  

    return render_template('login.jinja2', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user() 
    flash('Logged out successfully!', 'info')  
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_hash = generate_password_hash(password)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')  
            return redirect(url_for('auth.signup'))

        try:
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Signed up successfully! Please log in.', 'success')  
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('An error occurred while signing up. Please try again.', 'danger')  
            print(f"Error during signup: {e}")

    return render_template('signup.jinja2')
