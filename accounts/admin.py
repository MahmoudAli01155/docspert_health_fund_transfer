from django.contrib import admin

# Register your models here.
from accounts.models import *



admin.site.register(Account)




@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass