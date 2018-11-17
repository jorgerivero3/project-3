from Application import db, login_manager, application
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# Association Tables

friends = db.Table('friends', 
	db.Column('self_id', db.Integer, db.ForeignKey('user.id')), 
	db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
	)

# Models 

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20))
	text = db.Column(db.String(200))
	complete = db.Column(db.Boolean)
	due = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	duration = db.Column(db.Integer, primary_key=True)

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20))
	text = db.Column(db.String(200))
	time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


	

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
		return f"User('{self.username}'')"



