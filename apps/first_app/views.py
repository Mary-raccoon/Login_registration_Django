
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
from django.contrib.messages import error


def index(request):
  return render(request, "first_app/index.html")

def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
      for field, message in errors.iteritems():
        error(request, message, extra_tags=field)
        return redirect('/')
    password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = password_hash,
    )
    user = User.objects.last()
    request.session['id'] = user.id
    return redirect('/welcome')

def welcome(request):
    print "successful login"
    return render(request, 'first_app/welcome.html', {"user" : User.objects.get(id = request.session['id'])})

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
      for field, message in errors.iteritems():
        error(request, message, extra_tags=field)
        return redirect('/')
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    return redirect('/welcome')
    
