from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Users, Messages
from django.contrib import messages

# Create your views here.
def index(request):
	context = {
		'users': Users.objects.all()
	}
	return render(request,'dashboard/index.html', context)

def login(request):
	user = Users.objects.login(request.POST)
	if user[0]:
		u = Users.objects.get(email=request.POST['email'])
		request.session['auth'] = u.user_level
		request.session['id'] = u.id
		return redirect(reverse('dashboard_dashboard'))
	else:
		Users.objects.errormessage(request, user[1])
		return redirect(reverse('dashboard_index'))

def edit(request):
	return render(request,'dashboard/edit.html')
def update(request):
	validate = Users.objects.validate(request.POST)
	if validate[0]:
		Users.objects.adduser(request.POST)
		u = Users.objects.get(email=request.POST['email'])
		request.session['auth'] = u.user_level
		request.session['id'] = u.id
 		return redirect(reverse('dashboard_dashboard'))
 	else:
 		Users.objects.errormessage(request, validate[1])
 		return redirect(reverse('dashboard_index'))

def dashboard(request):
	context={
		'users': Users.objects.all()
	}
	return render(request,'dashboard/dashboard.html', context)

def show(request, userid):
	context={
		'users': Users.objects.filter(id=userid),
		'messages': Messages.objects.filter(show_id=userid).order_by('created_at'),
		'allusers': Users.objects.all()
	}
	u = Users.objects.get(id=userid)
	request.session['messageid'] = u.id
	return render(request,'dashboard/show.html', context)

def addmessage(request, messageid):
	Messages.objects.create(user_id=Users.objects.get(id=request.session['id']), message=request.POST['message'], show_id=request.session['messageid'])
	return redirect(reverse('dashboard_show', kwargs={'userid': request.session['messageid']}))

def edituser(request, userid):
	context={
		'users': Users.objects.filter(id=userid)
	}
	return render(request, 'dashboard/edituser.html', context)

def saveuser(request, userid):
	u = Users.objects.get(id=userid)
	u.first_name = request.POST['f_name']
	u.last_name = request.POST['l_name']
	u.email = request.POST['email']
	if request.POST['user_level'] == 'Admin':
		u.user_level = 9
	elif request.POST['user_level'] == 'Normal':
		u.user_level = 1
	u.save()
	return redirect(reverse('dashboard_dashboard'))

def logout(request):
	request.session.clear()
	return redirect(reverse('dashboard_index'))


