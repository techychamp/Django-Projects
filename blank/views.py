from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm , signup , signin
from django.http import HttpResponseRedirect
from .filehandler import handle_uploaded_file
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm ,PasswordResetForm
from django.contrib.auth.views import PasswordChangeView , PasswordResetView ,PasswordResetConfirmView,PasswordChangeDoneView,PasswordResetDoneView,PasswordResetCompleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
import glob
from .dtrees import classifier
files=[(i,v.rsplit("\\")[1]) for i,v in enumerate(glob.glob("blank/static/tmp/*"))]
def index(request):
    template=loader.get_template("blank/index.html")
    return HttpResponse(template.render(request))
def my_view(request):
    if(request.user.is_authenticated):
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
            return HttpResponseRedirect('login')
    else:
        form = signup()
    return render(request, 'blank/auth.html', {'form': form})

def logout_view(request):
    validated=login_verify(request)
    if(validated!=1):
        return validated
    logout(request)
    return my_view(request)
def upload_file(request):
    validated=login_verify(request)
    if(validated!=1):
        return validated
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            global files
            handle_uploaded_file(request.FILES['file'])
            files=[(i,v.rsplit("\\")[1]) for i,v in enumerate(glob.glob("blank/static/tmp/*"))]
            return render(request, 'blank/upload.html', {'form': form,"files":files})
    else:
        form = UploadFileForm()
    return render(request, 'blank/upload.html', {'form': form,"files":files})
def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.POST)
            return HttpResponse("password changed")
    else:
        template=loader.get_template("blank/forget_pass.html")
        form = PasswordChangeForm(request.user)
    return HttpResponse(template.render({"form":form}))


def train_data(request,choice):
    validated=login_verify(request)
    if(validated!=1):
        return validated
    else:
        classifier(files[choice][1])
        template=loader.get_template("blank/card.html")
        txt=open("blank/static/output/result.txt","r")
        text=txt.readlines()
        txt.close()
        del txt
        return HttpResponse(template.render({"file":files[choice][1],"text":text}))
def login_verify(request):
    if(request.user.is_authenticated):
        return 1
    else:
        return my_view(request)
