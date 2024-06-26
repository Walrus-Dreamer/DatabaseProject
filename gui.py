import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self):
        self.current_window = None
        self.next_window_name = None
        self.db_manager = None
        self.username = None
        self.password = None
        self.host = None
        self.port = None

    def __default_login(self):
        self.username = "root"
        self.password = None
        self.current_window.destroy()

    def __submit(
        self,
        login_window,
        entry_username,
        entry_password,
        entry_host=None,
        entry_port=None,
    ):
        self.username = entry_username.get()
        self.password = entry_password.get()
        if entry_host and entry_port:
            self.host = entry_host.get()
            self.port = entry_port.get()
        login_window.destroy()
        self.current_window.destroy()

    def __open_login_window(self, login_as_user=False):
        login_window = tk.Toplevel(self.current_window)

        login_window.title("Вход")

        label_username = tk.Label(login_window, text="Логин:")
        label_username.pack()

        entry_username = tk.Entry(login_window)
        if not login_as_user:
            entry_username.insert(0, "root")
        entry_username.pack()

        label_password = tk.Label(login_window, text="Пароль:")
        label_password.pack()

        entry_password = tk.Entry(login_window, show="*")
        entry_password.pack()
        if not login_as_user:
            entry_password.insert(0, "root")

        if not login_as_user:
            label_host = tk.Label(login_window, text="Хост:")
            label_host.pack()

            entry_host = tk.Entry(login_window)
            entry_host.pack()
            entry_host.insert(0, "localhost")

            label_port = tk.Label(login_window, text="Порт:")
            label_port.pack()

            entry_port = tk.Entry(login_window)
            entry_port.pack()
            entry_port.insert(0, "3306")

            button_submit = tk.Button(
                login_window,
                text="Войти",
                command=lambda: self.__submit(
                    login_window=login_window,
                    entry_username=entry_username,
                    entry_password=entry_password,
                    entry_host=entry_host,
                    entry_port=entry_port,
                ),
            )
            button_submit.pack()
        else:
            button_submit = tk.Button(
                login_window,
                text="Войти",
                command=lambda: self.__submit(
                    login_window=login_window,
                    entry_username=entry_username,
                    entry_password=entry_password,
                ),
            )
            button_submit.pack()

    def connect_to_db_screen(self):
        self.current_window = tk.Tk()
        self.current_window.title("Подключение к базе данных")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        page_description_label = tk.Label(
            self.current_window,
            text="На данной странице необходимо подключиться к БД как root пользователь. После этого будет создан администратор БД.",
        )
        default_login_btn = tk.Button(
            self.current_window,
            text="Вход по умолчанию (логин: root, без пароля).",
            command=self.__default_login,
        )
        login_btn = tk.Button(
            self.current_window,
            text="Вход c вводом логина и пароля",
            command=self.__open_login_window,
        )
        page_description_label.pack()
        default_login_btn.pack()
        login_btn.pack()

        self.current_window.mainloop()
        return self.username, self.password, self.host, self.port

    def set_db_manager(self, db_manager):
        self.db_manager = db_manager

    def __pick_role(self, role_name):
        self.role = role_name
        self.current_window.destroy()

    def sign_in(self):
        self.current_window = tk.Tk()
        self.current_window.title("Вход в систему")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        self.next_window_name = "main_menu"

        self.username = None
        self.password = None

        sign_in_btn = tk.Button(
            self.current_window,
            text="Войти",
            command=lambda: self.__open_login_window(login_as_user=True),
        )
        sign_in_btn.pack()

        exit_btn = tk.Button(
            self.current_window,
            text="Завершить работу",
            command=lambda: self.__set_next_window("exit"),
        )
        exit_btn.pack()

        self.current_window.mainloop()

        return self.username, self.password, self.next_window_name

    def __set_create_db(self, create_db):
        self.create_db = create_db
        self.current_window.destroy()

    def create_db_modal(self):
        self.current_window = tk.Tk()
        self.current_window.title("Вы хотите создать базу данных?")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        yes_btn = tk.Button(
            self.current_window,
            text="Да",
            command=lambda: self.__set_create_db(True),
        )
        yes_btn.pack()

        no_btn = tk.Button(
            self.current_window,
            text="Нет",
            command=lambda: self.__set_create_db(False),
        )
        no_btn.pack()

        self.current_window.mainloop()

        return self.create_db

    def get_role(self):
        return self.role

    def __set_next_window(self, next_window_name):
        self.next_window_name = next_window_name
        self.current_window.destroy()

    def __filter_actors(self):
        filter_actors_window = tk.Toplevel(self.current_window)
        filter_actors_window.title("Фильтры")
        self.selected_genre_filter = None
        self.selected_building_filter = None

        genres = [genre[0] for genre in self.db_manager.select_genres()]
        genres.append("Любой")
        genres = genres[::-1]

        buildings = [building[1] for building in self.db_manager.select_buildings()]
        buildings.append("Любое")
        buildings = buildings[::-1]

        genre_label = tk.Label(filter_actors_window, text="Жанр:")
        genre_label.pack()
        genre_combobox = ttk.Combobox(
            filter_actors_window, values=genres, state="readonly"
        )
        genre_combobox.current(0)
        genre_combobox.pack()

        building_label = tk.Label(filter_actors_window, text="Место работы:")
        building_label.pack()
        building_combobox = ttk.Combobox(
            filter_actors_window, values=buildings, state="readonly"
        )
        building_combobox.current(0)
        building_combobox.pack()

        def accept():
            self.selected_genre_filter = genre_combobox.get()
            self.selected_building_filter = building_combobox.get()
            filter_actors_window.destroy()

        accept_btn = tk.Button(
            filter_actors_window,
            text="Применить",
            command=accept,
        )
        accept_btn.pack()

        filter_actors_window.mainloop()
        return self.selected_genre_filter, self.selected_building_filter

    def __actors_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Информация об артистах")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        actors = self.db_manager.select_actors()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Genre",
                "Building name",
                "Name",
                "Surname",
                "Age",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Genre", text="Жанр")
        table.heading("Building name", text="")
        table.heading("Name", text="Имя артиста")
        table.heading("Surname", text="Фамилия артиста")
        table.heading("Age", text="Возраст артиста")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in actors:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        # Фильтрация артистов
        genres = [genre[0] for genre in self.db_manager.select_genres()]
        genres.append("Любой")
        genres = genres[::-1]

        buildings = [building[1] for building in self.db_manager.select_buildings()]
        buildings.append("Любое")
        buildings = buildings[::-1]

        genre_label = tk.Label(self.current_window, text="Жанр:")
        genre_label.pack()
        genre_combobox = ttk.Combobox(
            self.current_window, values=genres, state="readonly"
        )
        genre_combobox.current(0)
        genre_combobox.pack()

        building_label = tk.Label(self.current_window, text="Место работы:")
        building_label.pack()
        building_combobox = ttk.Combobox(
            self.current_window, values=buildings, state="readonly"
        )
        building_combobox.current(0)
        building_combobox.pack()

        def filter_actors():
            genre_filter = genre_combobox.get()
            building_filter = building_combobox.get()
            actors = self.db_manager.select_actors()

            def filter_by_genre(actor):
                if genre_filter == "Любой" or actor[1] == genre_filter:
                    return True
                return False

            def filter_by_building(actor):
                if building_filter == "Любое" or actor[2] == building_filter:
                    return True
                return False

            actors = filter(filter_by_genre, actors)
            actors = filter(filter_by_building, actors)
            # Очистка таблицы перед обновлением
            for row in table.get_children():
                table.delete(row)

            # Вставка отфильтрованных данных в таблицу
            for row in actors:
                table.insert("", "end", values=row[1:])  # Не отображаем id

        accept_btn = tk.Button(
            self.current_window,
            text="Поиск",
            command=filter_actors,
        )
        accept_btn.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __events_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Поиск подходящих событий")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Building name",
                "Event name",
                "Genre name",
                "Impresario name",
                "Impresario surname",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Building name", text="Место проведения")
        table.heading("Event name", text="Название")
        table.heading("Genre name", text="Жанр")
        table.heading("Impresario name", text="Имя импресарио")
        table.heading("Impresario surname", text="Фамилия импресарио")
        table.heading("Creation Date", text="Дата создания записи")

        # Размещение таблицы на окне
        table.pack()

        # Фильтрация событий
        genres = [genre[0] for genre in self.db_manager.select_genres()]
        genres.append("Любой")
        genres = genres[::-1]

        buildings = [building[1] for building in self.db_manager.select_buildings()]
        buildings.append("Любое")
        buildings = buildings[::-1]

        genre_label = tk.Label(self.current_window, text="Жанр:")
        genre_label.pack()
        genre_combobox = ttk.Combobox(
            self.current_window, values=genres, state="readonly"
        )
        genre_combobox.current(0)
        genre_combobox.pack()

        building_label = tk.Label(self.current_window, text="Место проведения:")
        building_label.pack()
        building_combobox = ttk.Combobox(
            self.current_window, values=buildings, state="readonly"
        )
        building_combobox.current(0)
        building_combobox.pack()

        def filter_events():
            building_filter = building_combobox.get()
            genre_filter = genre_combobox.get()

            def filter_by_building(event):
                if building_filter == "Любое" or event[1] == building_filter:
                    return True
                return False

            def filter_by_genre(event):
                if genre_filter == "Любой" or event[3] == genre_filter:
                    return True
                return False

            events = self.db_manager.select_events()
            events = filter(filter_by_genre, events)
            events = filter(filter_by_building, events)
            # Очистка таблицы перед обновлением
            for row in table.get_children():
                table.delete(row)

            # Вставка отфильтрованных данных в таблицу
            for row in events:
                table.insert("", "end", values=row[1:])  # Не отображаем id

        accept_btn = tk.Button(
            self.current_window,
            text="Поиск",
            command=filter_events,
        )
        accept_btn.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __event_stats_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Статистика по событиям")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Event name",
                "Genre name",
                "Impresario full name",
                "Building name",
                "Box office",
                "Average rating",
                "Actor likes",
            ),
        )
        table["show"] = "headings"
        table.heading("Event name", text="Название")
        table.heading("Genre name", text="Жанр")
        table.heading("Impresario full name", text="ФИО импресарио")
        table.heading("Building name", text="Место проведения")
        table.heading("Box office", text="Сборы")
        table.heading("Average rating", text="Средняя оценка")
        table.heading("Actor likes", text="Лайки актеров")

        # Размещение таблицы на окне
        table.pack()

        events = [event[2] for event in self.db_manager.select_events()]
        event_label = tk.Label(self.current_window, text="Выбрать событие:")
        event_label.pack()
        event_combobox = ttk.Combobox(
            self.current_window, values=events, state="readonly"
        )
        event_combobox.pack()

        def show_stats():
            selected_event_id = event_combobox.current() + 1
            # Очистка таблицы перед обновлением
            for row in table.get_children():
                table.delete(row)

            event_stats = self.db_manager.select_event_stats(selected_event_id)
            # Вставка отфильтрованных данных в таблицу
            prepared_data = (
                        event_stats[0][0],
                        event_stats[0][1],
                        event_stats[0][2],
                        event_stats[0][3] + " " + event_stats[0][4],
                        event_stats[0][5],
                        event_stats[0][6],
                        event_stats[0][7],
                        event_stats[0][8],
                    )
            table.insert("", "end", values=prepared_data[1:])  # Не отображаем id

        accept_btn = tk.Button(
            self.current_window,
            text="Показать статистику",
            command=show_stats,
        )
        accept_btn.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __impresarios_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Информация об импресариоИнформация об импресарио")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        impresarios = self.db_manager.select_impresarios()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Building name",
                "Impresario name",
                "Impresario surname",
                "Impresario age",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Building name", text="Название здания")
        table.heading("Impresario name", text="Имя импресарио")
        table.heading("Impresario surname", text="Фамилия импресарио")
        table.heading("Impresario age", text="Возраст импресарио")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in impresarios:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        # Фильтрация импресарио
        buildings = [building[1] for building in self.db_manager.select_buildings()]
        buildings.append("Любое")
        buildings = buildings[::-1]

        building_label = tk.Label(self.current_window, text="Место работы:")
        building_label.pack()
        building_combobox = ttk.Combobox(
            self.current_window, values=buildings, state="readonly"
        )
        building_combobox.current(0)
        building_combobox.pack()

        def filter_impresarios():
            building_filter = building_combobox.get()
            impresarios = self.db_manager.select_impresarios()

            def filter_by_building(impresario):
                if building_filter == "Любое" or impresario[1] == building_filter:
                    return True
                return False

            impresarios = filter(filter_by_building, impresarios)
            # Очистка таблицы перед обновлением
            for row in table.get_children():
                table.delete(row)

            # Вставка отфильтрованных данных в таблицу
            for row in impresarios:
                table.insert("", "end", values=row[1:])  # Не отображаем id

        accept_btn = tk.Button(
            self.current_window,
            text="Поиск",
            command=filter_impresarios,
        )
        accept_btn.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __buildings_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Страница зданий")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        buildings = self.db_manager.select_buildings()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window, columns=("Building name", "Creation Date")
        )
        table["show"] = "headings"
        table.heading("Building name", text="Название здания")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in buildings:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __contests_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Результаты конкурсов")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        events = self.db_manager.select_contests()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "name",
                "first_place",
                "second_place",
                "third_place",
            ),
        )
        table["show"] = "headings"
        table.heading("name", text="Название конкурса")
        table.heading("first_place", text="Первое место")
        table.heading("second_place", text="Второе место")
        table.heading("third_place", text="Третье место")

        # Вставка данных в таблицу
        for row in events:
            first_place = f"{row[1]} {row[2]}"  # Объединяем имя и фамилию первого места
            second_place = (
                f"{row[3]} {row[4]}"  # Объединяем имя и фамилию второго места
            )
            third_place = (
                f"{row[5]} {row[6]}"  # Объединяем имя и фамилию третьего места
            )
            table.insert(
                "", "end", values=[row[0], first_place, second_place, third_place]
            )

        # Размещение таблицы на окне
        table.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __to_main_menu(self):
        if self.current_window:
            self.current_window.destroy()
        return "main_menu"

    def __create_event_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление события")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        # Получаем названия жанров
        genres = [genre[0] for genre in self.db_manager.select_genres()]
        # Получаем id, имена и фамилии импресарио
        impresarios = {
            impresario[0]: impresario[2] + " " + impresario[3]
            for impresario in self.db_manager.select_impresarios()
        }
        buildings = [building[1] for building in self.db_manager.select_buildings()]

        event_name_label = tk.Label(self.current_window, text="Название события:")
        event_name_label.pack()
        event_name_entry = tk.Entry(self.current_window)
        event_name_entry.pack()

        genre_label = tk.Label(self.current_window, text="Выберите жанр:")
        genre_label.pack()
        genre_combobox = ttk.Combobox(
            self.current_window, values=genres, state="readonly"
        )
        genre_combobox.pack()

        impresario_label = tk.Label(self.current_window, text="Выберите импресарио:")
        impresario_label.pack()
        impresario_combobox = ttk.Combobox(
            self.current_window, values=list(impresarios.values()), state="readonly"
        )
        impresario_combobox.pack()

        building_label = tk.Label(self.current_window, text="Выберите здание:")
        building_label.pack()
        building_combobox = ttk.Combobox(
            self.current_window, values=buildings, state="readonly"
        )
        building_combobox.pack()

        event_date_label = tk.Label(self.current_window, text="Дата события:")
        event_date_label.pack()
        event_date_entry = tk.Entry(self.current_window)
        event_date_entry.pack()

        box_office_label = tk.Label(self.current_window, text="Сборы:")
        box_office_label.pack()
        box_office_entry = tk.Entry(self.current_window)
        box_office_entry.pack()

        def submit():
            event_name = event_name_entry.get()
            genre_name = genre_combobox.get()
            building_id = building_combobox.current() + 1
            event_date = event_date_entry.get()
            # TODO: добавить ошибку, если не получается преобразовать в int.
            box_office = int(box_office_entry.get())

            # Получаем id импресарио по выбранному ФИО
            selected_full_name = impresario_combobox.get()
            if not event_name or not genre_name or not selected_full_name:
                self.error_modal("Заполните все поля!")
                return
            impresario_id = [
                key for key, value in impresarios.items() if value == selected_full_name
            ][0]

            self.db_manager.create_event(
                event_name,
                genre_name,
                impresario_id,
                building_id,
                event_date,
                box_office,
            )
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def error_modal(self, error_message="Неизвестная ошибка"):
        error_window = tk.Toplevel(self.current_window)
        error_window.title("Ошибка!")

        error_message_label = tk.Label(error_window, text=error_message)
        error_message_label.pack()

        ok_btn = tk.Button(
            error_window,
            text="Ок",
            command=error_window.destroy,
        )
        ok_btn.pack()

        error_window.mainloop()

    def __create_user_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление пользователя")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        username_label = tk.Label(self.current_window, text="Логин пользователя:")
        username_label.pack()
        username_entry = tk.Entry(self.current_window)
        username_entry.pack()

        password_label = tk.Label(self.current_window, text="Пароль пользователя:")
        password_label = tk.Label(self.current_window, text="Пароль пользователя:")
        password_label.pack()
        password_entry = tk.Entry(self.current_window, show="*")
        password_entry.pack()

        verify_password_label = tk.Label(
            self.current_window, text="Введите пароль еще раз:"
        )
        verify_password_label.pack()
        verify_password_entry = tk.Entry(self.current_window, show="*")
        verify_password_entry.pack()

        roles = ["viewer_role", "event_manager_role", "impresario_role"]
        role_label = tk.Label(self.current_window, text="Роль пользователя:")
        role_label.pack()
        role_combobox = ttk.Combobox(
            self.current_window, values=roles, state="readonly"
        )
        role_combobox.pack()

        def submit():
            username = username_entry.get()
            password = password_entry.get()
            verify_password = verify_password_entry.get()
            role = role_combobox.get()

            if password != verify_password:
                self.error_modal("Пароли не совпадают.")
                return

            self.db_manager.create_user(username, password, role)
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Создать", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __create_contest_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление конкурса")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        # Получаем названия жанров
        actors = {
            actor[0]: actor[3] + " " + actor[4]
            for actor in self.db_manager.select_actors()
        }

        event_name_label = tk.Label(self.current_window, text="Название конкурса:")
        event_name_label.pack()
        event_name_entry = tk.Entry(self.current_window)
        event_name_entry.pack()

        first_place_label = tk.Label(self.current_window, text="Первое место:")
        first_place_label.pack()
        first_place_combobox = ttk.Combobox(
            self.current_window, values=list(actors.values()), state="readonly"
        )
        first_place_combobox.pack()

        second_place_label = tk.Label(self.current_window, text="Второе место:")
        second_place_label.pack()
        second_place_combobox = ttk.Combobox(
            self.current_window, values=list(actors.values()), state="readonly"
        )
        second_place_combobox.pack()

        third_place_label = tk.Label(self.current_window, text="Третье место:")
        third_place_label.pack()
        third_place_combobox = ttk.Combobox(
            self.current_window, values=list(actors.values()), state="readonly"
        )
        third_place_combobox.pack()

        def submit():
            event_name = event_name_entry.get()
            first_place_full_name = first_place_combobox.get()
            second_place_full_name = second_place_combobox.get()
            third_place_full_name = third_place_combobox.get()

            if (
                not event_name
                or not first_place_full_name
                or not second_place_full_name
                or not third_place_full_name
            ):
                self.error_modal("Заполните все поля!")
                return
            first_place_id = [
                key for key, value in actors.items() if value == first_place_full_name
            ][0]

            second_place_id = [
                key for key, value in actors.items() if value == second_place_full_name
            ][0]

            third_place_id = [
                key for key, value in actors.items() if value == third_place_full_name
            ][0]

            if len(set([first_place_id, second_place_id, third_place_id])) != 3:
                self.error_modal(
                    "Один участник не может занимать несколько мест одновременно!"
                )
                return

            self.db_manager.create_contest(
                event_name, first_place_id, second_place_id, third_place_id
            )
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __create_building_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление культурного сооружения")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        building_types = ["Театр", "Кинотеатр", "Дворец культуры"]

        building_name_label = tk.Label(self.current_window, text="Название здания:")
        building_name_label.pack()
        building_name_entry = tk.Entry(self.current_window)
        building_name_entry.pack()

        building_type_label = tk.Label(self.current_window, text="Тип здания:")
        building_type_label.pack()
        building_type_combobox = ttk.Combobox(
            self.current_window, values=building_types, state="readonly"
        )
        building_type_combobox.pack()

        def submit():
            building_name = building_name_entry.get()
            building_type = building_type_combobox.get()

            self.db_manager.create_building(building_name, building_type)
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __create_actor_event_link_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление артиста в событие")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        actors = [
            actor[3] + " " + actor[4] for actor in self.db_manager.select_actors()
        ]
        events = [event[2] for event in self.db_manager.select_events()]

        actor_label = tk.Label(self.current_window, text="Артист:")
        actor_label.pack()
        actor_combobox = ttk.Combobox(
            self.current_window, values=actors, state="readonly"
        )
        actor_combobox.pack()

        event_label = tk.Label(self.current_window, text="Событие:")
        event_label.pack()
        event_combobox = ttk.Combobox(
            self.current_window, values=events, state="readonly"
        )
        event_combobox.pack()

        def submit():
            actor_id = actor_combobox.current() + 1
            event_id = event_combobox.current() + 1
            self.db_manager.add_actor_event_link(actor_id, event_id)
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __rate_event_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Оценка культурного события")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        events = [event[2] for event in self.db_manager.select_events()]
        ratings = [1, 2, 3, 4, 5]

        event_label = tk.Label(self.current_window, text="Культурное событие:")
        event_label.pack()
        event_combobox = ttk.Combobox(
            self.current_window, values=events, state="readonly"
        )
        event_combobox.pack()

        rating_label = tk.Label(self.current_window, text="Оценка:")
        rating_label.pack()
        impresario_combobox = ttk.Combobox(
            self.current_window, values=ratings, state="readonly"
        )
        impresario_combobox.pack()

        def submit():
            event_id = event_combobox.current() + 1
            rating = impresario_combobox.get()

            self.db_manager.rate_event(event_id, self.username, rating)
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __favorite_actors_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Любимые артисты")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        favorite_actors = self.db_manager.select_my_favorite_actors(self.username)
        actors = [
            (actor[0], actor[3], actor[4])
            for actor in self.db_manager.select_actors()  # id, name, surname
        ]
        unpicked_actors = [actor for actor in actors if actor not in favorite_actors]
        combobox_actors = {
            actor[0]: actor[1] + " " + actor[2] for actor in unpicked_actors
        }

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Name",
                "Surname",
            ),
        )
        table["show"] = "headings"
        table.heading("Name", text="Имя артиста")
        table.heading("Surname", text="Фамилия артиста")

        # Вставка данных в таблицу
        for row in favorite_actors:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        actor_label = tk.Label(self.current_window, text="Добавить любимого артиста:")
        actor_label.pack()
        actor_combobox = ttk.Combobox(
            self.current_window, values=list(combobox_actors.values()), state="readonly"
        )
        actor_combobox.pack()

        def submit():
            # Получаем id импресарио по выбранному ФИО
            selected_full_name = actor_combobox.get()
            actor_id = [
                key
                for key, value in combobox_actors.items()
                if value == selected_full_name
            ][0]

            self.db_manager.add_favorite_actor(self.username, actor_id)

            # Очистка таблицы перед обновлением
            for row in table.get_children():
                table.delete(row)

            favorite_actors = self.db_manager.select_my_favorite_actors(self.username)

            # Вставка отфильтрованных данных в таблицу
            for row in favorite_actors:
                table.insert("", "end", values=row[1:])  # Не отображаем id

        accept_btn = tk.Button(self.current_window, text="Добавить", command=submit)
        accept_btn.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
            fg="red",
            bg="yellow",
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __main_menu(self, role):
        self.current_window = tk.Tk()
        self.current_window.title("Главное меню")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        self.next_window_name = "exit"

        header_text = None
        match role:
            case "admin_role":
                header_text = "Меню для администратора БД"
            case "viewer_role":
                header_text = "Меню для зрителя"
            case "event_manager_role":
                header_text = "Меню для менеджера событий"
            case "impresario_role":
                header_text = "Меню для импресарио"

        header_label = tk.Label(self.current_window, text=header_text)
        header_label.pack()

        # Общие для всех (кроме админа) кнопки:
        if role != "admin_role":
            actors_page_btn = tk.Button(
                self.current_window,
                text="Информация об артистах",
                command=lambda: self.__set_next_window("actors_page"),
            )
            events_page_btn = tk.Button(
                self.current_window,
                text="Поиск подходящих событий",
                command=lambda: self.__set_next_window("events_page"),
            )
            impresarios_page_btn = tk.Button(
                self.current_window,
                text="Информация об импресарио",
                command=lambda: self.__set_next_window("impresarios_page"),
            )
            buildings_page_btn = tk.Button(
                self.current_window,
                text="Страница зданий",
                command=lambda: self.__set_next_window("buildings_page"),
            )
            contests_page_btn = tk.Button(
                self.current_window,
                text="Результаты конкурсов",
                command=lambda: self.__set_next_window("contests_page"),
            )
            actors_page_btn.pack()
            events_page_btn.pack()
            impresarios_page_btn.pack()
            buildings_page_btn.pack()
            contests_page_btn.pack()

        match role:
            case "admin_role":
                create_user_btn = tk.Button(
                    self.current_window,
                    text="Создание пользователя",
                    command=lambda: self.__set_next_window("create_user"),
                )
                create_user_btn.pack()
            case "viewer_role":
                rate_event_btn = tk.Button(
                    self.current_window,
                    text="Оценка культурного события",
                    command=lambda: self.__set_next_window("rate_event"),
                )
                rate_event_btn.pack()
                favorite_actors_btn = tk.Button(
                    self.current_window,
                    text="Любимые артисты",
                    command=lambda: self.__set_next_window("favorite_actors_page"),
                )
                favorite_actors_btn.pack()
            case "event_manager_role":
                create_event_btn = tk.Button(
                    self.current_window,
                    text="Создать событие",
                    command=lambda: self.__set_next_window("create_event"),
                )
                create_event_btn.pack()

                create_building_btn = tk.Button(
                    self.current_window,
                    text="Создать здание",
                    command=lambda: self.__set_next_window("create_building"),
                )
                create_building_btn.pack()

                create_actor_event_link_btn = tk.Button(
                    self.current_window,
                    text="Добавить артиста в событие",
                    command=lambda: self.__set_next_window("create_actor_event_link"),
                )
                create_actor_event_link_btn.pack()

                event_stats_btn = tk.Button(
                    self.current_window,
                    text="Статистика по событиям",
                    command=lambda: self.__set_next_window("event_stats_page"),
                )
                event_stats_btn.pack()
            case "impresario_role":
                create_event_btn = tk.Button(
                    self.current_window,
                    text="Создать событие",
                    command=lambda: self.__set_next_window("create_event"),
                )
                create_contest_btn = tk.Button(
                    self.current_window,
                    text="Создать конкурс",
                    command=lambda: self.__set_next_window("create_contest"),
                )
                create_event_btn.pack()
                create_contest_btn.pack()
        exit_btn = tk.Button(
            self.current_window,
            text="Выйти из аккаунта",
            command=lambda: self.__set_next_window("change_user"),
        )
        exit_btn.pack()

        self.current_window.mainloop()
        return self.next_window_name

    def handle_command(self, command, role):
        next_window = "exit"
        match command:
            case "main_menu":
                next_window = self.__main_menu(role)
            case "actors_page":
                next_window = self.__actors_page()
            case "events_page":
                next_window = self.__events_page()
            case "impresarios_page":
                next_window = self.__impresarios_page()
            case "buildings_page":
                next_window = self.__buildings_page()
            case "create_event":
                next_window = self.__create_event_page()
            case "create_user":
                next_window = self.__create_user_page()
            case "create_contest":
                next_window = self.__create_contest_page()
            case "create_building":
                next_window = self.__create_building_page()
            case "create_actor_event_link":
                next_window = self.__create_actor_event_link_page()
            case "contests_page":
                next_window = self.__contests_page()
            case "rate_event":
                next_window = self.__rate_event_page()
            case "favorite_actors_page":
                next_window = self.__favorite_actors_page()
            case "event_stats_page":
                next_window = self.__event_stats_page()
        return next_window
