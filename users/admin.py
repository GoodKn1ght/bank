from django.contrib import admin
from .models import User, Person, Extract

class UserAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Terms_Of_Use', 'Mother_Surname', 'Money_Left', 'User_Created')
    search_fields = ('ID', 'Mother_Surname')
    list_filter = ('User_Created',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Phone_Number', 'Email')
    search_fields = ('Phone_Number', 'Email')

class ExtractAdmin(admin.ModelAdmin):
    list_display = ('Time_started', 'Money_Used', 'Operation_Type', 'initial_balance')
    search_fields = ('Operation_Type',)
    list_filter = ('Time_started',)

# Register models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Extract, ExtractAdmin)
