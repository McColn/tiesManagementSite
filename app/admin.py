from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Clients)
admin.site.register(Project)
admin.site.register(ProjectInvoice)
admin.site.register(ProjectPayment)
admin.site.register(ProjectBudget)
admin.site.register(ProjectExpense)
admin.site.register(ProjectUpdate)
admin.site.register(ProjectPurchases)
admin.site.register(PurchasesAccumulated)
admin.site.register(ProjectDirectCost)
admin.site.register(Assignment)
admin.site.register(AssignmentUpdates)
admin.site.register(Leaves)
admin.site.register(Event)
admin.site.register(SalaryAdvance)
admin.site.register(Company)