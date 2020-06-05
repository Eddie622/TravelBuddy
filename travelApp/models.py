from django.db import models
from datetime import date
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "username should be at least 3 characters"
        if len(postData['pwd']) < 8:
            errors["pwd"] = "Password should be at least 8 characters"
        if postData['pwd'] != postData['confirm_pwd']:
            errors['confrim_pwd'] = "Passwords do not match"
        
        users = User.objects.all()
        for user in users:
            if postData['username'] == user.username:
                errors['username'] = "username is taken"

        return errors

class PlanManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        DATE_REGEX = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')
        if not DATE_REGEX.match(postData['date_from']):            
            errors['date_from'] = "From Date must be formatted YYYY-MM-DD"
        if not DATE_REGEX.match(postData['date_to']):            
            errors['date_to'] = "To Date must be formatted YYYY-MM-DD"
        
        from_date_values = postData['date_from'].split("-")
        to_date_values = postData['date_to'].split("-")

        if len(from_date_values) == 3:
            if from_date_values[1] > '21' or from_date_values[2] > '31':
                errors['range'] = "Date out of range"
        if len(to_date_values) == 3:
            if to_date_values[1] > '21' or to_date_values[2] > '31':
                errors['range'] = "Date out of range"

        if len(postData['destination']) < 1:
            errors["destination"] = "Destination field cannot be empty"
        if len(postData['description']) < 1:
            errors["description"] = "Description cannot be empty"
        if postData['date_from'] < str(date.today()):
            errors['date_from_past'] = "Travel Cannot be set in the past"
        if postData['date_from'] > postData['date_to']:
            errors['dates'] = "Date To cannot be before Date From"

        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TravelPlan(models.Model):
    destination = models.CharField(max_length=45)
    description = models.TextField()
    dateFrom = models.DateField()
    dateTo = models.DateField()
    creator = models.ForeignKey(User, related_name="plans", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlanManager()

class Trip(models.Model):
    plan = models.ForeignKey(TravelPlan, related_name="trips", on_delete = models.CASCADE)
    users = models.ManyToManyField(User, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)