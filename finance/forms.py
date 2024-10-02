from django import forms
from finance.models import *
from django.db.models import Sum

class ExpensesCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpensesCategory
        fields = [
                  'title','description'
                ]

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = [
                  'title','description',
                  'amount'
                ]
        
class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = [
                  'name','type','number',
                  'logo'
                ]