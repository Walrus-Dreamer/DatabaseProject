import mysql.connector

log = True


class UserGenerator:
    @staticmethod
    def __create_db_admin(cursor):
        cursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';")

    @staticmethod
    def create_default_users(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_users log:")
        try:
            cursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';")
            cursor.execute("CREATE USER 'viewer'@'localhost' IDENTIFIED BY 'viewer';")
            cursor.execute(
                "CREATE USER 'event_manager'@'localhost' IDENTIFIED BY 'event_manager';"
            )
            cursor.execute(
                "CREATE USER 'impresario'@'localhost' IDENTIFIED BY 'impresario';"
            )
            if log:
                print("\t-Users created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create users: {}".format(error))
