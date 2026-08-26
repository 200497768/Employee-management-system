from django.contrib import admin

from employees.check_reference_users import CheckReferenceUsers
from employees.create_departments import CreateDepartments
from employees.create_offices import CreateOffices
from employees.create_user_in_active_directory import CreateUserInActiveDirectory
from employees.test_powershell import TestPowerShell

# Register your models here.

from .models import Department, Employee, Group, MaintenanceAction, ReferenceUser

from .models import Office


from .models import Employee, Office

from django.contrib import messages

class EmployeeAdmin(admin.ModelAdmin):
    fields = ['first_name','last_name','role','manager','office','department','student','reference_user','extra_groups']

    actions = ['create_user','retrieve_extra_groups']

    @admin.action(description='Create user in Active Directory')
    def create_user(self, request, queryset)->None:
        for employee in queryset:
            create_user_in_active_directory:CreateUserInActiveDirectory=CreateUserInActiveDirectory()
            create_user_in_active_directory.create_new_user(employee=employee)

        self.message_user(
            request,
            'The action to create user in Active Directory was completed.',
            messages.SUCCESS,
        )

    @admin.action(description='Retrieve extra groups using reference user')
    def retrieve_extra_groups(self, request, queryset)->None:
        for employee in queryset:
            employee.retrieve_extra_groups()

        self.message_user(
            request,
            'The action to create retrieve extra groups using reference user was completed.',
            messages.SUCCESS,
        )

class ReferenceUserAdmin(admin.ModelAdmin):
    fields = ['user_principal_name_prefix','confirmed_exists','extra_groups']

    actions = ['check_reference_users']

    @admin.action(description='Check whether reference users exist in Active Directory and retrieve extra groups')
    def check_reference_users(self, request, queryset)->None:
        for reference_user in queryset:
            reference_user.retrieve()

        self.message_user(
            request,
            'The action to check whether reference users exist in Active Directory and retrieve extra groups was completed.',
            messages.SUCCESS,
        )

class MaintenanceActionAdmin(admin.ModelAdmin):
    fields = ['proceed']

    actions = ['test_powershell','create_departments','create_offices','check_reference_users']

    @admin.action(description='Test PowerShell')
    def test_powershell(self, request, queryset)->None:
        test_powershell:TestPowerShell=TestPowerShell()
        output:str=test_powershell.check_proceed(queryset=queryset)

        self.message_user(request,output,messages.SUCCESS,)

    @admin.action(description='Create departments')
    def create_departments(self, request, queryset)->None:
        create_departments:CreateDepartments=CreateDepartments()
        output:str=create_departments.check_proceed(queryset=queryset)

        self.message_user(request,output,messages.SUCCESS,)

    @admin.action(description='Create offices')
    def create_offices(self, request, queryset)->None:
        create_offices:CreateOffices=CreateOffices()
        output:str=create_offices.check_proceed(queryset=queryset)

        self.message_user(request,output,messages.SUCCESS,)

    @admin.action(description='Check whether reference users exist in Active Directory and retrieve extra groups')
    def check_reference_users(self, request, queryset)->None:
        check_reference_users:CheckReferenceUsers=CheckReferenceUsers()
        output:str=check_reference_users.check_proceed(queryset=queryset)

        self.message_user(request,output,messages.SUCCESS,)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Office)
admin.site.register(Department)
admin.site.register(ReferenceUser, ReferenceUserAdmin)
admin.site.register(Group)
admin.site.register(MaintenanceAction, MaintenanceActionAdmin)