from flask import render_template, url_for, flash, redirect, request
from Application import application, db, bcrypt, mail
from Application.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateInfo, NewItem
from Application.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import sys
import random


@application.route('/')
def home():
	return render_template('/home.html', title='Home')

@application.route('/about')
def about():
	return render_template('/about.html', title='About')

@application.route('/todo_list')
@login_required
def ToDoList():
	page = request.args.get('page', 1, type=int)
	tasks = Task.query.filter_by(author=current_user)\
	.order_by(Task.id.asc())\
	.paginate(page=page, per_page=10)
	return render_template('/todo_list.html', title='ToDoList', tasks=tasks, user=current_user)

@application.route('/calendar')
@login_required
def calendar():
	return render_template('/calendar.html', title='Calendar')

@application.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account creation succesful!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@application.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessful. Email and/or password incorrect.')
	return render_template('login.html', title='Login', form=form)

@application.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateInfo()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Info Updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account Information', form=form)

@application.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@application.route("/password_retrieval", methods=['GET', 'POST'])
def password_retrieval():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('login'))
	return render_template('password_retrieval.html', title='Reset Password', form=form)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f''' To reset your password, click the following link, or copy and paste it into your web browser: {url_for('reset_token', token=token, _external=True)} If you did not make this request then please ignore this email.'''
	mail.send(msg)

@application.route("/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('The reset token you are using is invalid or expired.')
		return redirect(url_for('password_retrieval'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Password has been updated.', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)

@application.route("/task/new", methods=['GET', 'POST'])
@login_required
def taskListing():
	form = NewItem()
	if form.validate_on_submit():
		post = Task(title=form.title.data, description=form.description.data, due=form.due.data, user=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash("Item Created", "success")
		return redirect(url_for('ToDoList'))
	return render_template('newItem.html', title='New Listing', form=form, legend="New Listing")

''' taken from project 0
@application.route("/listings/new", methods=['GET', 'POST'])
@login_required
def itemListing():
	form = newItem()
	if form.validate_on_submit():
		_, f_ext = os.path.splitext(form.itemPic.data.filename)
		post = Post(itemName=form.itemName.data, description=form.description.data, itemPrice=form.itemPrice.data, user=current_user.id, ext=f_ext)
		db.session.add(post)
		db.session.commit()
		save_pic(form.itemPic.data, str(post.id), f_ext)
		flash('Item Listed!', 'success')
		return redirect(url_for('home'))
	return render_template("newItem.html", title="New Item Listing", form=form, legend='New Listing')
'''

@application.route("/task/<int:task_id>/delete", methods=['GET'])
@login_required
def delete_task(task_id):
	post = Task.query.get_or_404(task_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Task Deleted', 'succss')
	return redirect(url_for('ToDoList'))

@application.route("/task/<int:task_id>/complete", methods=['GET'])
@login_required
def complete_task(task_id):
	post = Task.query.get_or_404(task_id)
	if post.author != current_user:
		abort(403)
	if post.complete:
		post.complete = False
	else:
		post.complete = True
	db.session.commit()
	return redirect(url_for('ToDoList'))
