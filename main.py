from init.db_init import DbInitializer
from init.generators.dump_generator import DumpGenerator
from init.generators.roles_generator import RolesGenerator
from init.generators.tables_generator import TablesGenerator
from init.generators.users_generator import UserGenerator
from db_manager import DBManager

from gui import GUI
import mysql


class Kernel:
    def __init__(self):
        self.role = None

    def run(self):
        gui = GUI()
        root_login, root_password = gui.connect_to_db_screen()
        db_initer = DbInitializer(root_login, root_password)
        try:
            TablesGenerator.create_tables(db_initer.connector)
            TablesGenerator.create_triggers(db_initer.connector)
            TablesGenerator.create_procedures(db_initer.connector)
            TablesGenerator.create_functions(db_initer.connector)
            RolesGenerator.create_default_roles(db_initer.connector)
            # UserGenerator.create_default_users(db_initer.connector)
            DumpGenerator.create_dump(db_initer.connector)
        except mysql.connector.Error as error:
            print(f"Failed to generate data: {error}")

        self.role = gui.select_role()
        db_manager = DBManager(db_initer.connector)
        gui.set_db_manager(db_manager)

        next_window_name = "main_menu"
        while next_window_name != "exit":
            next_window_name = gui.handle_command(next_window_name, self.role)

        user_decision = input("Вы хотите очистить базу? (y/n): ")
        if user_decision == "y":
            RolesGenerator.delete_roles(db_initer.connector)
            db_initer.drop_db()


kernel = Kernel()
kernel.run()

# TODO: Фильтрация записей
# TODO: Выкидывать ошибку, если добавляемое событие уже есть в БД
