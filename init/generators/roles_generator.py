import mysql.connector

log = True


class RolesGenerator:
    @staticmethod
    def __refresh_roles(cursor):
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'admin';")
            cursor.execute("DROP USER 'admin'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'viewer';")
            cursor.execute("DROP USER 'viewer'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'event_manager';")
            cursor.execute("DROP USER 'event_manager'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'impresario';")
            cursor.execute("DROP USER 'impresario'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))

        cursor.execute("FLUSH PRIVILEGES;")

    @staticmethod
    def __add_admin_role(cursor):
        cursor.execute("CREATE ROLE 'admin'@'localhost';")
        cursor.execute("GRANT ALL ON theatre.* TO 'admin'@'localhost';")
        if log:
            print("-Admin role created successfully.")

    @staticmethod
    def __add_viewer_role(cursor):
        cursor.execute("CREATE ROLE 'viewer'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'viewer'@'localhost';")
        if log:
            print("-Viewer role created successfully.")

    @staticmethod
    def __add_event_manager_role(cursor):
        cursor.execute("CREATE ROLE 'event_manager'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'event_manager'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.event TO 'event_manager'@'localhost';")
        cursor.execute("GRANT UPDATE ON theatre.event TO 'event_manager'@'localhost';")
        if log:
            print("-Event manager role created successfully.")

    @staticmethod
    def __add_impresario_role(cursor):
        cursor.execute("CREATE ROLE 'impresario'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'impresario'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.event TO 'impresario'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.contest TO 'impresario'@'localhost';")
        cursor.execute("GRANT UPDATE ON theatre.event TO 'impresario'@'localhost';")
        if log:
            print("-Impresario role created successfully.")

    @staticmethod
    def create_default_roles(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_default_roles log:")
        try:
            RolesGenerator.__refresh_roles(cursor)
            RolesGenerator.__add_admin_role(cursor)
            RolesGenerator.__add_viewer_role(cursor)
            RolesGenerator.__add_event_manager_role(cursor)
            RolesGenerator.__add_impresario_role(cursor)
            if log:
                print("\t-Roles created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create roles: {}".format(error))