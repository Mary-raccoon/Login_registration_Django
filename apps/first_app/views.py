from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
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
    return redirect('/quotes')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
      for field, message in errors.iteritems():
        error(request, message, extra_tags=field)
        return redirect('/')
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    return redirect('/quotes')
    
def quotes(request):
    context = {
        'messages': Quote.objects.all(),
        'user': User.objects.get(id=request.session['id']),
        'quoted_by': Quote.objects.all(),
        'other_quotes': Quote.objects.all(),
        'action1': "Add to my List",
        'action2': "Remove from my List",
    }
    return render(request, 'first_app/quotes.html', context)

def create_process(request):
    # errors = Quote.objects.quote_validator(request.POST)
    # if len(errors):
    #   for field, message in errors.iteritems():
    #     error(request, message, extra_tags=field)
    #     return redirect('/quotes')

    this_user = User.objects.get(id=request.session['id'])
    this_quote = Quote.objects.create(message = request.POST['message'])
    this_user.quotes.add(this_quote)

    return redirect('/quotes')


def users(request, id):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'messages': Quote.objects.all(),
    }
    
    return render(request, "first_app/users.html", context)

def favorite_quote(request,id):
    context = {
        'messages': Quote.objects.all(),
        'user': User.objects.get(id=request.session['id']),
    }
    this_user = User.objects.get(id=id)
    this_message = Quote.objects.get(id = id)
    this_user.messages.add(this_message)
    
    return redirect('/quotes')

def remove_quote(request, id):
    context = {
        'messages': Quote.objects.all(),
        'user': User.objects.get(id=request.session['id'])
    }
    this_user = User.objects.get(id=request.session['id'])
    this_quote = Quote.objects.get(id = id)
    this_user.quotes.remove(this_quote)

    return redirect('/quotes')

def logout(request):
    return redirect('/')

def home(request):
    return redirect('/quotes')