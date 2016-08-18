from django.conf.urls import url
from . import views           

urlpatterns = [
url(r'^$', views.index, name='dashboard_index'),
url(r'^login$', views.login, name='dashboard_login'), 
url(r'^dashboard/edit$', views.edit, name='dashboard_edit'),  
url(r'^dashboard/update$', views.update, name='dashboard_update'),
url(r'^dashboard/dashboard$', views.dashboard, name='dashboard_dashboard'),
url(r'^dashboard/show/user/(?P<userid>\d+)$', views.show, name='dashboard_show'),
url(r'^dashboard/addmessage/(?P<messageid>\d+)$', views.addmessage, name='dashboard_addmessage'),
url(r'^dashboard/user/edit/(?P<userid>\d+)$', views.edituser, name='dashboard_edituser'),
url(r'^dashboard/user/saveuser/(?P<userid>\d+)$', views.saveuser, name='dashboard_saveuser'), 
url(r'^dashboard/user/logout$', views.logout, name='dashboard_logout')           
	]