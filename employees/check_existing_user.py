from ldap3 import Connection
from ldap3.utils.conv import escape_filter_chars

from employees.create_connection import CreateConnection


class CheckExistingUser:
    def check(self,user_principal_name_prefix:str)->bool:
        create_connection:CreateConnection=CreateConnection()
        connection:Connection=create_connection.create_connection()

        user_principal_name:str=user_principal_name_prefix+'@testing.ca'

        connection.search(
            search_base='DC=testing,DC=ca',
            search_filter='(userPrincipalName='+escape_filter_chars(user_principal_name)+')'
        )

        user_exists=len(connection.entries)>0

        connection.unbind()

        return user_exists