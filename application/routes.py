from flask import request, render_template, redirect, url_for, Blueprint, flash
from .forms import CreateUserForm, LoginForm, DeleteUserForm
from .models import User, UserData
from . import db
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__, template_folder='templates')

ADMIN_EMAIL = "ksanjay034@gmail.com"
ADMIN_PASSWORD = "sanjay@2003"

@main.route('/home')
@login_required
def home():
    if current_user.email == ADMIN_EMAIL:
        users = User.query.all()  
    else:
        users = UserData.query.filter_by(user_id=current_user.id).all() 
    return render_template('users.jinja2', user=current_user, users=users)

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.email == ADMIN_EMAIL:
            return redirect(url_for('main.show_all_users')) 
        return redirect(url_for('main.show_users')) 
    return render_template('login.jinja2')

@main.route('/show_users')
@login_required
def show_users():
    user_data = UserData.query.filter_by(user_id=current_user.id).all()
    form = DeleteUserForm()
    if not user_data:
        flash('No user data found in the database.', 'info')
    return render_template('your_data.jinja2', users=user_data, form=form, title="Your Data")

@main.route('/show_all_users')
@login_required
def show_all_users():
    if current_user.email == ADMIN_EMAIL:
        all_users = User.query.all()
        form = CreateUserForm()
        return render_template('users.jinja2', users=all_users, form=form, title="All Users")
    else:
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for('main.index'))

@main.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.create_user'))

        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(email=form.email.data, 
                        username=form.username.data, 
                        password_hash=hashed_password, 
                        about_user=form.about_user.data)
        db.session.add(new_user)
        
        try:
            db.session.commit()

            user_data = UserData(user_id=new_user.id, about=form.about_user.data)
            db.session.add(user_data)
            db.session.commit()

            flash('User created successfully!', 'success')
            return redirect(url_for('main.show_users')) 
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the user. Please try again.', 'danger')
    
    return render_template('create_user.jinja2', form=form)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)

    if current_user.email == ADMIN_EMAIL or user_to_delete.id == current_user.id:
        try:
            UserData.query.filter_by(user_id=user_to_delete.id).delete() 
            db.session.commit()
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback() 
            flash('Error occurred while deleting user.', 'danger')
            print(f"Error: {e}")
    else:
        flash('You do not have permission to delete this user.', 'danger')

    if current_user.email == ADMIN_EMAIL:
        return redirect(url_for('main.show_all_users'))  
    else:
        return redirect(url_for('main.show_users'))  

@main.route('/your_data')
@login_required
def your_data():
    if current_user.email == ADMIN_EMAIL:
        return redirect(url_for('main.show_all_users'))
    user_data = UserData.query.filter_by(user_id=current_user.id).all()
    if not user_data:
        flash('No user data found in the database.', 'info')
    return render_template('your_data.jinja2', user_data=user_data)  

