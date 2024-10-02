
from django.urls import path
from . import views
from .views import user_details

urlpatterns = [
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employees, name='employees'),
    path('employeesDetails/<int:id>/', views.employeesDetails, name='employeesDetails'),
    path('project/', views.project, name='project'),
    path('projectAdd/', views.projectAdd, name='projectAdd'),
    path('projectEdit/<int:id>/', views.projectEdit, name='projectEdit'),
    path('projectDetails/<int:id>/', views.projectDetails, name='projectDetails'),
    path('projectInvoiceAdd/<int:project_id>/', views.projectInvoiceAdd, name='projectInvoiceAdd'),
    path('projectPaymentAdd/<int:project_id>/', views.projectPaymentAdd, name='projectPaymentAdd'),
    path('projectExpensesAdd/<int:project_id>/', views.projectExpensesAdd, name='projectExpensesAdd'),
    path('projectBudgetAdd/<int:project_id>/', views.projectBudgetAdd, name='projectBudgetAdd'),
    path('projectRemarkAdd/<int:project_id>/', views.projectRemarkAdd, name='projectRemarkAdd'),

    path('clients/', views.clients, name='clients'),
    path('clientDetails/<int:id>/', views.clientDetails, name='clientDetails'),
    path('clientAdd/', views.clientAdd, name='clientAdd'),
    path('basicInfo/<int:id>/', views.basicInfo, name='basicInfo'),
    path('personalInfo/<int:id>/', views.personalInfo, name='personalInfo'),
    path('educationInfo/<int:id>/', views.educationInfo, name='educationInfo'),
    path('contractInfo/<int:id>/', views.contractInfo, name='contractInfo'),
    path('assignment/', views.assignment, name='assignment'),
    path('assignmentAdd/', views.assignmentAdd, name='assignmentAdd'),
    path('assignmentDetails/<int:id>/', views.assignmentDetails, name='assignmentDetails'),
    path('assignmentDetailsAdd/<int:assignment_id>/', views.assignmentDetailsAdd, name='assignmentDetailsAdd'),

    path('leaves/', views.leaves, name='leaves'),
    path('leavesRequest/', views.leavesRequest, name='leavesRequest'),
    path('leavesDetails/<int:id>/', views.leavesDetails, name='leavesDetails'),
    path('leavesActions/<int:id>/', views.leavesActions, name='leavesActions'),

    path('user/details/', user_details, name='user_details'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('company/', views.company, name='company'),

]