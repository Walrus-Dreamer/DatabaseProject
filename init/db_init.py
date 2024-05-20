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
    def __init__(self, username="root", password=None, host="localhost", port=3306):
        # Это самый настоящий костыль, просот код захворал (как и я).
        # TODO: не передавать сюда пустые строки, если хост и порт не были указаны.
        if host == "" or not host:
            host = "localhost"
        if port == "" or not port:
            port = 3306
        else:
            port = int(port)
        self.username = username
        self.password = password
        connector = mysql.connector.connect(
            host=host, user=username, password=password, port=port
        )
        connector.autocommit = True
        cursor = connector.cursor()
        if log:
            print("\ndb_initer log:")
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS infosystem")
            if log:
                print("\t-Database created successfully.")
        except mysql.connector.Error:
            if log:
                print("\t-Database already exists.")

        self.connector = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            port=port,
            database="infosystem",
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()

    # TODO: УБИТЬ, НО НЕ ИСТЯЗАТЬ
    # def __del__(self):
    #     self.cursor.close()
    #     self.connector.close()
