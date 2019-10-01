from django.urls import path , re_path

from . import views

urlpatterns = [
    path('', views.my_view, name='index'),
    path('upload', views.upload_file, name='upload'),
    re_path(r'^login/$',views.my_view,name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^passchng/$', views.PasswordChangeView.as_view(), name='changepass'),
    path('forget/', views.PasswordResetView.as_view(), name='forget'),
    path('signup', views.sign_up, name='signup'),
    path('train_dt/<int:choice>/', views.train_data, name='run'),
    #path('result', views.index, name='result'),
]