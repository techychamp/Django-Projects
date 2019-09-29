from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm , signup , signin ,PasswordChangeForm
from django.http import HttpResponseRedirect
from .filehandler import handle_uploaded_file
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
import glob

def index(request):
    template=loader.get_template("blank/index.html")
    return HttpResponse(template.render(request))
def my_view(request):
    validated=login_verify(request)
    if(validated==1):
        return HttpResponseRedirect('/blank/upload')
    if request.method == 'POST':
        form = signin(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/blank/upload')
    else:
        form = signin()
    return render(request, 'blank/auth.html', {'form': form})
def sign_up(request):
    if request.method == 'POST':
        form = signup(request.POST)
        if form.is_valid() and request.POST['password']==request.POST['cnf_password']:
            user = User.objects.create_user(request.POST['username'], request.POST['mail'], request.POST['password'])
            user.save()
            return HttpResponseRedirect('blank/login')
    else:
        form = signup()
    return render(request, 'blank/auth.html', {'form': form})

def logout_view(request):
    validated=login_verify(request)
    if(validated!=1):
        return validated
    logout(request)
    return HttpResponse("logged out")
def upload_file(request):
    validated=login_verify(request)
    if(validated!=1):
        return validated
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'blank/result.html', {'result': "success"})
    else:
        form = UploadFileForm()
    return render(request, 'blank/upload.html', {'form': form,"files":[i.rsplit("\\")[1] for i in glob.glob("blank/static/tmp/*")]})
def frget_pswd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)#, data=request.POST
        if form.is_valid():
            update_session_auth_hash(request, request.user)
            return render(request, 'blank/result.html', {'result': "mail sent to your email"})
    else:
        form = PasswordChangeForm()
    return render(request, 'blank/result.html', {'result': form})

def login_verify(request):
    if(request.user.is_authenticated):
        return 1
    else:
        return HttpResponseRedirect('login')
