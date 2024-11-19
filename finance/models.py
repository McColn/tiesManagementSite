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

class Assets(models.Model):
    title = models.CharField(max_length=1000)
    amount = models.IntegerField(null=True, blank=True) #no of asset
    unit_cost = models.FloatField()
    totalCost = models.FloatField(null=True, blank=True) 
    createdAt = models.DateTimeField(auto_now_add=True)
    processor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calculate the total cost based on unit_cost and amount
        self.totalCost = round(self.unit_cost * self.amount, 2) if self.unit_cost and self.amount else None
        super().save(*args, **kwargs)

