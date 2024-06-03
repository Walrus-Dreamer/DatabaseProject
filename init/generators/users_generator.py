import mysql.connector

log = True


class UsersGenerator:
    @staticmethod
    def delete_users(connector):
        cursor = connector.cursor()
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'admin';")
            cursor.execute("DROP USER 'admin'@'localhost';")
            if log:
                print("\t-admin deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'viewer';")
            cursor.execute("DROP USER 'viewer'@'localhost';")
            if log:
                print("\t-viewer deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'event_manager';")
            cursor.execute("DROP USER 'event_manager'@'localhost';")
            if log:
                print("\t-event_manager deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'impresario';")
            cursor.execute("DROP USER 'impresario'@'localhost';")
            if log:
                print("\t-impresario deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))

        cursor.execute("FLUSH PRIVILEGES;")

    @staticmethod
    def __add_admin_user(cursor):
        cursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY '1';")
        cursor.execute("GRANT 'admin_role'@'localhost' TO 'admin'@'localhost';")
        cursor.execute("GRANT SUPER ON *.* TO 'admin'@'localhost';")
        if log:
            cursor.execute(
                "GRANT ALL ON infosystem.* TO 'admin'@'localhost'  WITH GRANT OPTION;"
            )
            cursor.execute("GRANT EXECUTE ON *.* TO 'admin'@'localhost';")
            cursor.execute(
                "GRANT CREATE USER ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;"
            )
        if log:
            print("\t-Admin user created successfully.")

    @staticmethod
    def __add_viewer_user(cursor):
        cursor.execute("CREATE USER 'viewer'@'localhost' IDENTIFIED BY '1';")
        # cursor.execute("GRANT 'viewer_role'@'localhost' TO 'viewer'@'localhost';")
        if log:
            cursor.execute("GRANT SELECT ON infosystem.* TO 'viewer'@'localhost';")
            cursor.execute("GRANT EXECUTE ON infosystem.* TO 'viewer'@'localhost';")
            cursor.execute(
                "GRANT INSERT ON infosystem.favorite_actor_link TO 'viewer'@'localhost';"
            )
        if log:
            print("\t-Viewer user created successfully.")

    @staticmethod
    def __add_event_manager_user(cursor):
        cursor.execute("CREATE USER 'event_manager'@'localhost' IDENTIFIED BY '1';")
        # cursor.execute(
        #     "GRANT 'event_manager_role'@'localhost' TO 'event_manager'@'localhost';"
        # )
        if log:
            cursor.execute(
                "GRANT SELECT ON infosystem.* TO 'event_manager'@'localhost';"
            )
            cursor.execute(
                "GRANT EXECUTE ON infosystem.* TO 'event_manager'@'localhost';"
            )
        if log:
            print("\t-Event manager user created successfully.")

    @staticmethod
    def __add_impresario_user(cursor):
        cursor.execute("CREATE USER 'impresario'@'localhost' IDENTIFIED BY '1';")
        cursor.execute(
            "GRANT 'impresario_role'@'localhost' TO 'impresario'@'localhost';"
        )
        if log:
            cursor.execute("GRANT SELECT ON infosystem.* TO 'impresario'@'localhost';")
            cursor.execute("GRANT EXECUTE ON infosystem.* TO 'impresario'@'localhost';")
        if log:
            print("\t-Impresario user created successfully.")

    @staticmethod
    def __flush_privileges(cursor):
        cursor.execute("FLUSH PRIVILEGES;")
        if log:
            print("\t-Priveleges flushed successfully.")

    @staticmethod
    def create_default_users(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_default_users log:")
        try:
            UsersGenerator.delete_users(connector)

            UsersGenerator.__flush_privileges(cursor)

            UsersGenerator.__add_admin_user(cursor)
            UsersGenerator.__add_viewer_user(cursor)
            UsersGenerator.__add_event_manager_user(cursor)
            UsersGenerator.__add_impresario_user(cursor)

            UsersGenerator.__flush_privileges(cursor)
            if log:
                print("\t-Default users created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create default users: {}".format(error))
