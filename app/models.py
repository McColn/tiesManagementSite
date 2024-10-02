from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Create your models here.
class CustomUser(AbstractUser):
    #basic info
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True,blank=True, default="null")
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    
    #personal info
    nextKinName = models.CharField(max_length=100, null=True, blank=True)
    nextKinRelation = models.CharField(max_length=100, null=True, blank=True)
    nextKinAddress = models.CharField(max_length=100, null=True, blank=True)
    nextKinPhone = models.CharField(max_length=100, null=True, blank=True)
    nida = models.CharField(max_length=100, null=True, blank=True)
    homeAdress = models.CharField(max_length=100, null=True, blank=True)
    #education
    uniName = models.CharField(max_length=100, null=True, blank=True)
    uniLevel = models.CharField(max_length=100, null=True, blank=True)
    uniCourse = models.CharField(max_length=100, null=True, blank=True)
    startYear = models.CharField(max_length=100, null=True, blank=True)
    endYear = models.CharField(max_length=100, null=True, blank=True)
    #contract
    role = models.CharField(max_length=50, null=True,blank=True, default="user")
    signedDate = models.DateField(null=True, blank=True)
    expireDate = models.DateField(null=True, blank=True)
    contractDuration = models.CharField(max_length=100, null=True, blank=True)
    remainDuration = models.CharField(max_length=100, null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate contract duration
        if self.signedDate and self.expireDate:
            delta = relativedelta(self.expireDate, self.signedDate)
            self.contractDuration = f'{delta.years * 12 + delta.months} months'

        # Calculate remain duration
        if self.expireDate:
            today = timezone.now().date()
            delta = relativedelta(self.expireDate, today)
            self.remainDuration = f'{delta.years * 12 + delta.months}'

        super().save(*args, **kwargs)
    


class Clients(models.Model):
    clientName = models.CharField(max_length=200)
    address = models.CharField(max_length=1000, null=True, blank=True)
    representativeName = models.CharField(max_length=100, null=True, blank=True)
    representativeTitle = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

# project
class Project(models.Model):
    title = models.CharField(max_length=200)
    client = models.ForeignKey(Clients,on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    performance = models.CharField(max_length=100, null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)
    person_in_charge = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

# project budget 
class ProjectBudget(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    desription = models.CharField(max_length=10000, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)

# Project cost daily payment
class ProjectExpense(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    desription = models.CharField(max_length=10000, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)

# project invoice or general project requirement cost which reflect the profit
class ProjectInvoice(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    desription = models.CharField(max_length=10000, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)

# project day to day revenue, amount company receive per each project
class ProjectPayment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    desription = models.CharField(max_length=10000, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)
    processor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

# project progress
class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    desription = models.CharField(max_length=10000, null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)

# Assignment task to an employees
class Assignment(models.Model):
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignments_received')  
    description = models.CharField(max_length=10000, null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateField()
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignments_given')
    status = models.CharField(max_length=100, default="on_progress", null=True, blank=True)

class AssignmentUpdates(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  
    description = models.CharField(max_length=10000, null=True, blank=True)
    issuedDate = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Leaves(models.Model): 
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leaveType = models.CharField(max_length=10000, null=True, blank=True)
    leave_reason = models.CharField(max_length=10000, null=True, blank=True)
    action = models.CharField(max_length=10000, default='pending')
    action_reason = models.CharField(max_length=10000, null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)



class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name