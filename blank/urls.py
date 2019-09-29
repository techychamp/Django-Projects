from django.urls import path , re_path

from . import views

urlpatterns = [
    path('', views.my_view, name='index'),
    path('upload', views.upload_file, name='upload'),
    re_path(r'^login/$',views.my_view,name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^forget/$', views.frget_pswd, name='forget'),
    path('signup', views.sign_up, name='signup'),
    path('train_dt', views.sign_up, name='signup'),
    path('result', views.index, name='result'),
]