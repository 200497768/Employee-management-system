
from employees.models import Department


class Departments:
    administration:Department=Department(name='Administration',group_name='Administration',multiple_office_groups=False,choose_group=False)
    information_technology:Department=Department(name='Information Technology',group_name='Information Technology',multiple_office_groups=False,choose_group=True)
    departments:list[Department]=[administration,information_technology]

    def create(self)->None:
        for department in self.departments:
            department.save()