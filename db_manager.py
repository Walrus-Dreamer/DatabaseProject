import mysql.connector

log = True


class DBManager:
    def __init__(self, username="root", password=None):
        self.username = username
        self.password = password
        self.connector = mysql.connector.connect(
            host="localhost", user=username, password=password, database="infosystem"
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()

    def select_all_from(self, table_name):
        # TODO: Закинуть в хранимку.
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def select_actors(self):
        self.cursor.execute(
            """
                            SELECT actor.id,
                                    event.genre_name,
                                    building.name as building_name,
                                    actor.name,
                                    actor.surname,
                                    actor.age,
                                    actor.creation_date
                            FROM actor
                            JOIN event ON actor.event_id = event.id
                            JOIN building ON actor.building_id = building.id
                            """
        )
        return self.cursor.fetchall()

    def select_buildings(self):
        self.cursor.execute("SELECT * FROM building")
        return self.cursor.fetchall()

    def select_events(self):
        self.cursor.execute(
            """
                            SELECT event.id,
                                    building.name as building_name,
                                    event.name as event_name,
                                    event.genre_name as genre_name,
                                    impresario.name as impresario_name,
                                    impresario.surname as impresario_surname,
                                    event.creation_date
                            FROM event
                            JOIN impresario ON event.impresario_id = impresario.id
                            JOIN building ON impresario.building_id = building.id
                            """
        )
        return self.cursor.fetchall()

    def select_impresarios(self):
        self.cursor.execute(
            """
                            SELECT impresario.id,
                                    building.name,
                                    impresario.name,
                                    impresario.surname,
                                    impresario.age,
                                    impresario.creation_date
                            FROM impresario
                            JOIN building ON impresario.building_id = building.id
                            """
        )
        return self.cursor.fetchall()

    def select_genres(self):
        self.cursor.execute("SELECT * FROM genre")
        return self.cursor.fetchall()

    def select_contests(self):
        self.cursor.execute(
            """
            SELECT c.name AS contest_name, 
                a1.name AS first_place_name, a1.surname AS first_place_surname,
                a2.name AS second_place_name, a2.surname AS second_place_surname,
                a3.name AS third_place_name, a3.surname AS third_place_surname
            FROM contest c
            JOIN actor a1 ON c.first_place_id = a1.id
            JOIN actor a2 ON c.second_place_id = a2.id
            JOIN actor a3 ON c.third_place_id = a3.id;

            """
        )
        return self.cursor.fetchall()

    def create_event(
        self, name, genre_name, impresario_id, building_id, event_date, box_office
    ):
        self.cursor.execute(
            f"CALL add_event('{name}', '{genre_name}', {impresario_id}, {building_id}, '{event_date}', {box_office})"
        )

    def create_contest(self, name, first_place_id, second_place_id, third_place_id):
        self.cursor.execute(
            f"CALL add_contest('{name}', {first_place_id}, {second_place_id}, {third_place_id})"
        )

    def create_building(self, name, type):
        self.cursor.execute(f"CALL add_building('{name}', '{type}')")

    def print_select_all(self, table_name):
        print(f"{table_name}:")
        result = ""
        for row in self.select_all(table_name):
            print(result)
            result += repr(row) + "\n"
        return result

    def drop_db(self):
        self.connector = mysql.connector.connect(
            host="localhost", user=self.username, password=self.password
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()
        if log:
            print("\ndrop_db log:")
        try:
            self.cursor.execute("DROP DATABASE infosystem")
            if log:
                print("\t-Database deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print(f"\t-Dropping database failed: {error}.")

    def __get_my_username(self):
        self.cursor.execute("SELECT get_my_username();")
        return self.cursor.fetchone()[0]

    def get_my_role(self):
        self.cursor.execute(
            "SELECT role FROM username_role WHERE username_role.username like CURRENT_USER();"
        )
        self.role = self.cursor.fetchone()[0]
        return self.role

    def create_user(self, username, password, role):
        self.cursor.execute(
            f"INSERT INTO username_role VALUES ('{username}@localhost', '{role}');"
        )
        self.cursor.execute(
            f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
        )
        self.cursor.execute(
            f"GRANT SELECT ON infosystem.* TO '{username}'@'localhost';"
        )
        self.cursor.execute(
            f"GRANT EXECUTE ON infosystem.* TO '{username}'@'localhost';"
        )
