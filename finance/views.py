from django.shortcuts import render, redirect
from finance.forms import *
from app.models import ProjectPayment
from django.db.models import Sum
from django.utils import timezone
import calendar
from datetime import datetime, timedelta


# Create your views here.
def base(request):
    return render(request, 'finance/base.html')

def base2(request):
    return render(request, 'finance/base2.html')

def overview(request):
    return render(request, 'finance/overview.html')

def income(request):
    # Get the current date and time
    now = timezone.now()

    # Calculate date range for the current month
    start_of_current_month = datetime(now.year, now.month, 1)
    start_of_next_month = start_of_current_month + timedelta(days=32)
    start_of_next_month = datetime(start_of_next_month.year, start_of_next_month.month, 1)

    # Calculate date range for the last month
    start_of_last_month = start_of_current_month - timedelta(days=1)
    start_of_last_month = datetime(start_of_last_month.year, start_of_last_month.month, 1)
    end_of_last_month = start_of_current_month - timedelta(seconds=1)

    # Calculate date range for the current year
    start_of_current_year = datetime(now.year, 1, 1)

    # Calculate date range for the last year
    start_of_last_year = datetime(now.year - 1, 1, 1)
    end_of_last_year = datetime(now.year - 1, 12, 31, 23, 59, 59)

    # Query for the total payment amounts
    total_income = ProjectPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income_this_month = ProjectPayment.objects.filter(issuedDate__gte=start_of_current_month, issuedDate__lt=start_of_next_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_income_last_month = ProjectPayment.objects.filter(issuedDate__gte=start_of_last_month, issuedDate__lt=start_of_current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_income_this_year = ProjectPayment.objects.filter(issuedDate__gte=start_of_current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_income_last_year = ProjectPayment.objects.filter(issuedDate__gte=start_of_last_year, issuedDate__lte=end_of_last_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate monthly payments for the current and last years
    monthly_payments_this_year = []
    monthly_payments_last_year = []

    for month in range(1, 13):
        start_of_month = datetime(now.year, month, 1)
        if month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(now.year, month + 1, 1)
        total_for_month = ProjectPayment.objects.filter(issuedDate__gte=start_of_month, issuedDate__lt=start_of_next_month).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_payments_this_year.append((month, total_for_month))

        start_of_last_year_month = datetime(now.year - 1, month, 1)
        if month == 12:
            start_of_next_last_year_month = datetime(now.year, 1, 1)
        else:
            start_of_next_last_year_month = datetime(now.year - 1, month + 1, 1)
        total_for_last_year_month = ProjectPayment.objects.filter(issuedDate__gte=start_of_last_year_month, issuedDate__lt=start_of_next_last_year_month).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_payments_last_year.append((month, total_for_last_year_month))

    context = {
        'all_incomes': ProjectPayment.objects.all(),
        'total_income': total_income,
        'total_income_this_month': total_income_this_month,
        'total_income_last_month': total_income_last_month,
        'total_income_this_year': total_income_this_year,
        'total_income_last_year': total_income_last_year,
        'monthly_payments_this_year': monthly_payments_this_year,
        'monthly_payments_last_year': monthly_payments_last_year,
    }

    return render(request, 'finance/income.html', context)

def expenses(request):
    today = timezone.now()
    current_year = today.year
    current_month = today.month

    # Calculate start and end dates for this month
    start_of_current_month = timezone.make_aware(timezone.datetime(current_year, current_month, 1))
    if current_month == 12:
        start_of_next_month = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1))
    else:
        start_of_next_month = timezone.make_aware(timezone.datetime(current_year, current_month + 1, 1))
    end_of_current_month = start_of_next_month - timezone.timedelta(days=1)

    # Calculate start and end dates for the previous month
    if current_month == 1:
        start_of_last_month = timezone.make_aware(timezone.datetime(current_year - 1, 12, 1))
        end_of_last_month = timezone.make_aware(timezone.datetime(current_year, 1, 1)) - timezone.timedelta(days=1)
    else:
        start_of_last_month = timezone.make_aware(timezone.datetime(current_year, current_month - 1, 1))
        end_of_last_month = start_of_current_month - timezone.timedelta(days=1)

    # Calculate start and end dates for this year
    start_of_this_year = timezone.make_aware(timezone.datetime(current_year, 1, 1))
    end_of_this_year = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1)) - timezone.timedelta(days=1)

    # Calculate start and end dates for last year
    start_of_last_year = timezone.make_aware(timezone.datetime(current_year - 1, 1, 1))
    end_of_last_year = timezone.make_aware(timezone.datetime(current_year, 1, 1)) - timezone.timedelta(days=1)

    expenses_category = ExpensesCategory.objects.all()
    categories_with_expenses = []

    # Initialize totals for months
    monthly_expenses_current_year = {month: 0 for month in range(1, 13)}
    monthly_expenses_last_year = {month: 0 for month in range(1, 13)}

    # Overall totals
    total_expenses_current_month = 0
    total_expenses_last_month = 0
    total_expenses_this_year = 0
    total_expenses_last_year = 0
    total_expenses_overall = 0

    for category in expenses_category:
        # Get the first two expenses
        first_two_expenses = Expenses.objects.filter(category=category).order_by('-id')[:2]

        # Calculate expenses for this month
        expenses_current_month = Expenses.objects.filter(
            category=category,
            expenseDate__range=[start_of_current_month, end_of_current_month]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate expenses for last month
        expenses_last_month = Expenses.objects.filter(
            category=category,
            expenseDate__range=[start_of_last_month, end_of_last_month]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate expenses for this year
        expenses_this_year = Expenses.objects.filter(
            category=category,
            expenseDate__range=[start_of_this_year, end_of_this_year]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate expenses for last year
        expenses_last_year = Expenses.objects.filter(
            category=category,
            expenseDate__range=[start_of_last_year, end_of_last_year]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate monthly expenses for this year and last year
        for month in range(1, 13):
            start_of_month = timezone.make_aware(timezone.datetime(current_year, month, 1))
            if month == 12:
                start_of_next_month = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1))
            else:
                start_of_next_month = timezone.make_aware(timezone.datetime(current_year, month + 1, 1))
            end_of_month = start_of_next_month - timezone.timedelta(days=1)

            monthly_expenses_current_year[month] += Expenses.objects.filter(
                category=category,
                expenseDate__range=[start_of_month, end_of_month]
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            start_of_last_year_month = timezone.make_aware(timezone.datetime(current_year - 1, month, 1))
            if month == 12:
                start_of_next_month_last_year = timezone.make_aware(timezone.datetime(current_year, 1, 1))
            else:
                start_of_next_month_last_year = timezone.make_aware(timezone.datetime(current_year - 1, month + 1, 1))
            end_of_last_year_month = start_of_next_month_last_year - timezone.timedelta(days=1)

            monthly_expenses_last_year[month] += Expenses.objects.filter(
                category=category,
                expenseDate__range=[start_of_last_year_month, end_of_last_year_month]
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate overall total
        category_total = Expenses.objects.filter(category=category).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        total_expenses_current_month += expenses_current_month
        total_expenses_last_month += expenses_last_month
        total_expenses_this_year += expenses_this_year
        total_expenses_last_year += expenses_last_year
        total_expenses_overall += category_total

        categories_with_expenses.append({
            'category': category,
            'expenses': first_two_expenses,
            'expenses_current_month': expenses_current_month,
            'expenses_last_month': expenses_last_month,
            'expenses_this_year': expenses_this_year,
            'expenses_last_year': expenses_last_year,
            'total_amount': category_total,
        })

    context = {
        'categories_with_expenses': categories_with_expenses,
        'total_expenses_current_month': total_expenses_current_month,
        'total_expenses_last_month': total_expenses_last_month,
        'total_expenses_this_year': total_expenses_this_year,
        'total_expenses_last_year': total_expenses_last_year,
        'total_expenses_overall': total_expenses_overall,
        'monthly_expenses_current_year': monthly_expenses_current_year,
        'monthly_expenses_last_year': monthly_expenses_last_year,
    }

    return render(request, 'finance/expenses.html', context)

def expensesAdd(request, project_id):
    expenses_list = Expenses.objects.all()
    category = ExpensesCategory.objects.get(id=project_id)
    form = ExpensesForm()
    
    if request.method == 'POST':
        form = ExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.category = category
                expense.processor = request.user
                expense.save()
                return redirect('expensesDetails', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'category': category,
        'expenses_list': expenses_list,
        'project_id': project_id
    }
    return render(request, "finance/expensesDetails.html", context)

def expensesDetails(request, id):
    today = timezone.now()
    current_year = today.year
    current_month = today.month

    # Calculate start and end dates for this month
    start_of_current_month = timezone.make_aware(timezone.datetime(current_year, current_month, 1))
    if current_month == 12:
        start_of_next_month = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1))
    else:
        start_of_next_month = timezone.make_aware(timezone.datetime(current_year, current_month + 1, 1))
    end_of_current_month = start_of_next_month - timezone.timedelta(days=1)

    # Calculate start and end dates for the previous month
    if current_month == 1:
        start_of_last_month = timezone.make_aware(timezone.datetime(current_year - 1, 12, 1))
        end_of_last_month = timezone.make_aware(timezone.datetime(current_year, 1, 1)) - timezone.timedelta(days=1)
    else:
        start_of_last_month = timezone.make_aware(timezone.datetime(current_year, current_month - 1, 1))
        end_of_last_month = start_of_current_month - timezone.timedelta(days=1)

    # Calculate start and end dates for this year
    start_of_this_year = timezone.make_aware(timezone.datetime(current_year, 1, 1))
    end_of_this_year = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1)) - timezone.timedelta(days=1)

    # Calculate start and end dates for last year
    start_of_last_year = timezone.make_aware(timezone.datetime(current_year - 1, 1, 1))
    end_of_last_year = timezone.make_aware(timezone.datetime(current_year, 1, 1)) - timezone.timedelta(days=1)

    # Get the category and its expenses
    category = ExpensesCategory.objects.get(id=id)
    expenses_list = Expenses.objects.filter(category_id=id).order_by('-id')

    # Calculate total expenses
    total_expenses_current_month = Expenses.objects.filter(
        category_id=id,
        expenseDate__range=[start_of_current_month, end_of_current_month]
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    total_expenses_last_month = Expenses.objects.filter(
        category_id=id,
        expenseDate__range=[start_of_last_month, end_of_last_month]
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    total_expenses_this_year = Expenses.objects.filter(
        category_id=id,
        expenseDate__range=[start_of_this_year, end_of_this_year]
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    total_expenses_last_year = Expenses.objects.filter(
        category_id=id,
        expenseDate__range=[start_of_last_year, end_of_last_year]
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Calculate monthly expenses for this year and last year
    monthly_expenses_current_year = {month: 0 for month in range(1, 13)}
    monthly_expenses_last_year = {month: 0 for month in range(1, 13)}

    for month in range(1, 13):
        start_of_month = timezone.make_aware(timezone.datetime(current_year, month, 1))
        if month == 12:
            start_of_next_month = timezone.make_aware(timezone.datetime(current_year + 1, 1, 1))
        else:
            start_of_next_month = timezone.make_aware(timezone.datetime(current_year, month + 1, 1))
        end_of_month = start_of_next_month - timezone.timedelta(days=1)

        monthly_expenses_current_year[month] = Expenses.objects.filter(
            category_id=id,
            expenseDate__range=[start_of_month, end_of_month]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        start_of_last_year_month = timezone.make_aware(timezone.datetime(current_year - 1, month, 1))
        if month == 12:
            start_of_next_month_last_year = timezone.make_aware(timezone.datetime(current_year, 1, 1))
        else:
            start_of_next_month_last_year = timezone.make_aware(timezone.datetime(current_year - 1, month + 1, 1))
        end_of_last_year_month = start_of_next_month_last_year - timezone.timedelta(days=1)

        monthly_expenses_last_year[month] = Expenses.objects.filter(
            category_id=id,
            expenseDate__range=[start_of_last_year_month, end_of_last_year_month]
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Calculate overall total
    total_amount = Expenses.objects.filter(category_id=id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    context = {
        'category': category,
        'expenses_list': expenses_list,
        'total_expenses_current_month': total_expenses_current_month,
        'total_expenses_last_month': total_expenses_last_month,
        'total_expenses_this_year': total_expenses_this_year,
        'total_expenses_last_year': total_expenses_last_year,
        'monthly_expenses_current_year': monthly_expenses_current_year,
        'monthly_expenses_last_year': monthly_expenses_last_year,
        'total_amount': total_amount,
    }

    return render(request, 'finance/expensesDetails.html', context)

def expensesCategoryAdd(request):
    form = ExpensesCategoryForm()
    
    if request.method == 'POST':
        form = ExpensesCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('expenses')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form
    }
    return render(request, "finance/expenses.html", context)

def balance(request):
    card_list = BankCard.objects.all()
    project_payment = ProjectPayment.objects.all()
    total_income = project_payment.aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'card_list':card_list,
        'total_income':total_income,
    }
    return render(request, 'finance/balance.html',context)

def transactions(request):
    project_income = ProjectPayment.objects.all().order_by('-id')
    project_expenses = ProjectExpense.objects.all().order_by('-id')
    company_expenses = Expenses.objects.all().order_by('-id')

    context = {
        'project_income':project_income,
        'project_expenses':project_expenses,
        'company_expenses':company_expenses,
    }

    return render(request, 'finance/transactions.html',context)

def bankCardAdd(request):
    form = BankCardForm()
    
    if request.method == 'POST':
        form = BankCardForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('balance')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form
    }
    return render(request, "finance/balance.html", context)


def analytics(request):
    return render(request, 'finance/analytics.html')

def incomeStatement(request):
    # Calculate total cost of goods
    total_cost_goods = ProjectExpense.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    # Calculate total revenue
    total_revenue = ProjectPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    # You can calculate the profit (or loss) if needed
    total_profit = total_revenue - total_cost_goods

    context = {
        'total_cost_goods': total_cost_goods,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
    }

    return render(request, 'finance/incomeStatement.html', context)