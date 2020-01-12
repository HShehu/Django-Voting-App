from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from VotingUsers.admin import UserCreationForm, LoginForm
# Create your views here.


def registration_view(request):
    context = {}
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            student_number = form.cleaned_data.get('student_number')
            full_name = form.cleaned_data.get('full_name')
            login_code = form.cleaned_data.get('login_code')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(student_number=student_number,
                                   full_name=full_name, login_code=login_code, password=raw_password)
            login(request, account)
            return redirect('VotingApp:home')
        else:
            context['registration_form'] = form
    else:  # GET Request
        form = UserCreationForm()
        context['registration_form'] = form
    return render(request, 'VotingUsers/register.html', context)


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,'You Have Logged Out')
    return redirect('VotingApp:home')

def login_view(request):
    context = {}

    user= request.user
    if user.is_authenticated:
        messages.add_message(request, messages.SUCCESS, 'You Have Logged In')
        return redirect('VotingApp:home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
          student_number=request.POST['student_number']
          password=request.POST['password'] 
          user = authenticate(student_number=student_number,password=password)

          if user:
              login(request, user)
              messages.add_message(
                  request, messages.SUCCESS, 'You Have Logged In')
              return redirect('VotingApp:home')

    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request,'VotingUsers/login.html',context)
