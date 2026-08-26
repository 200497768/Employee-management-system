from ldap3 import Connection
from ldap3.utils.conv import escape_filter_chars

from employees.create_connection import CreateConnection


class RetrieveExistingGroups:
    def retrieve(self,user_principal_name_prefix:str)->list[str]:
        create_connection:CreateConnection=CreateConnection()
        connection:Connection=create_connection.create_connection()

        try:
            user_principal_name:str=user_principal_name_prefix+'@testing.ca'

            connection.search(search_base='DC=testing,DC=ca',search_filter='(userPrincipalName='+escape_filter_chars(user_principal_name)+')',attributes=['memberOf'])

            required_groups:list[str]=['CN=Required group,OU=Groups,OU=Option,DC=testing,DC=ca','CN=Most employees,OU=Groups,OU=Option,DC=testing,DC=ca']

            if not connection.entries:
                return required_groups

            entry = connection.entries[0]

            if 'memberOf' not in entry:
                return required_groups

            return list(entry.memberOf.values)
        finally:
            connection.unbind()