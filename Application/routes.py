from flask import render_template, url_for, flash, redirect, request
from Application import application, db, bcrypt, mail
from Application.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateInfo, NewItem
from Application.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime, timedelta
import random
import sys


@application.route('/')
def home():
	return render_template('/home.html', title='Home')

@application.route('/about')
def about():
	return render_template('/about.html', title='About')

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

######################
##### TO-DO LIST #####
######################

@application.route('/todo_list')
@login_required
def ToDoList():
	page = request.args.get('page', 1, type=int)
	tasks = Task.query.filter_by(author=current_user)\
	.order_by(Task.due.asc())\
	.paginate(page=page, per_page=8)
	return render_template('/todo_list.html', title='ToDoList', tasks=tasks, user=current_user)

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

@application.route("/task/<int:task_id>/delete", methods=['GET'])
@login_required
def delete_task(task_id):
	post = Task.query.get_or_404(task_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Task Deleted', 'success')
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

@application.route("/view/<int:task_id>")
def view(task_id):
	post = Task.query.get_or_404(task_id)
	if post.author != current_user:
		abort(403)
	return render_template('post.html', title=post.title, post=post)

####################
##### CALENDAR #####
####################

@application.route('/calendar')
@login_required
def cal():
	titles = []
	ids = []
	times = []
	for task in current_user.posts:
		if task.due != None:
			titles.append(task.title)
			ids.append(task.id)
			hour = str(task.due.hour)
			minute = str(task.due.minute)
			day = str(task.due.day)
			month = str(task.due.month)
			if task.due.hour < 10:
				hour = '0' + str(task.due.hour)
			if task.due.minute < 10:
				minute = '0' + str(task.due.minute)
			if task.due.day < 10:
				day = '0' + str(task.due.day)
			if task.due.month < 10:
				month = '0' + str(task.due.month)
			times.append(str(task.due.year)+'-'+month+'-'+day+'T'+hour+':'+minute+":00")
	return render_template('calendar.html', titles=titles, ids=ids, times=times)

#########################
##### NOTIFICATIONS #####
#########################

# takes advantage of ajax
@application.route('/notifs', methods=['GET'])
@login_required
def notif():
	response = ""
	for task in current_user.posts:
		if task.due != None:# and task.complete == False:
			dif = int((task.due - datetime.now()).total_seconds() * 1000) + 21600000
			if dif > 0:
				response += task.title+"-"+str(dif)+"-"
	if response != "":
		response = response[:-1]
		return response
	return ' '
