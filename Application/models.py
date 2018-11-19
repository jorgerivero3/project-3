from Application import db, login_manager, application
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime


@login_manager.user_loader # loads in user
def load_user(user_id):
	return User.query.get(int(user_id))

# Models
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Task', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(application.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(application.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}')"

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20))
	description = db.Column(db.String(200))
	complete = db.Column(db.Boolean, nullable=False, default=False)
	due = db.Column(db.DateTime, nullable=True)
	#duration = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

''' work out events later
class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20))
	text = db.Column(db.String(200))
	#time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
'''