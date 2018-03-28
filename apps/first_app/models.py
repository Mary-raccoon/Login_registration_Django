from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be longer than 2 characters"
        elif not 'first_name' in errors and not re.match(NAME_REGEX, postData['first_name']):
            errors['first_name'] = "First name must only contain letters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be longer than 2 characters"
        elif not 'last_name' in errors and not re.match(NAME_REGEX, postData['last_name']):
            errors['last_name'] = "Last name must only contain letters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords do not match"
        if not 'email' in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        else:
            if len(self.filter(email = postData['email'])) > 1:
                errors['email'] = 'Email address is already in use'
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Not a valid email"
        if len(User.objects.filter(email=postData['email'])) == 0:
            errors['email1'] = "Email does not exist. Register first!"
        if len(User.objects.filter(email=postData['email'])) == 1:
            password_hash = User.objects.get(email=postData['email']).password
            if bcrypt.checkpw(postData['password'].encode(), password_hash.encode()) == False:  
                errors['password'] = "Incorrect password. Try again!"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
   
    def __repr__(self): # retrieves all records in the Blog table
        return "user_object: {} {} {} {}".format(self.first_name, self.last_name, self.email, self.password)

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        # if len(postData['quoted_by']) < 3:
        #     errors['quoted_by'] = "Your Name should be longer than 3 characters"
        if len(postData['message']) < 10:
            errors['message'] = "Message should be longer than 10 characters"
        return errors
        
class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    users = models.ManyToManyField(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

    def __repr__(self): 
        return "Quote_object: {} {} {}".format(self.message, self.quoted_by,self.users )
