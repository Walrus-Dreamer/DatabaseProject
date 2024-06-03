import mysql.connector

log = True


class RolesGenerator:
    @staticmethod
    def delete_roles(connector):
        cursor = connector.cursor()
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'admin_role';")
            cursor.execute("DROP USER 'admin_role'@'localhost';")
            if log:
                print("\t-admin_role deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'viewer_role';")
            cursor.execute("DROP USER 'viewer_role'@'localhost';")
            if log:
                print("\t-viewer_role deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute(
                "DELETE FROM mysql.user WHERE User LIKE 'event_manager_role';"
            )
            cursor.execute("DROP USER 'event_manager_role'@'localhost';")
            if log:
                print("\t-event_manager_role deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'impresario_role';")
            cursor.execute("DROP USER 'impresario_role'@'localhost';")
            if log:
                print("\t-impresario_role deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))

        cursor.execute("FLUSH PRIVILEGES;")

    @staticmethod
    def __add_admin_role(cursor):
        cursor.execute("CREATE ROLE 'admin_role'@'localhost';")
        cursor.execute("GRANT ALL ON infosystem.* TO 'admin_role'@'localhost';")
        if log:
            print("\t-Admin role created successfully.")

    @staticmethod
    def __add_viewer_role(cursor):
        cursor.execute("CREATE ROLE 'viewer_role'@'localhost';")
        cursor.execute("GRANT SELECT ON infosystem.* TO 'viewer_role'@'localhost';")
        cursor.execute("GRANT EXECUTE ON infosystem.* TO 'viewer_role'@'localhost';")
        cursor.execute(
            "GRANT INSERT ON infosystem.favorite_actor_link TO 'viewer_role'@'localhost';"
        )
        if log:
            print("\t-Viewer role created successfully.")

    @staticmethod
    def __add_event_manager_role(cursor):
        cursor.execute("CREATE ROLE 'event_manager_role'@'localhost';")
        cursor.execute(
            "GRANT SELECT ON infosystem.* TO 'event_manager_role'@'localhost';"
        )
        cursor.execute(
            "GRANT INSERT ON infosystem.event TO 'event_manager_role'@'localhost';"
        )
        cursor.execute(
            "GRANT UPDATE ON infosystem.event TO 'event_manager_role'@'localhost';"
        )
        if log:
            print("\t-Event manager role created successfully.")

    @staticmethod
    def __add_impresario_role(cursor):
        cursor.execute("CREATE ROLE 'impresario_role'@'localhost';")
        cursor.execute("GRANT SELECT ON infosystem.* TO 'impresario_role'@'localhost';")
        cursor.execute(
            "GRANT INSERT ON infosystem.event TO 'impresario_role'@'localhost';"
        )
        cursor.execute(
            "GRANT INSERT ON infosystem.contest TO 'impresario_role'@'localhost';"
        )
        cursor.execute(
            "GRANT UPDATE ON infosystem.event TO 'impresario_role'@'localhost';"
        )
        if log:
            print("\t-Impresario role created successfully.")

    @staticmethod
    def __flush_privileges(cursor):
        cursor.execute("FLUSH PRIVILEGES;")
        if log:
            print("\t-Priveleges flushed successfully.")

    @staticmethod
    def create_default_roles(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_default_roles log:")
        try:
            RolesGenerator.delete_roles(connector)
            RolesGenerator.__flush_privileges(cursor)

            RolesGenerator.__add_admin_role(cursor)
            RolesGenerator.__add_viewer_role(cursor)
            RolesGenerator.__add_event_manager_role(cursor)
            RolesGenerator.__add_impresario_role(cursor)

            RolesGenerator.__flush_privileges(cursor)
            if log:
                print("\t-Default roles created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create default roles: {}".format(error))
