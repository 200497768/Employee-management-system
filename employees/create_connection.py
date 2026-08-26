from ldap3 import Connection


class CreateConnection:
    def create_connection(self)->Connection:
        from ldap3 import Server, Connection, ALL

        import os
        from dotenv import load_dotenv
        load_dotenv()
        print('Confirming whether able to retrieve confirmation text',os.environ['CONFIRMATION'])

        # Connect to LDAP server
        server:Server=Server(
            os.environ['LDAP_HOST'],
            use_ssl=True,
            get_info=ALL
        )

        from ldap3 import NTLM
        connection:Connection=Connection(server,os.environ['LDAP_USER'],os.environ['LDAP_PASSWORD'], authentication=NTLM, auto_bind=True)

        return connection