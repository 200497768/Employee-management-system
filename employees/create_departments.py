from employees.departments import Departments
from employees.offices import Offices
from employees.start_maintenance_action import StartMaintenanceAction


class CreateDepartments(StartMaintenanceAction):
    def proceed(self)->str:
        departments:Departments=Departments()
        departments.create()
        
        return 'Departments created.'