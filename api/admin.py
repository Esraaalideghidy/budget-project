from django.contrib import admin

# Register your models here.


from .models import User,Expenses,Plan,PlanItems

admin.site.register(User)
admin.site.register(Expenses)
admin.site.register(Plan)
admin.site.register(PlanItems)
