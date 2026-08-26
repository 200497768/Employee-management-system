from employees.offices import Offices
from employees.start_maintenance_action import StartMaintenanceAction


class CreateOffices(StartMaintenanceAction):
    def proceed(self)->str:
        offices:Offices=Offices()
        offices.create()
        
        return 'Offices created.'