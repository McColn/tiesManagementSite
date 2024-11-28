from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib import messages
from app.models import *
from app.forms import *
from datetime import date
from datetime import datetime
import requests
from django.db.models import Count
from django.db.models import Min

def home(request):
    # Get the minimum remainDuration for employee contract
    min_duration = CustomUser.objects.aggregate(Min('remainDuration'))['remainDuration__min']
    # Filter employees with that minimum remainDuration
    employees = CustomUser.objects.filter(remainDuration=min_duration)

    # Get the two projects that are upcoming to end, comparing by endDate
    upcoming_projects = Project.objects.filter(endDate__gte=date.today()).order_by('endDate')[:2]


    project = Project.objects.all()
    # projects
    total_projects = project.count()
    completed_project = Project.objects.filter(status="complete").count()
    uncompleted_project = Project.objects.exclude(status="complete").count()
    overdue_projects = Project.objects.filter(endDate__lt=datetime.today()).exclude(status="complete").count()
    # leaves
    total_leaves = Leaves.objects.all().count()
    approved_leaves = Leaves.objects.exclude(action="pending").count()
    pending_leaves = Leaves.objects.filter(action="pending").count()
    # employee
    total_employee = CustomUser.objects.all().count()
    # clients
    total_clients = Clients.objects.all().count()
    current_year = datetime.now().year
    clients_this_year = Clients.objects.filter(created_date__year=current_year).count()
    # Rank top 2 clients by total income from projects
    # Rank top 2 clients by the number of projects
    top_clients = (
        Clients.objects.annotate(project_count=Count('project'))
        .order_by('-project_count')[:2]
    )
    # tasks
    total_task = Assignment.objects.all().count()

    # Invoice calculations
    now = datetime.now()
    start_of_current_year = datetime(now.year, 1, 1)
    start_of_last_year = datetime(now.year - 1, 1, 1)
    start_of_next_year = datetime(now.year + 1, 1, 1)

    start_of_current_month = datetime(now.year, now.month, 1)
    start_of_last_month = start_of_current_month - timedelta(days=1)
    start_of_last_month = datetime(start_of_last_month.year, start_of_last_month.month, 1)

    total_invoice_this_year = ProjectInvoice.objects.filter(issuedDate__gte=start_of_current_year, issuedDate__lt=start_of_next_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_invoice_last_year = ProjectInvoice.objects.filter(issuedDate__gte=start_of_last_year, issuedDate__lt=start_of_current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_invoice_this_month = ProjectInvoice.objects.filter(issuedDate__gte=start_of_current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_invoice_last_month = ProjectInvoice.objects.filter(issuedDate__gte=start_of_last_month, issuedDate__lt=start_of_current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_invoice_overall = ProjectInvoice.objects.aggregate(Sum('amount'))['amount__sum'] or 0


    # tasks
    total_task = Assignment.objects.all().count()
    # Assignment calculations
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())  # Start of the current week (Monday)
    start_of_month = datetime(now.year, now.month, 1)  # Start of the current month
    start_of_year = datetime(now.year, 1, 1)  # Start of the current year
    # Assignments count for different periods
    assignments_this_week = Assignment.objects.filter(issuedDate__gte=start_of_week).count()
    assignments_this_month = Assignment.objects.filter(issuedDate__gte=start_of_month).count()
    assignments_this_year = Assignment.objects.filter(issuedDate__gte=start_of_year).count()
    # Assignments due today
    assignments_due_today = Assignment.objects.filter(dueDate=datetime.today())


    # Calculate monthly projects for the current and last years
    monthly_projects_this_year = []
    monthly_projects_last_year = []

    for month in range(1, 13):
        start_of_month = datetime(now.year, month, 1)
        start_of_next_month = datetime(now.year, month + 1, 1) if month < 12 else datetime(now.year + 1, 1, 1)
        
        total_for_month = Project.objects.filter(startDate__gte=start_of_month, startDate__lt=start_of_next_month).count()
        monthly_projects_this_year.append((month, total_for_month))

        start_of_last_year_month = datetime(now.year - 1, month, 1)
        start_of_next_last_year_month = datetime(now.year - 1, month + 1, 1) if month < 12 else datetime(now.year, 1, 1)
        
        total_for_last_year_month = Project.objects.filter(startDate__gte=start_of_last_year_month, startDate__lt=start_of_next_last_year_month).count()
        monthly_projects_last_year.append((month, total_for_last_year_month))

    context = {
        'project': project,
        'employees': employees,
        'upcoming_projects':upcoming_projects,
        'total_projects': total_projects,
        'completed_project': completed_project,
        'uncompleted_project': uncompleted_project,
        'overdue_projects': overdue_projects,
        'total_leaves': total_leaves,
        'approved_leaves': approved_leaves,
        'pending_leaves': pending_leaves,
        'total_employee': total_employee,
        'total_clients': total_clients,
        'clients_this_year': clients_this_year,
        'top_clients': top_clients,
        'total_task': total_task,
        'monthly_projects_this_year': monthly_projects_this_year,
        'monthly_projects_last_year': monthly_projects_last_year,
        'total_invoice_this_year': total_invoice_this_year,
        'total_invoice_last_year': total_invoice_last_year,
        'total_invoice_this_month': total_invoice_this_month,
        'total_invoice_last_month': total_invoice_last_month,
        'total_invoice_overall': total_invoice_overall,
        'assignments_this_week': assignments_this_week,
        'assignments_this_month': assignments_this_month,
        'assignments_this_year': assignments_this_year,
        'assignments_due_today': assignments_due_today,
    }
    return render(request, "app/home.html", context)

def base(request):
    return render(request,"app/base.html")

def dashboard(request):
    return render(request,"app/dashboard.html")

def employees(request):
    employee = CustomUser.objects.all()
    context = {
         'employee':employee
    }
    return render(request,"app/employees.html", context)

def employeesDetails(request,id):
    employee = CustomUser.objects.get(id=id)
    context = {
         'employee':employee
    }
    return render(request,"app/employeesDetails.html",context)

def project(request):
    projects = Project.objects.all()
    completed_project = Project.objects.filter(status="complete").count()
    uncompleted_project = Project.objects.exclude(status="complete").count()
    clients = Clients.objects.all()
    employee = CustomUser.objects.all()

    projects_with_performance = []

    for proj in projects:
        # Calculate total budget and total expense for each project
        total_budget = ProjectBudget.objects.filter(project=proj).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = ProjectExpense.objects.filter(project=proj).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate performance
        if total_budget == 0:
            performance = 0
        else:
            performance = (total_expense / total_budget) * 100
            performance = round(performance, 2)

        # Append project with calculated performance
        projects_with_performance.append({
            'project': proj,
            'performance': performance
        })

    context = {
        'projects_with_performance': projects_with_performance,
        'project_total': len(projects_with_performance),
        'clients': clients,
        'completed_project': completed_project,
        'uncompleted_project': uncompleted_project,
        'employee': employee,
    }
    
    return render(request, "app/project.html", context)

def projectAdd(request):
    clients = Clients.objects.all()
    employee = CustomUser.objects.all()
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('project')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
    context = {
         'form':form,
         'clients':clients,
         'employee':employee,
    }
    return render(request,"app/project.html",context)

def projectEdit(request,id):
    project = Project.objects.get(id=id)
    clients = Clients.objects.all()
    form = ProjectEditForm(instance=project)
    if request.method == 'POST':
        form = ProjectEditForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            try:
                form.save()
                return redirect('projectDetails', id=project.id)
            except Exception as e:
                print(f"Error updating item: {e}")
                # Optionally, add some error message to the context to show on the form
        else:
            print("Form is not valid")
    context = {
         'project':project,
         'form':form,
         'clients':clients
    }
    return render(request,"app/projectDetails.html",context)

def projectDetails(request, id):
    project_list = Project.objects.all()
    projectBudget = ProjectBudget.objects.filter(project_id=id).order_by('-id')
    projectExpense = ProjectExpense.objects.filter(project_id=id).order_by('-id')
    projectUpdate = ProjectUpdate.objects.filter(project_id=id).order_by('-id')
    projectInvoice = ProjectInvoice.objects.filter(project_id=id).order_by('-id')
    projectPayment = ProjectPayment.objects.filter(project_id=id).order_by('-id')
    project = Project.objects.get(id=id)
    clients = Clients.objects.all()
    
    # Calculate the total expense for the given project ID
    total_expense = projectExpense.aggregate(total=Sum('amount'))['total'] or 0
    total_budget = projectBudget.aggregate(total=Sum('amount'))['total'] or 0
    total_income = projectInvoice.aggregate(total=Sum('amount'))['total'] or 0
    total_payment = projectPayment.aggregate(total=Sum('amount'))['total'] or 0
    saved_amount = total_income - total_expense
    # performance = (total_expense / total_budget) * 100
    if total_budget == 0:
        print("Error: The total budget cannot be zero.")
        performance = 0
        percentage_payment_left = 0
    else:
        performance = (total_expense / total_budget) * 100
        performance = round(performance, 2)
        print(f"Performance: {performance:.2f}%")

        percentage_payment_left = (total_payment / total_income) * 100
        percentage_payment_left = round(percentage_payment_left, 2)
        print(f"percentage_payment_left: {percentage_payment_left:.2f}%")
    
    context = {
        'project': project,
        'project_list': project_list,
        'projectBudget': projectBudget,
        'projectExpense': projectExpense,
        'projectInvoice': projectInvoice,
        'projectUpdate': projectUpdate,
        'projectPayment': projectPayment,
        'project_id': id,
        'total_expense': total_expense,
        'total_budget': total_budget,
        'total_income': total_income,
        'saved_amount': saved_amount,
        'total_payment': total_payment,
        'clients': clients,
        'performance': performance,
        'percentage_payment_left': percentage_payment_left
    }
    return render(request, 'app/projectDetails.html', context)

def projectInvoiceAdd(request, project_id):
    project_list = Project.objects.all()
    project = Project.objects.get(id=project_id)
    form = ProjectInvoiceForm()
    
    if request.method == 'POST':
        form = ProjectInvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.save()
                return redirect('projectDetails', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(project)
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'project_list': project_list,
        'project_id': project_id
    }
    return render(request, "app/projectDetails.html", context)

def projectPaymentAdd(request, project_id):
    project_list = Project.objects.all()
    project = Project.objects.get(id=project_id)
    form = ProjectPaymentForm()
    
    if request.method == 'POST':
        form = ProjectPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.processor = request.user
                expense.save()
                return redirect('projectDetails', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(project)
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'project_list': project_list,
        'project_id': project_id
    }
    return render(request, "app/projectDetails.html", context)

def projectExpensesAdd(request, project_id):
    project_list = Project.objects.all()
    project = Project.objects.get(id=project_id)
    form = ProjectExpensesForm()
    
    if request.method == 'POST':
        form = ProjectExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.save()
                return redirect('projectDetails', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(project)
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'project_list': project_list,
        'project_id': project_id
    }
    return render(request, "app/projectDetails.html", context)

def projectBudgetAdd(request, project_id):
    project_list = Project.objects.all()
    project = Project.objects.get(id=project_id)
    form = ProjectBudgetForm()
    
    if request.method == 'POST':
        form = ProjectBudgetForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.save()
                return redirect('projectDetails', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(project)
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'project_list': project_list,
        'project_id': project_id
    }
    return render(request, "app/projectDetails.html", context)

def projectRemarkAdd(request, project_id):
    project_list = Project.objects.all()
    project = Project.objects.get(id=project_id)
    form = ProjectUpdateForm()
    
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.save()
                return redirect('projectProgress', id=project_id)
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(project)
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'project': project,
        'project_list': project_list,
        'project_id': project_id
    }
    return render(request, "app/projectDetails.html", context)

def clients(request):
    clients = Clients.objects.all()
    context = {
        'clients':clients
    }
    return render(request,"app/clients.html",context)

def clientDetails(request, id):
    # Fetch the client or return a 404 error if not found
    client = get_object_or_404(Clients, id=id)
    
    # Fetch projects associated with this client
    projects = Project.objects.filter(client=client)
    
    projects_with_performance = []
    
    for project in projects:
        # Calculate total budget and total expense for each project
        total_budget = ProjectBudget.objects.filter(project=project).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = ProjectExpense.objects.filter(project=project).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate performance
        if total_budget == 0:
            performance = 0
        else:
            performance = (total_expense / total_budget) * 100
            performance = round(performance, 2)

        # Append project with calculated performance
        projects_with_performance.append({
            'project': project,
            'performance': performance
        })
    
    context = {
        'client': client,
        'projects_with_performance': projects_with_performance
    }
    
    return render(request, "app/clientDetails.html", context)

def clientAdd(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('clients')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
    context = {
         'form':form
    }
    return render(request,"app/clients.html",context)

def basicInfo(request,id):
    employee = CustomUser.objects.get(id=id)
    form = BasicInfoForm(instance=employee)
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            try:
                form.save()
                return redirect('employeesDetails', id=employee.id)
            except Exception as e:
                print(f"Error updating item: {e}")
                # Optionally, add some error message to the context to show on the form
        else:
            print("Form is not valid")
    context = {
         'employee':employee,
         'form':form
    }
    return render(request,"app/employeesDetails.html",context)

def personalInfo(request,id):
    employee = CustomUser.objects.get(id=id)
    form = PersonalInfoForm(instance=employee)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            try:
                form.save()
                return redirect('employeesDetails', id=employee.id)
            except Exception as e:
                print(f"Error updating item: {e}")
                # Optionally, add some error message to the context to show on the form
        else:
            print("Form is not valid")
    context = {
         'employee':employee,
         'form':form
    }
    return render(request,"app/employeesDetails.html",context)

def educationInfo(request,id):
    employee = CustomUser.objects.get(id=id)
    form = EducationInfoForm(instance=employee)
    if request.method == 'POST':
        form = EducationInfoForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            try:
                form.save()
                return redirect('employeesDetails', id=employee.id)
            except Exception as e:
                print(f"Error updating item: {e}")
                # Optionally, add some error message to the context to show on the form
        else:
            print("Form is not valid")
    context = {
         'employee':employee,
         'form':form
    }
    return render(request,"app/employeesDetails.html",context)

def contractInfo(request,id):
    employee = CustomUser.objects.get(id=id)
    form = ContractInfoForm(instance=employee)
    if request.method == 'POST':
        form = ContractInfoForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            try:
                form.save()
                return redirect('employeesDetails', id=employee.id)
            except Exception as e:
                print(f"Error updating item: {e}")
                # Optionally, add some error message to the context to show on the form
        else:
            print("Form is not valid")
    context = {
         'employee':employee,
         'form':form
    }
    return render(request,"app/employeesDetails.html",context)

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate (username=username,password = password1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Bad Authenticate')
            return redirect('signin')
    return render(request, 'app/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('signin')
    return render(request, 'app/signout.html')

def signup(request):
	if request.method == 'POST':
		username=request.POST['username']
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		email=request.POST['username']
		password1=request.POST['password1']
		password2=request.POST['password2']

		myuser=CustomUser.objects.create_user(username,email,password1)
		myuser.first_name=firstname
		myuser.last_name=lastname
		myuser.save()
		messages.success(request,'You registered successfully')
		return redirect('signin')

	return render(request,'app/signup.html')

def assignment(request):
    all_assignment = Assignment.objects.all().order_by('-id')
    user_assignment = Assignment.objects.filter(assigned_to=request.user).order_by('-id')
    all_assignment_total = Assignment.objects.all().count()
    employee = CustomUser.objects.all()
    context = {
        'employee':employee,
        'all_assignment':all_assignment,
        'all_assignment_total':all_assignment_total,
        'user_assignment':user_assignment,
    }
    return render(request, 'app/assignment.html', context)

def assignmentAdd(request):
    form = AssignmentAddForm()
    employee = CustomUser.objects.all()
    if request.method == 'POST':
        form = AssignmentAddForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.assigned_by = request.user
                expense.save()
                return redirect('assignment')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, "app/assignment.html", context)

def assignmentDetails(request,id):
    assignment_details = Assignment.objects.get(id = id)
    assignmentsUpdatesList = AssignmentUpdates.objects.filter(assignment_id=id).order_by('-id')
    context = {
        'assignment_details':assignment_details,
        'assignmentsUpdatesList':assignmentsUpdatesList,
        'assignment_id':id,
    }
    return render(request, 'app/assignmentDetails.html',context)

def assignmentDetailsAdd(request, assignment_id):
    assignment_list = Assignment.objects.all()
    assignment = Assignment.objects.get(id=assignment_id)
    form = AssignmentUpdatesForm()

    if request.method == 'POST':
        form = AssignmentUpdatesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                update = form.save(commit=False)
                update.assignment = assignment
                update.assigned_by = request.user  # Set the logged-in user as the person assigning the update
                update.save()
                return redirect('assignmentDetails', id=assignment_id)
            except Exception as e:
                print(f"Error updating assignment: {e}")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging

    context = {
        'form': form,
        'assignment_list': assignment_list,
        'assignment_id': assignment_id
    }
    return render(request, "app/assignmentDetails.html", context)

def leaves(request):
    leaves_list = Leaves.objects.all().order_by('-id')
    # Filter leave requests by the logged-in user
    user_leaves = Leaves.objects.filter(employee=request.user).order_by('-id')
    context = {
        'leaves_list':leaves_list,
        'user_leaves':user_leaves,
    }
    return render(request,'app/leaves.html',context)

def leavesletter(request,id):
    leaves_details = Leaves.objects.get(id = id)
    context = {
        'leaves_details':leaves_details
    }
    return render(request, 'app/leavesletter.html',context)

def leavesDetails(request,id):
    leaves_details = Leaves.objects.get(id = id)
    # Get all other leaves for the same employee, excluding the clicked leave
    leaves_list = Leaves.objects.filter(employee=leaves_details.employee).exclude(id=id).order_by('-id')
    context = {
        'leaves_details':leaves_details,
        'leaves_list':leaves_list,
        'assignment_id':id,
    }
    return render(request, 'app/leavesDetails.html',context)

def leavesRequest(request):
    form = LeavesRequestForm()
    if request.method == 'POST':
        form = LeavesRequestForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                leave = form.save(commit=False)
                leave.employee = request.user
                leave.save()
                return redirect('leaves')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
    context = {
         'form':form
    }
    return render(request,'app/leavesRequest.html')

def leavesActions(request,id):
    s = Leaves.objects.get(id=id)
    leaves_details = Leaves.objects.get(id = id)
    form = LeavesActionForm(instance=s)
    if request.method == 'POST':
        form = LeavesActionForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('leavesDetails',id)
    context = {
        'form':form,
        'leaves_details':leaves_details,
        's':s,
    }
    return render(request, 'app/leavesDetails.html',context)

from django.contrib.auth.decorators import login_required
@login_required
def user_details(request):
    return render(request, 'app/user_details.html', {'user': request.user})

def calendar_view(request):
    events = Event.objects.all()


    current_year = date.today().year
    current_month = date.today().month

    return render(request, 'app/calendar.html', {
        'events': events,
        'current_year': current_year,
        'current_month': current_month,
    })

def salaryAdvance(request):
    # Get current date
    today = timezone.now()
    
    # Get the first and last day of the current month
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Filter records for this month
    this_month_records = SalaryAdvance.objects.filter(date_applied__gte=start_of_month, date_applied__lte=end_of_month).order_by('-id')
    
    # Filter records excluding those of this month (before start of the current month)
    past_records = SalaryAdvance.objects.filter(date_applied__lt=start_of_month).order_by('-id')
    
    context = {
        'this_month_records': this_month_records,
        'past_records': past_records,
    }
    
    return render(request, 'app/salaryAdvance.html', context)

def salaryAdvanceDetails(request, id):
    x = SalaryAdvance.objects.get(id = id)
    context = {
        'x':x
    }
    return render(request, 'app/salaryAdvanceDetails.html',context)

def salaryAdvanceActions(request,id):
    s = SalaryAdvance.objects.get(id=id)
    salary_adv = SalaryAdvance.objects.get(id=id)
    form = SalaryAdvanceActionForm(instance=s)
    if request.method == 'POST':
        form = SalaryAdvanceActionForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('salaryAdvanceDetails',id)
    context = {
        'form':form,
        'salary_adv':salary_adv,
        's':s,
    }
    return render(request, 'app/salaryAdvanceActions.html',context)

def advanceRequest(request):
    form = SalaryAdvanceForm()
    if request.method == 'POST':
        form = SalaryAdvanceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                leave = form.save(commit=False)
                leave.name = request.user
                leave.save()
                return redirect('salaryAdvance')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
    context = {
         'form':form
    }
    return render(request,'app/advanceRequest.html',context)

def company(request):
    employeeCode = Company.objects.filter(category='employeeCode')
    certificate = Company.objects.filter(category='certificate')
    secretarialReport = Company.objects.filter(category='secretarialReport')
    other = Company.objects.filter(category='other')
    context = {
        'employeeCode':employeeCode,
        'certificate':certificate,
        'secretarialReport':secretarialReport,
        'other':other,
    }

    return render(request,'app/company.html', context)

def companyPdfAdd(request):
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                leave = form.save(commit=False)
                leave.uploader = request.user
                leave.save()
                return redirect('company')
            except Exception as e:
                print(f"Error updating item: {e}")
        else:
            print("Form is not valid")
    context = {
         'form':form
    }
    return render(request,'app/advanceRequest.html',context)

def salarymccoln(mccoln):
    return render(mccoln, 'app/salarymccoln.html')

def projectProgress(request, id):
    # Retrieve the project using its ID
    project = get_object_or_404(Project, id=id)

    # Get all main tasks (ProjectUpdate) related to the project
    main_task = ProjectUpdate.objects.filter(project=project)

    # Get all subtasks (ProjectUpdateSubTask) related to the main tasks
    sub_task = ProjectUpdateSubTask.objects.filter(projectUpdate__in=main_task)

    context = {
        'project': project,
        'main_task': main_task,
        'sub_task': sub_task,
    }
    return render(request, 'app/projectProgress.html', context)

def projectProgressSubtask(request, project_update_id):
    # Get the ProjectUpdate object by its id
    project_update = get_object_or_404(ProjectUpdate, id=project_update_id)

    workers = CustomUser.objects.all()

    # Assuming `Project` is related to `ProjectUpdate` and has an id you want to redirect to
    project = project_update.project  # Assuming `ProjectUpdate` has a foreign key to `Project`

    if request.method == 'POST':
        form = ProjectUpdateSubTaskForm(request.POST)
        
        if form.is_valid():
            # Create a new subtask from the form data, but associate it with the current project update
            subtask = form.save(commit=False)
            subtask.projectUpdate = project_update  # Assign the entire ProjectUpdate object (not just the id)
            subtask.assigner = request.user  # Assign the current user as the assignee
            subtask.save()

            # Redirect to the project progress page associated with the parent project (using Project ID)
            
            return redirect('projectProgress', id=project.id)

    else:
        form = ProjectUpdateSubTaskForm()

    context = {
        'form': form, 
        'project_update': project_update,
        'workers': workers,
    }

    return render(request, 'app/projectProgressSubtask.html', context)

def projectProgressStatus(request):
    return render(request, 'app/projectProgressStatus.html')

def projectProgressStatus(request, subtask_id):
    # Fetch the subtask object using its ID
    subtask = get_object_or_404(ProjectUpdateSubTask, id=subtask_id)
    

    # If the request method is POST, we will handle the form submission
    if request.method == "POST":
        form = ProjectUpdateSubTaskStatusForm(request.POST, instance=subtask)  # Bind the form with the POST data

        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the updated status to the database
            # Redirect back to the project progress page
            return redirect('projectProgress', id=subtask.projectUpdate.project.id)

    else:
        # If the request is GET, create an empty form instance
        form = ProjectUpdateSubTaskStatusForm(instance=subtask)

    return render(request, 'app/projectProgressStatus.html', {'form': form, 'subtask': subtask})