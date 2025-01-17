from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
  if request.user.is_authenticated:
    return redirect('home')
    
  if request.method == 'POST':
    if request.POST['username'] and request.POST['email'] and request.POST['password'] and request.POST['confirmpassword']:
      if request.POST['password'] == request.POST['confirmpassword']:
        try:
          user = User.objects.get(username = request.POST['username'])
          return render(request, 'accounts/signup.html', {'error' : 'Username has been already taken'})
        except User.DoesNotExist:
          user = User.objects.create_user(username =request.POST['username'], password=request.POST['password'], email=request.POST['email'])
          auth.login(request, user)
          return redirect('home')
      else:
        return render(request, 'accounts/signup.html', {'error' : 'Passwords are not correct'})

    else:
      return render(request, 'accounts/signup.html', {'error' : 'Please fill all fields'})

  else:
    return render (request, 'accounts/signup.html')

def login(request):
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
    if user is not None:
      auth.login(request, user)
      return redirect('home')
    else:
      return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
  
  else:
    return render (request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST' and request.user.is_authenticated:
    auth.logout(request)
  return redirect('home')
  