from employees.models import MaintenanceAction


class StartMaintenanceAction:
    def check_proceed(self,queryset)->str:
        if len(queryset)==1:
            for maintenance_action in queryset:
                if maintenance_action.proceed:
                    output:str=self.proceed()
                    return output
                else:
                    return 'This maintenance action won\'t be completed because the option to proceed wasn\'t turned on when this maintenance option was created. This action can be completed by choosing another maintenance action that can proceed. If another maintenance action doesn\'t exist, create another maintenance action, and ensure that the option to proceed is turned on when creating it.'
        else:
            return 'This maintenance action won\'t be completed because only a single maintenance action can be chosen.'

    def proceed(self)->str:
        return 'Not available'