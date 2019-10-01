from django.urls import path , re_path 
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.my_view, name='index'),
    path('upload', views.upload_file, name='upload'),
    re_path(r'^login/$',views.my_view,name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^passchng/$', views.PasswordChangeView.as_view(), name='changepass'),
    path('signup', views.sign_up, name='signup'),
    path('train_dt/<int:choice>/', views.train_data, name='run'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('result', views.index, name='result'),
]