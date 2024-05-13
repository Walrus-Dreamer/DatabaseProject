import mysql.connector

log = True


class DBManager:
    def __init__(self, connector):
        self.cursor = connector.cursor()

    def select_all_from(self, table_name):
        # TODO: add make this function in db
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def select_actors(self):
        self.cursor.execute(
            """
                            SELECT actor.id,
                                    event.name as event_name,
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
                                    event.name,
                                    event.genre_name,
                                    impresario.name as impresario_name,
                                    impresario.surname as impresario_surname,
                                    event.creation_date
                            FROM event
                            JOIN impresario ON event.impresario_id = impresario.id
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

    def insert_event(self, name, genre_name, impresario_id):
        self.cursor.execute(
            f"CALL add_event('{name}', '{genre_name}', {impresario_id})"
        )

    def print_select_all(self, table_name):
        print(f"{table_name}:")
        result = ""
        for row in self.select_all(table_name):
            print(result)
            result += repr(row) + "\n"
        return result