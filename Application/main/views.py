from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from main.forms import RegisterForm, LoginForm, UploadProfileImageForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from main.models import Patient, Address, Doctor
from datetime import date
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage

def index(request):
    template = loader.get_template('main/index.html')
    form = RegisterForm()
    context = {
        'registerForm' : form,
    }
    return render(request, 'index.html', context)

def app_login(request):
    if not request.user.is_authenticated():
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect("/dashboard")
        return render(request, 'login.html', {'loginForm' : form})
    else:
        return HttpResponseRedirect("/dashboard")



def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(request.POST.get("email"), request.POST.get("email"), request.POST.get("password"))
        address = Address.create_address(request.POST)
        parameters = request.POST
        dob = date(int(request.POST.get("date_year")),int(request.POST.get("date_month")),int(request.POST.get("date_day")))

        if(request.POST.get("type") == '2'):
            doctor = Doctor.object.get(request.POST.get("doctor"))
            patient = Patient.createPatient(parameters.get("firstName"),parameters.get("lastName"),parameters.get("contact"),dob,address,user)
            patient.save()
        else:
            doctor = Doctor.createDoctor(parameters.get("firstName"),parameters.get("lastName"),parameters.get("contact"),dob,address,user)
            doctor.save()

        user = authenticate(username=request.POST.get("email"), password=request.POST.get("password"))
        if user:
            login(request, user)
            user.first_name = request.POST.get("firstName")
            user.last_name = request.POST.get("lastName")
            user.save()
            return HttpResponseRedirect("/dashboard")

    return render(request, 'register.html', {'registerForm' : form})



def app_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def profile(request):
    return render(request,'dashboard/user.html')

def uploadProfileImage(request):
    if request.method == "POST" :
        form = UploadProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/profile')
        return HttpResponse("OK")
    return HttpResponseRedirect(settings.STATIC_ROOT)

def handle_uploaded_file(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    url = fs.url(filename)
    profileImagePath = os.path.join(settings.STATIC_ROOT, 'media/profiles/users/' + user.username)
    with open(profileImagePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
