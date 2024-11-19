from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Expenses)
admin.site.register(ExpensesCategory)
admin.site.register(BankCard)
admin.site.register(Assets)