from employees.models import ReferenceUser
from employees.start_maintenance_action import StartMaintenanceAction


class CheckReferenceUsers(StartMaintenanceAction):
    def proceed(self)->str:
        reference_users:list[ReferenceUser]=ReferenceUser.objects.all()

        for reference_user in reference_users:
            reference_user.retrieve()
            
        return 'The maintenance action to check whether reference users exist in Active Directory and retrieve extra groups was completed.'