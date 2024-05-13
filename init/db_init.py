import mysql.connector


# user_login = input("Enter your login: ")

# user_answer = input("Does your database has password? (y/n): ")
# user_password = None
# if user_answer == "y":
#     user_password = input("Enter your password: ")

# user_answer = input("Do you want to enable logging? (y/n): ")
# log = False
# if user_answer == "y":
#     log = True
log = True


class DbInitializer:
    def __init__(self, username="root", password=None):
        self.username = username
        self.password = password
        connector = mysql.connector.connect(
            host="localhost", user=username, password=password
        )
        connector.autocommit = True
        cursor = connector.cursor()
        if log:
            print("\ndb_initer log:")
        try:
            cursor.execute("CREATE DATABASE theatre")
            if log:
                print("\t-Database created successfully.")
        except mysql.connector.Error:
            if log:
                print("\t-Database already exists.")

        self.connector = mysql.connector.connect(
            host="localhost", user="root", password=password, database="theatre"
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()

    # TODO: close connector and cursor in destructor
    # def __del__(self):
    #     self.cursor.close()
    #     self.connector.close()
