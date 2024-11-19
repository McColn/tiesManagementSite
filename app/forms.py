from django import forms
from .models import *
from django.db.models import Sum

class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
                  'first_name','last_name','middle_name',
                  'username','email','phone','image',
                  'gender','birthDate'
                  ]
        

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
                  'nextKinName','nextKinRelation','nextKinAddress',
                  'nextKinPhone','nida','homeAddress'
                  ]
        
class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
                  'uniName','uniLevel','uniCourse',
                  'startYear','endYear'
                  ]
        
class ContractInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
                  'role','signedDate','expireDate',
                  'attachment'
                  ]
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        # Calculate remain duration
        if instance.expireDate:
            today = timezone.now().date()
            delta = relativedelta(instance.expireDate, today)
            instance.remainDuration = f'{delta.years * 12 + delta.months} months'
        instance.save()
        return instance
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = [
                  'clientName','address','representativeName',
                  'representativeTitle','email','phone'
                  ]
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
                  'title','client','location','startDate','endDate','person_in_charge'
                  ]
    

class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
                  'title','client','location','startDate','endDate','status'
                  ]
        
class ProjectExpensesForm(forms.ModelForm):
    class Meta:
        model = ProjectExpense
        fields = [
                  'title','description',
                  'amount'
                  ]
        
class ProjectBudgetForm(forms.ModelForm):
    class Meta:
        model = ProjectBudget
        fields = [
                  'title','description',
                  'amount'
                  ]

class ProjectInvoiceForm(forms.ModelForm):
    class Meta:
        model = ProjectInvoice
        fields = [
                  'title','description',
                  'amount'
                  ]

class ProjectPaymentForm(forms.ModelForm):
    class Meta:
        model = ProjectPayment
        fields = [
                  'title',
                  'amount'
                  ]
               
class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = [
                  'description'
                  ]
        
class AssignmentAddForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
                  'assigned_to','description','dueDate'
                  ]
        
class AssignmentUpdatesForm(forms.ModelForm):
    class Meta:
        model = AssignmentUpdates
        fields = [
                  'description'
                  ]
        
class LeavesRequestForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = [
                  'leaveType','leave_reason','startDate',
                  'endDate'
                  ]
        

class LeavesActionForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = [
                  'action','action_reason'
                  ]
        
class SalaryAdvanceForm(forms.ModelForm):
    class Meta:
        model = SalaryAdvance
        fields = [
                  'typeOf','amount'
                  ]
        
class SalaryAdvanceActionForm(forms.ModelForm):
    class Meta:
        model = SalaryAdvance
        fields = [
                  'status'
                  ]
        
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
                  'title','category','pdfFile'
                  ]