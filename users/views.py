from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.add_message(request, constants.ERROR, "Passwords do not match")
            return redirect('/users/signup/')
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, "Password must be at least 6 characters")
            return redirect('/users/signup/')
        
        users = User.objects.filter(username=username)
        if users.exists():
            messagesessages.add_message(request, constants.ERROR, "Username already exists")
            return redirect('/users/signup/')
        
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/users/login/')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/mentorship')
        
        messages.add_message(request, constants.ERROR, "Invalid username or password")
        return redirect('login')