from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsersManager(models.Manager):
	def validate(self, post):
		if len(post['f_name']) < 2:
			return (False, 'error1')
		elif len(post['l_name']) < 2:
			return (False, 'error2')
		elif len(post['email']) < 1:
			return (False, 'error3')
		elif not EMAIL_REGEX.match(post['email']):
			return (False, 'error4')
		elif len(post['password']) < 8:
			return (False, 'error5')
		elif post['password'] != post['c_password']:
			return (False, 'error6')
		try:
			if Users.objects.filter(email=post['email'])[0]:
				return (False, 'error7')
		except:
			return (True, post['email'])

	def adduser(self, post):
		try:
			Users.objects.get(id=1)
			Users.objects.create(first_name=post['f_name'], last_name=post['l_name'], email=post['email'], password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt(12)), user_level=1)
		except:
			Users.objects.create(first_name=post['f_name'], last_name=post['l_name'], email=post['email'], password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt(12)), user_level=9)
	def errormessage(self,request, error):
		errorlist={
			'error1': 'Name must be at least 2 characters',
			'error2': 'Alias must be at least 2 characters',
			'error3': 'Email field must be entered',
			'error4': 'Email must match standard format. (ex: 123@abc.xyz)',
			'error5': 'Password must be at least 8 characters',
			'error6': 'Passwords must match',
			'error7': 'That Email is already registered',
			'error8': 'Wrong Email or Password'
		}
		messages.add_message(request, messages.ERROR, errorlist[error])

	def login(self, post):
		try:
			user = Users.objects.get(email=post['email'])
			if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password.encode():
				return (True, user.id)
		except:
			return (False, 'error8')

# Create your models here.
class Users(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	user_level = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UsersManager()

class Messages(models.Model):
	user_id = models.ForeignKey(Users)
	show_id = models.CharField(max_length=3, default=2)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)