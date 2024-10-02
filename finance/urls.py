
from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('base2/', views.base2, name='base2'),
    path('overview/', views.overview, name='overview'),
    path('income/', views.income, name='income'),
    path('expenses/', views.expenses, name='expenses'),
    path('expensesDetails/<int:id>/', views.expensesDetails, name='expensesDetails'),
    path('balance/', views.balance, name='balance'),
    path('transactions/', views.transactions, name='transactions'),
    path('expensesCategoryAdd/', views.expensesCategoryAdd, name='expensesCategoryAdd'),
    path('bankCardAdd/', views.bankCardAdd, name='bankCardAdd'),
    path('expensesAdd/<int:project_id>/', views.expensesAdd, name='expensesAdd'),
    path('analytics/', views.analytics, name='analytics'),
    path('incomeStatement/', views.incomeStatement, name='incomeStatement'),
]