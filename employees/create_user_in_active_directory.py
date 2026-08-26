from ldap3 import BASE, Connection

from employees.check_existing_user import CheckExistingUser
from employees.models import Department, Employee, Office, RequiredGroups


class CreateUserInActiveDirectory:
    def create_new_user(self,employee:Employee)->None:
        check_existing_user:CheckExistingUser=CheckExistingUser()

        first_name_first_letter:str=employee.first_name[0]
        flast_user_principal_name_prefix:str=first_name_first_letter.lower()+employee.last_name.lower()
        flast_user_principal_name_prefix_exists:bool=check_existing_user.check(user_principal_name_prefix=flast_user_principal_name_prefix)

        if flast_user_principal_name_prefix_exists:
            first_last_user_principal_name_prefix:str=employee.first_name.lower()+'.'+employee.last_name.lower()
            first_last_user_principal_name_prefix_exists:bool=check_existing_user.check(user_principal_name_prefix=first_last_user_principal_name_prefix)

            if first_last_user_principal_name_prefix_exists:
                print('Not created because both of the options for the User Principal Name prefix aren\'t available')
            else:
                print('first.last option chosen, and the User Principal Name prefix will be '+first_last_user_principal_name_prefix)
                self.create_user(employee=employee,user_principal_name_prefix=first_last_user_principal_name_prefix)
        else:
            print('flast option chosen, and the User Principal Name prefix will be '+flast_user_principal_name_prefix)
            self.create_user(employee=employee,user_principal_name_prefix=flast_user_principal_name_prefix)

    def create_user(self,employee:Employee,user_principal_name_prefix:str)->None:
        from employees.create_connection import CreateConnection
        create_connection:CreateConnection=CreateConnection()
        connection:Connection=create_connection.create_connection()

        department:Department=employee.department

        from ldap3.utils.dn import escape_rdn
        distinguished_name:str='CN='+escape_rdn(employee.retrieve_common_name())+',OU='+escape_rdn(department.retrieve_ou(employee=employee))+',OU=Option,DC=testing,DC=ca'

        try:
            add_success:bool=self.add(employee=employee,user_principal_name_prefix=user_principal_name_prefix,connection=connection,distinguished_name=distinguished_name)

            if add_success:
                self.modify(employee=employee,connection=connection,distinguished_name=distinguished_name)
                self.required_groups(connection=connection,distinguished_name=distinguished_name)
                self.department_group(employee=employee,connection=connection,distinguished_name=distinguished_name)
                self.extra_groups(employee=employee,connection=connection,distinguished_name=distinguished_name)
        finally:
            connection.unbind()

    def add(self,employee:Employee,user_principal_name_prefix:str,connection:Connection,distinguished_name:str)->bool:
        user_principal_name:str=user_principal_name_prefix+'@testing.ca'

        add_success:bool=connection.add(
            distinguished_name,
            ['top', 'person', 'organizationalPerson', 'user'],
            {
                'cn': employee.retrieve_common_name(),
                'sn': employee.last_name,
                'givenName': employee.first_name,
                'displayName': employee.retrieve_common_name(),
                'sAMAccountName': user_principal_name_prefix[:20],
                'userPrincipalName': user_principal_name
            }
        )

        print("add_success",add_success)
        print("LDAP",connection.result)

        return add_success

    def modify(self,employee:Employee,connection:Connection,distinguished_name:str)->None:
        from ldap3 import MODIFY_REPLACE

        # Set password
        modify_password_success:bool=connection.extend.microsoft.modify_password(distinguished_name,'testing')

        print("modify_password_success",modify_password_success)
        print("LDAP",connection.result)

        # Enable account
        modify_success:bool=connection.modify(
            distinguished_name,
            {
                'userAccountControl': [
                    (MODIFY_REPLACE, [512])  # NORMAL_ACCOUNT
                ]
            }
        )

        print("modify_success",modify_success)
        print("LDAP",connection.result)

        office:Office=employee.office
        department:Department=employee.department

        modify_success:bool=connection.modify(
            distinguished_name,
            {
                'initials': [(MODIFY_REPLACE, [first_name_first_letter+last_name_first_letter])],
                'description': [(MODIFY_REPLACE, [employee.role])],
                'department': [(MODIFY_REPLACE, [department.name])],
                'streetAddress': [(MODIFY_REPLACE, [office.street])],
                'l': [(MODIFY_REPLACE, [office.city])],
                'st': [(MODIFY_REPLACE, [office.province])],
                'postalCode': [(MODIFY_REPLACE, [office.postal_code])],
                'c': [(MODIFY_REPLACE, ['CA'])],
                'co': [(MODIFY_REPLACE, ['Canada'])],
                'countryCode': [(MODIFY_REPLACE, [124])],
                'telephoneNumber': [(MODIFY_REPLACE, [office.phone+' x'])]
            }
        )

        print("modify_success",modify_success)
        print("LDAP",connection.result)

    def required_groups(self,connection:Connection,distinguished_name:str)->None:
        required_groups:RequiredGroups=RequiredGroups()

        for required_group in required_groups.retrieve():
            add_group_success:bool=connection.extend.microsoft.add_members_to_groups(distinguished_name,required_group.distinguished_name)
                        
            print("add_group_success "+required_group.distinguished_name,add_group_success)
            print("LDAP",connection.result)

    def department_group(self,employee:Employee,connection:Connection,distinguished_name:str)->None:
        department:Department=employee.department
        department_group_distinguished_name:str=department.retrieve_group_distinguished_name(office=employee.office)

        if department_group_distinguished_name!='':
            group_exists:bool=connection.search(search_base=department_group_distinguished_name,search_filter='(objectClass=group)',search_scope=BASE)

            if group_exists:
                add_group_success=connection.extend.microsoft.add_members_to_groups(distinguished_name,department_group_distinguished_name)

                print("add_group_success "+department_group_distinguished_name,add_group_success)
                print("LDAP",connection.result)
            else:
                print('Group doesn\'t exist '+department_group_distinguished_name)

    def extra_groups(self,employee:Employee,connection:Connection,distinguished_name:str)->None:
        for extra_group in employee.extra_groups.all():
            add_group_success:bool=connection.extend.microsoft.add_members_to_groups(distinguished_name,extra_group.distinguished_name)

            print("add_group_success "+extra_group.distinguished_name,add_group_success)
            print("LDAP",connection.result)