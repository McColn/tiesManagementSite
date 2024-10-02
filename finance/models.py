from django.db import models
from app.models import *

# Create your models here.
class ExpensesCategory(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

class Expenses(models.Model):
    category = models.ForeignKey(ExpensesCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True,blank=True)
    amount = models.FloatField()
    processor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    expenseDate = models.DateTimeField(auto_now_add=True)

class BankCard(models.Model):
    name = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000, null=True,blank=True)
    number = models.CharField(max_length=1000, null=True,blank=True)
    amount = models.FloatField(default= 0)
    logo = models.ImageField(upload_to='media/', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)