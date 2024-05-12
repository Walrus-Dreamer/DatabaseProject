from glebglebglebglebgleb_part3 import (
    DbInitializer,
    TablesGenerator,
    DumpGenerator,
    DBManager,
)
from gui import GUI
import mysql


class Kernel:
    def __init__(self):
        self.role = None

    def run(self):
        gui = GUI()
        login, password = gui.connect_to_db_screen()
        db_initer = DbInitializer(login, password)
        try:
            TablesGenerator.create_tables(db_initer.connector)
            TablesGenerator.create_triggers(db_initer.connector)
            TablesGenerator.create_procedures(db_initer.connector)
            TablesGenerator.create_functions(db_initer.connector)
            DumpGenerator.create_dump(db_initer.connector)
        except mysql.connector.Error as error:
            print(f"Failed to generate data: {error}")

        self.role = gui.select_role()
        db_manager = DBManager(db_initer.connector)
        gui.set_db_manager(db_manager)

        next_window_name = "main_menu"
        while next_window_name != "exit":
            next_window_name = gui.handle_command(next_window_name, self.role)
        # return
        db_initer.drop_db()


kernel = Kernel()
kernel.run()

# TODO: Фильтрация записей
# TODO: Выкидывать ошибку, если добавляемое событие уже есть в БД
