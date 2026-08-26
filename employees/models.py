from django.db import models
from django.db.models import QuerySet

from employees.check_existing_user import CheckExistingUser
from employees.retrieve_existing_groups import RetrieveExistingGroups

# Create your models here.

class Office(models.Model):
    name=models.CharField(max_length=200,unique=True)
    street=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    province=models.CharField(max_length=200)
    postal_code=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    group_name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=200,unique=True)
    group_name=models.CharField(max_length=200,unique=True)
    multiple_office_groups=models.BooleanField(default=False)
    choose_group=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def retrieve_group_name(self,office:Office)->str:
        combined_department_and_office_group_names:str=self.combine_department_and_office_group_names(office=office)

        if self.name=='Group that isn\'t included':
            return ''

        if combined_department_and_office_group_names=='Group that needs to be changed':
            return 'Change group'

        return combined_department_and_office_group_names

    def combine_department_and_office_group_names(self,office:Office)->str:
        if self.multiple_office_groups:
            return self.group_name+'-'+office.group_name
        else:
            return self.group_name

    def retrieve_group_distinguished_name(self,office:Office)->str:
        group_name:str=self.retrieve_group_name(office=office)

        if group_name=='':
            return ''

        if self.choose_group:
            return 'CN='+group_name+',OU=Groups,OU=Option,DC=testing,DC=ca'
        else:
            return 'CN='+group_name+',OU=Groups,OU=Another option,DC=testing,DC=ca'

    def retrieve_ou(self,employee:Employee)->str:
        if employee.student:
            return 'Students'
        elif self.name=='Another department':
            return 'Another department'
        else:
            return 'Most of our employees'

class Group(models.Model):
    distinguished_name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.distinguished_name

    def __eq__(self,other:Group)->bool:
        return self.distinguished_name==other.distinguished_name

    def __hash__(self):
        return hash(self.distinguished_name)

class CheckExtraGroup:
    def check_extra_group(self,group:Group)->bool:
        created_groups:list[Group]=self.create_groups()

        change_to_extra_groups:list[Group]=self.retrieve_change_to_extra_groups()
        for change_to_extra_group in change_to_extra_groups:
            if change_to_extra_group in created_groups:
                created_groups.remove(change_to_extra_group)

        extra_group:bool=not group in created_groups
        return extra_group

    def create_groups(self)->list[Group]:
        required_groups:RequiredGroups=RequiredGroups()

        groups:list[Group]=required_groups.retrieve()

        departments:list[Department]=Department.objects.all()
        offices:list[Office]=Office.objects.all()

        return groups

class RequiredGroups:
    def retrieve(self)->list[Group]:
        required_group:Group=Group(distinguished_name='CN=Required group,OU=Groups,OU=Option,DC=testing,DC=ca')
        most_employees:Group=Group(distinguished_name='CN=Most employees,OU=Groups,OU=Option,DC=testing,DC=ca')

        groups:list[Group]=[required_group,most_employees]

        return groups

class ReferenceUser(models.Model):
    user_principal_name_prefix=models.CharField(max_length=200,unique=True)
    confirmed_exists=models.BooleanField(default=False)
    extra_groups=models.ManyToManyField(Group,blank=True)

    def retrieve(self)->None:
        self.change_confirmed_exists()
        self.change_extra_groups()

    def change_confirmed_exists(self)->None:
        check_existing_user:CheckExistingUser=CheckExistingUser()
        self.confirmed_exists=check_existing_user.check(user_principal_name_prefix=self.user_principal_name_prefix)

        self.save()

    def change_extra_groups(self)->None:
        self.extra_groups.clear()

        if self.confirmed_exists:
            retrieve_existing_groups:RetrieveExistingGroups=RetrieveExistingGroups()
            retrieved_extra_groups:list[str]=retrieve_existing_groups.retrieve(user_principal_name_prefix=self.user_principal_name_prefix)

            for retrieved_extra_group in retrieved_extra_groups:
                check_extra_group:CheckExtraGroup=CheckExtraGroup()
                created_group:Group=Group(distinguished_name=retrieved_extra_group)

                if check_extra_group.check_extra_group(group=created_group):
                    Group.objects.get_or_create(distinguished_name=retrieved_extra_group)
                    extra_group:Group=Group.objects.get(distinguished_name=retrieved_extra_group)
                    extra_group.save()

                    self.extra_groups.add(extra_group)

        self.save()

    def __str__(self):
        return self.user_principal_name_prefix

class Employee(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    role=models.CharField(max_length=200)
    manager=models.CharField(max_length=200)
    office=models.ForeignKey(Office,on_delete=models.PROTECT)
    department=models.ForeignKey(Department,on_delete=models.PROTECT)
    student=models.BooleanField(default=False)
    reference_user=models.ForeignKey(ReferenceUser,on_delete=models.CASCADE,blank=True,null=True)
    extra_groups=models.ManyToManyField(Group,blank=True)

    def __str__(self):
        return self.first_name+' '+self.last_name

    def retrieve_common_name(self)->str:
        common_name:str=self.first_name+' '+self.last_name
        return common_name

    def retrieve_extra_groups(self)->None:
        reference_user:ReferenceUser=self.reference_user

        reference_user.retrieve()

        reference_user_extra_groups:QuerySet[Group]=reference_user.extra_groups.all()

        self.extra_groups.clear()

        for reference_user_extra_group in reference_user_extra_groups:
            self.extra_groups.add(reference_user_extra_group)

class MaintenanceAction(models.Model):
    proceed=models.BooleanField(default=False,unique=True)

    def __str__(self):
        if self.proceed:
            return 'Maintenance action that will proceed'
        else:
            return 'Maintenance action that won\'t proceed'