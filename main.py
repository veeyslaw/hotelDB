import sys
import datetime
import cx_Oracle
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5 import QtCore
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    WELCOME_PAGE = 0
    BOOK_PAGE = 1
    OFFERS_PAGE = 2
    CHECK_OUT_PAGE = 3
    SUCCESSFUL_PAGE = 4
    ADMIN_PAGE = 5
    CITY_PAGE = 0
    HOTEL_PAGE = 1
    APARTMENT_PAGE = 2
    BOOKING_PAGE = 3
    GUEST_PAGE = 4
    CURRENT_ITEM_BASE_LABEL = 'Managing: '
    CURRENT_ITEM_BASE_LABEL_LEN = len(CURRENT_ITEM_BASE_LABEL)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("Front/form.ui", self)

        self.error_dialog = QDialog(self)
        self.add_dialog = QDialog(self)
        self.update_delete_dialog = QDialog(self)
        self.configure_dialogs()
        self.connect_ui()
        self.reset_book_cache()

        self.db_connection = cx_Oracle.connect('tema', 'vlad', 'localhost/xe')

    def connect_ui(self):
        self.book_button.clicked.connect(self.go_to_fresh_book_page)
        self.admin_button.clicked.connect(self.go_to_admin_page)
        self.search_button.clicked.connect(self.search_bookings)
        self.back_button_2.clicked.connect(self.go_to_book_page)
        self.back_button.clicked.connect(self.go_to_book_page)
        self.confirm_button.clicked.connect(self.confirm_booking)
        self.another_booking_button.clicked.connect(self.go_to_fresh_book_page)
        self.quit_button.clicked.connect(self.close)
        self.quit_admin_button.clicked.connect(self.close)
        self.search_button_2.clicked.connect(self.search_admin)
        self.search_combo_box.currentIndexChanged.connect(self.on_search_combo_box_change)
        self.check_in_date_edit.dateChanged.connect(self.on_check_in_date_change)
        self.offers_list.itemClicked.connect(self.book)
        self.search_list.itemDoubleClicked.connect(self.administer_item)
        self.add_dialog.add_button.clicked.connect(self.add_entry)
        self.update_delete_dialog.update_button.clicked.connect(self.update_entry)
        self.update_delete_dialog.delete_button.clicked.connect(self.delete_entry)
        self.update_delete_dialog.city_name_line_edit.textChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.hotel_name_line_edit.textChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.hotel_name_line_edit_2.textChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.apart_number_spin_box.valueChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.hotel_name_line_edit_5.textChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.apart_number_spin_box_3.valueChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.check_in_date_edit.dateChanged.connect(self.disable_dialog_delete_button)
        self.update_delete_dialog.passport_number_line_edit.textChanged.connect(self.disable_dialog_delete_button)

    def configure_error_dialog(self):
        self.error_dialog.resize(300, 300)
        self.error_dialog.setWindowTitle('Error')
        vertical_layout = QVBoxLayout(self.error_dialog)

        self.error_label = QLabel(self.error_dialog)
        self.error_label.setObjectName('error_label')
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        vertical_layout.addWidget(self.error_label)

        button_box = QDialogButtonBox(self.error_dialog)
        button_box.setStandardButtons(QDialogButtonBox.Ok)
        button_box.setObjectName('button_box')
        button_box.accepted.connect(self.error_dialog.accept)
        vertical_layout.addWidget(button_box)

    def configure_dialogs(self):
        self.configure_error_dialog()
        loadUi("Front/add_dialog_form.ui", self.add_dialog)
        loadUi("Front/update_delete_dialog_form.ui", self.update_delete_dialog)

    def reset_book_cache(self):
        self.check_in = '2000-01-01'
        self.check_out = '2000-01-01'
        self.adults_count = -1
        self.children_count = -1
        self.hotel_name = ''
        self.apartment_number = -1

    def disable_dialog_delete_button(self):
        self.update_delete_dialog.delete_button.setEnabled(False)

    def error(self, message):
        self.error_label.setText(message)
        self.error_dialog.exec()

    def prepare_city_options(self):
        self.city_combo_box.clear()
        self.city_combo_box.addItem('Any city')
        with self.db_connection.cursor() as cursor:
            cursor.execute('SELECT city_name FROM CITY')
            for row in cursor:
                self.city_combo_box.addItem(row[0])

    def prepare_date_edits(self):
        with self.db_connection.cursor() as cursor:
            sysdate = cursor.execute('SELECT SYSDATE FROM DUAL').fetchone()[0].date()
        self.check_in_date_edit.setMinimumDate(sysdate)
        self.check_in_date_edit.setMaximumDate(sysdate + datetime.timedelta(days=366))
        self.check_out_date_edit.setMinimumDate(sysdate + datetime.timedelta(days=1))
        self.check_out_date_edit.setMaximumDate(sysdate + datetime.timedelta(days=367))

    def reset_options(self):
        self.rooms_combo_box.setCurrentIndex(0)
        self.adults_spin_box.setValue(1)
        self.children_spin_box.setValue(0)
        self.rating_combo_box.setCurrentIndex(0)
        self.restaurant_check_box.setChecked(False)
        self.free_meals_check_box.setChecked(False)
        self.minibar_check_box.setChecked(False)
        self.pool_check_box.setChecked(False)
        self.free_internet_check_box.setChecked(False)
        self.tv_check_box.setChecked(False)
        self.ac_check_box.setChecked(False)
        self.double_bed_check_box.setChecked(False)

    def on_check_in_date_change(self, date):
        self.check_out_date_edit.setMinimumDate(date.addDays(1))

    def go_to_fresh_book_page(self):
        self.prepare_city_options()
        self.prepare_date_edits()
        self.reset_options()
        self.reset_book_cache()
        self.main_stacked_widget.setCurrentIndex(MainWindow.BOOK_PAGE)

    def go_to_book_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.BOOK_PAGE)

    def go_to_admin_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.ADMIN_PAGE)

    def search_bookings(self):
        if self.city_combo_box.currentIndex() == 0:
            city = None
        else:
            city = str(self.city_combo_box.currentText())
        self.check_in = str(self.check_in_date_edit.date().toPyDate())
        self.check_out = str(self.check_out_date_edit.date().toPyDate())
        try:
            room_count = int(self.rooms_combo_box.currentText())
        except ValueError:
            room_count = None
        self.adults_count = self.adults_spin_box.value()
        self.children_count = self.children_spin_box.value()
        try:
            rating = int(self.rating_combo_box.currentText())
        except ValueError:
            rating = None
        restaurant = int(self.restaurant_check_box.isChecked())
        free_meals = int(self.free_meals_check_box.isChecked())
        minibar = int(self.minibar_check_box.isChecked())
        pool = int(self.pool_check_box.isChecked())
        free_internet = int(self.free_internet_check_box.isChecked())
        tv = int(self.tv_check_box.isChecked())
        ac = int(self.ac_check_box.isChecked())
        double_bed = int(self.double_bed_check_box.isChecked())

        query = f"""
                SELECT
                    city_name,
                    hotel_name,
                    text_desc, rating, restaurant, free_meals, pool, free_internet,
                    apart_number, room_count, price_per_night_euro,
                    air_conditioner, minibar, tv, double_bed
                FROM
                    CITY c,
                    HOTEL h,
                    HOTEL_DESCRIPTION hd,
                    (SELECT *
                     FROM APARTMENT inner_a
                     WHERE (SELECT COUNT(*)
                            FROM BOOKING b
                            WHERE b.apart_id = inner_a.apart_id
                                AND b.check_out > TO_DATE('{self.check_in}', 'YYYY-MM-DD')
                                AND b.check_in < TO_DATE('{self.check_out}', 'YYYY-MM-DD')) = 0)
                    a,
                    APARTMENT_DESCRIPTION ad
                WHERE
                    c.city_id = h.city_id
                    AND h.hotel_id = hd.hotel_id
                    AND a.hotel_id = h.hotel_id
                    AND ad.apart_id = a.apart_id
                    AND restaurant >= {restaurant}
                    AND free_meals >= {free_meals}
                    AND pool >= {pool}
                    AND free_internet >= {free_internet}
                    AND air_conditioner >= {ac}
                    AND minibar >= {minibar}
                    AND tv >= {tv}
                    AND double_bed >= {double_bed}
                    AND apart_capacity >= {self.adults_count + self.children_count}
                    {f"AND city_name = '{city}'" if city is not None else ''}
                    {f'AND rating >= {rating}' if rating is not None else ''}
                    {f'AND room_count >= {room_count}' if room_count is not None else ''}
                """

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            offers = [row for row in cursor]
        if offers is None:
            self.error('No available offers. Try a broader search.')
        else:
            self.go_to_offers_page(offers)

    def add_offer(self, offer):
        hotel_comodities = offer[4] + offer[5] + offer[6] + offer[7]
        apartment_comodities = offer[11] + offer[12] + offer[13] + offer[14]
        item = f"{''.ljust(len(offer[2]), '-')}\n" +\
            f"{offer[1]}, {offer[0]}{f', {offer[3]} stars' if offer[3] is not None else ''}\n" +\
            f"{offer[2]}" +\
            f"{f'{chr(10)}' if hotel_comodities > 0 else ''}" +\
            f"{f'Hotel restaurant {chr(10003)} ' if offer[4] == 1 else ''}" +\
            f"{f'Free meals {chr(10003)} ' if offer[5] == 1 else ''}" +\
            f"{f'Private pool {chr(10003)} ' if offer[6] == 1 else ''}" +\
            f"{f'Free internet {chr(10003)} ' if offer[7] == 1 else ''}" +\
            f"{f'{chr(10)}' if apartment_comodities > 0 else ''}" +\
            f"{f'AC {chr(10003)} ' if offer[11] == 1 else ''}" +\
            f"{f'Minibar {chr(10003)} ' if offer[12] == 1 else ''}" +\
            f"{f'TV {chr(10003)} ' if offer[13] == 1 else ''}" +\
            f"{f'Double bed {chr(10003)} ' if offer[14] == 1 else ''}" +\
            f"\nNo. {offer[8]}, {offer[9]} rooms ----- only {offer[10]} {chr(8364)} per night" +\
            f"\n{''.ljust(len(offer[2]), '_')}"

        self.offers_list.addItem(item)

    def go_to_offers_page(self, offers):
        self.period_label.setText(f'Offers for {self.check_in} - {self.check_out}')
        self.offers_list.clear()

        for offer in offers:
            self.add_offer(offer)

        self.main_stacked_widget.setCurrentIndex(MainWindow.OFFERS_PAGE)

    def book(self, item):
        text = item.text()

        hotel_name_start = text.find('\n') + 1
        hotel_name_stop = text.find(',', hotel_name_start)
        self.hotel_name = text[hotel_name_start: hotel_name_stop]

        apartment_number_start = text.rfind('No.') + 4
        apartment_number_stop = text.find(',', apartment_number_start)
        self.apartment_number = int(text[apartment_number_start: apartment_number_stop])

        self.first_name_line_edit.clear()
        self.last_name_line_edit.clear()
        self.passport_line_edit.clear()
        self.email_line_edit.clear()
        self.phone_number_line_edit.clear()
        self.main_stacked_widget.setCurrentIndex(MainWindow.CHECK_OUT_PAGE)

    def confirm_booking(self):
        first_name = str(self.first_name_line_edit.text())
        last_name = str(self.last_name_line_edit.text())
        passport_number = str(self.passport_line_edit.text())
        email = str(self.email_line_edit.text())
        phone_number = str(self.phone_number_line_edit.text())
        phone_number_text = f", '{phone_number}'" if len(phone_number) > 0 else ''

        with self.db_connection.cursor() as cursor:
            cursor.execute(f"SELECT first_name, last_name, email, phone_number FROM GUEST WHERE passport_number = '{passport_number}'")
            guest_data = [row for row in cursor]

        if len(guest_data) == 0:
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO GUEST (first_name, last_name, passport_number, email{', phone_number' if len(phone_number) > 0 else ''}) " +\
                                f"VALUES ('{first_name}', '{last_name}', '{passport_number}', '{email}'{phone_number_text})")
        else:
            if (first_name, last_name, email, phone_number) != guest_data:
                self.error('You have another active booking, but the details provided are different. Please verify again or contact us.')
                return

        with self.db_connection.cursor() as cursor:
            sysdate = str(cursor.execute('SELECT SYSDATE FROM DUAL').fetchone()[0].date())

        with self.db_connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO BOOKING (guest_id, apart_id, book_date, check_in, check_out, adults_count, children_count)
                            VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = '{passport_number}'),
                                    (SELECT apart_id FROM APARTMENT
                                     WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{self.hotel_name}')
                                         AND apart_number = {self.apartment_number}),
                                    TO_DATE('{sysdate}', 'YYYY-MM-DD'),
                                    TO_DATE('{self.check_in}', 'YYYY-MM-DD'),
                                    TO_DATE('{self.check_out}', 'YYYY-MM-DD'),
                                    {self.adults_count},
                                    {self.children_count}
                            )""")

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute('COMMIT')
        except Exception as e:
            print(type(e))
            print(e)
            self.error('Could not confirm booking. Try again later.')

        self.main_stacked_widget.setCurrentIndex(MainWindow.SUCCESSFUL_PAGE)

    def on_search_combo_box_change(self, index):
        self.search_list.clear()
        self.search_stacked_widget.setCurrentIndex(index)

    def get_add_item_city(self):
        city_name = str(self.city_name_line_edit.text())

        if city_name == '':
            return None
        else:
            item = f"""Add city:
            Name: {city_name}
            """
            return item

    def get_add_item_hotel(self):
        hotel_name = str(self.hotel_name_line_edit.text())
        city_name = str(self.city_name_line_edit_2.text())
        if (city_name, hotel_name) == ('', ''):
            return None
        else:
            item = "Add hotel:\n" +\
                (f'  Name: {hotel_name}{chr(10)}' if hotel_name != '' else '') +\
                (f'  City: {city_name}{chr(10)}' if city_name != '' else '')
            return item

    def get_add_item_apartment(self):
        hotel_name = str(self.hotel_name_line_edit_2.text())
        apartment_number = self.apartment_number_spin_box.value()

        if (hotel_name, apartment_number) == ('', 0):
            return None
        else:
            item = "Add apartment:\n" +\
                (f'  Hotel: {hotel_name}{chr(10)}' if hotel_name != '' else '') +\
                (f'  Number: {apartment_number}{chr(10)}' if apartment_number != 0 else '')
            return item

    def search_city(self):
        city_name = str(self.city_name_line_edit.text())

        with self.db_connection.cursor() as cursor:
            cursor.execute(f"SELECT city_name FROM CITY WHERE LOWER(city_name) LIKE LOWER('%{city_name}%')")
            items = [row[0] for row in cursor]

        return items

    def search_hotel(self):
        hotel_name = str(self.hotel_name_line_edit.text())
        city_name = str(self.city_name_line_edit_2.text())

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT hotel_name, city_name, contact_number, manager_name, " +\
                                    "text_desc, rating, restaurant, free_meals, pool, free_internet " +\
                            "FROM HOTEL h, CITY c, HOTEL_DESCRIPTION hd " +\
                            f"WHERE LOWER(hotel_name) LIKE LOWER('%{hotel_name}%') " +\
                            f"AND LOWER(city_name) LIKE LOWER('%{city_name}%') " +\
                            "AND h.city_id = c.city_id " +\
                            "AND hd.hotel_id = h.hotel_id")
            items = [f'{row[0]}\n{row[1]}\nContact: {row[2].strip()}{f"{chr(10)}Manager: {row[3]}" if row[3] is not None else ""}\n' +\
                    f'{row[4]}{f"{chr(10)}Rating: {row[5]}" if row[5] is not None else ""}\n' +\
                    f"{f'Hotel restaurant {chr(10003)} ' if row[6] == 1 else ''}" +\
                    f"{f'Free meals {chr(10003)} ' if row[7] == 1 else ''}" +\
                    f"{f'Private pool {chr(10003)} ' if row[8] == 1 else ''}" +\
                    f"{f'Free internet {chr(10003)} ' if row[9] == 1 else ''}"
                    for row in cursor]

        return items

    def search_apartment(self):
        hotel_name = str(self.hotel_name_line_edit_2.text())
        apartment_number = self.apartment_number_spin_box.value()

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT hotel_name, apart_number, room_count, apart_capacity, price_per_night_euro, " +\
                                    "air_conditioner, minibar, tv, double_bed " +\
                            "FROM HOTEL h, APARTMENT a, APARTMENT_DESCRIPTION ad " +\
                            f"WHERE LOWER(hotel_name) LIKE LOWER('%{hotel_name}%') " +\
                            f"{f'AND apart_number = {apartment_number} ' if apartment_number > 0 else ''}" +\
                            "AND h.hotel_id = a.hotel_id " +\
                            "AND ad.apart_id = a.apart_id")
            items = [f'{row[0]}, Apart. No.{row[1]}\n{row[2]} rooms, capacity - {row[3]}, {row[4]} {chr(8364)} per night\n' +\
                    f"{f'AC {chr(10003)} ' if row[5] == 1 else ''}" +\
                    f"{f'Minibar {chr(10003)} ' if row[6] == 1 else ''}" +\
                    f"{f'TV {chr(10003)} ' if row[7] == 1 else ''}" +\
                    f"{f'Double bed {chr(10003)} ' if row[8] == 1 else ''}"
                    for row in cursor]

        return items

    def search_booking(self):
        hotel_name = str(self.hotel_name_line_edit_3.text())
        apartment_number = self.apartment_number_spin_box_2.value()
        passport_number = str(self.passport_line_edit_2.text())
        check_in = str(self.check_in_date_edit_2.date().toPyDate())
        check_in_line = f"AND check_in LIKE TO_DATE('{check_in}', 'YYYY-MM-DD') " if check_in != "2000-01-01" else ''

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT passport_number, hotel_name, apart_number, book_date, " +\
                                    "check_in, check_out, adults_count, children_count " +\
                            "FROM BOOKING b, GUEST g, APARTMENT a, HOTEL h " +\
                            f"WHERE LOWER(hotel_name) LIKE LOWER('%{hotel_name}%') " +\
                            f"{f'AND apart_number = {apartment_number} ' if apartment_number > 0 else ''}" +\
                            f"AND LOWER(passport_number) LIKE LOWER('%{passport_number}%') " +\
                            check_in_line +\
                            "AND b.apart_id = a.apart_id " +\
                            "AND h.hotel_id = a.hotel_id " +\
                            "AND b.guest_id = g.guest_id ")
            items = [f'{row[1]}, Apart. No.{row[2]}, Guest passport number: {row[0]}\n' +\
                    f'Booked on: {str(row[3].date())}, Check-in: {str(row[4].date())}, Check-out: {str(row[5].date())}\n' +\
                    f'{row[6]} adults, {row[7]} children'
                    for row in cursor]

        return items

    def search_guest(self):
        first_name = str(self.first_name_line_edit_2.text())
        last_name = str(self.last_name_line_edit_2.text())
        passport_number = str(self.passport_line_edit_3.text())
        email = str(self.email_line_edit_2.text())

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT first_name, last_name, passport_number, email, phone_number " +\
                            "FROM GUEST " +\
                            f"WHERE LOWER(first_name) LIKE LOWER('%{first_name}%') " +\
                            f"AND LOWER(last_name) LIKE LOWER('%{last_name}%') " +\
                            f"AND LOWER(passport_number) LIKE LOWER('%{passport_number}%') " +\
                            f"AND LOWER(email) LIKE LOWER('%{email}%')")
            items = [f'First name: {row[0]}\nLast name: {row[1]}\nPassport: {row[2]}\nEmail: {row[3]}' +\
                    f'{f"{chr(10)}Phone number: {row[4].strip()}" if row[4] is not None else ""}'
                    for row in cursor]

        return items

    def clear_search_pages(self):
        self.city_name_line_edit.clear()
        self.hotel_name_line_edit.clear()
        self.city_name_line_edit_2.clear()
        self.hotel_name_line_edit_2.clear()
        self.apartment_number_spin_box.setValue(0)
        self.hotel_name_line_edit_3.clear()
        self.apartment_number_spin_box_2.setValue(0)
        self.passport_line_edit_2.clear()
        self.check_in_date_edit_2.setDate(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
        self.first_name_line_edit_2.clear()
        self.last_name_line_edit_2.clear()
        self.passport_line_edit_3.clear()
        self.email_line_edit_2.clear()

    def search_admin(self):
        index = self.search_combo_box.currentIndex()

        if index == MainWindow.CITY_PAGE:
            item = self.get_add_item_city()
            items = [item] if item is not None else []
        elif index == MainWindow.HOTEL_PAGE:
            item = self.get_add_item_hotel()
            items = [item] if item is not None else []
        elif index == MainWindow.APARTMENT_PAGE:
            item = self.get_add_item_apartment()
            items = [item] if item is not None else []
        elif index == MainWindow.BOOKING_PAGE\
            or index == MainWindow.GUEST_PAGE:
            items = []

        if index == MainWindow.CITY_PAGE:
            items += self.search_city()
        elif index == MainWindow.HOTEL_PAGE:
            items += self.search_hotel()
        elif index == MainWindow.APARTMENT_PAGE:
            items += self.search_apartment()
        elif index == MainWindow.BOOKING_PAGE:
            items += self.search_booking()
        elif index == MainWindow.GUEST_PAGE:
            items += self.search_guest()

        self.search_list.clear()
        for item in items:
            self.search_list.addItem(item)

        self.clear_search_pages()

    def clear_add_dialog(self):
        self.add_dialog.city_name_line_edit.clear()
        self.add_dialog.hotel_name_line_edit.clear()
        self.add_dialog.city_name_line_edit_2.clear()
        self.add_dialog.contact_number_line_edit.clear()
        self.add_dialog.manager_name_line_edit.clear()
        self.add_dialog.text_desc_text_edit.clear()
        self.add_dialog.rating_combo_box.setCurrentIndex(0)
        self.add_dialog.restaurant_check_box.setChecked(False)
        self.add_dialog.free_meals_check_box.setChecked(False)
        self.add_dialog.pool_check_box.setChecked(False)
        self.add_dialog.free_internet_check_box.setChecked(False)
        self.add_dialog.hotel_name_line_edit_2.clear()
        self.add_dialog.apart_number_spin_box.setValue(1)
        self.add_dialog.room_count_spin_box.setValue(1)
        self.add_dialog.apart_capacity_spin_box.setValue(1)
        self.add_dialog.price_per_night_spin_box.setValue(0)
        self.add_dialog.ac_check_box.setChecked(False)
        self.add_dialog.minibar_check_box.setChecked(False)
        self.add_dialog.tv_check_box.setChecked(False)
        self.add_dialog.double_bed_check_box.setChecked(False)

    def clear_update_delete_dialog(self):
        self.update_delete_dialog.current_item_label.setText(MainWindow.CURRENT_ITEM_BASE_LABEL)
        self.update_delete_dialog.city_name_line_edit.clear()
        self.update_delete_dialog.hotel_name_line_edit.clear()
        self.update_delete_dialog.city_name_line_edit_2.clear()
        self.update_delete_dialog.contact_number_line_edit.clear()
        self.update_delete_dialog.manager_name_line_edit.clear()
        self.update_delete_dialog.text_desc_text_edit.clear()
        self.update_delete_dialog.rating_combo_box.setCurrentIndex(0)
        self.update_delete_dialog.restaurant_check_box.setChecked(False)
        self.update_delete_dialog.free_meals_check_box.setChecked(False)
        self.update_delete_dialog.pool_check_box.setChecked(False)
        self.update_delete_dialog.free_internet_check_box.setChecked(False)
        self.update_delete_dialog.hotel_name_line_edit_2.clear()
        self.update_delete_dialog.apart_number_spin_box.setValue(1)
        self.update_delete_dialog.room_count_spin_box.setValue(1)
        self.update_delete_dialog.apart_capacity_spin_box.setValue(1)
        self.update_delete_dialog.price_per_night_spin_box.setValue(0)
        self.update_delete_dialog.ac_check_box.setChecked(False)
        self.update_delete_dialog.minibar_check_box.setChecked(False)
        self.update_delete_dialog.tv_check_box.setChecked(False)
        self.update_delete_dialog.double_bed_check_box.setChecked(False)
        self.update_delete_dialog.passport_number_line_edit_3.clear()
        self.update_delete_dialog.hotel_name_line_edit_5.clear()
        self.update_delete_dialog.apart_number_spin_box_3.setValue(1)
        self.update_delete_dialog.check_in_date_edit.setMinimumDate(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
        self.update_delete_dialog.check_in_date_edit.setMaximumDate(datetime.datetime.strptime('9999-12-31', '%Y-%m-%d'))
        self.update_delete_dialog.check_in_date_edit.setDate(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
        self.update_delete_dialog.check_out_date_edit.setMinimumDate(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
        self.update_delete_dialog.check_out_date_edit.setMaximumDate(datetime.datetime.strptime('9999-12-31', '%Y-%m-%d'))
        self.update_delete_dialog.check_out_date_edit.setDate(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
        self.update_delete_dialog.adults_count_spin_box.setValue(1)
        self.update_delete_dialog.children_count_spin_box.setValue(0)
        self.update_delete_dialog.first_name_line_edit.clear()
        self.update_delete_dialog.last_name_line_edit.clear()
        self.update_delete_dialog.passport_number_line_edit.clear()
        self.update_delete_dialog.email_line_edit.clear()
        self.update_delete_dialog.phone_number_line_edit.clear()

    def administer_item(self, item):
        index = self.search_combo_box.currentIndex()
        if (index == MainWindow.CITY_PAGE \
            or index == MainWindow.HOTEL_PAGE \
            or index == MainWindow.APARTMENT_PAGE) \
            and item.listWidget().currentRow() == 0 \
            and item.text()[0: 4] == 'Add ':

            self.add_dialog.add_stacked_widget.setCurrentIndex(index)

            text = item.text()
            if index == MainWindow.CITY_PAGE:
                name_start = text.find('Name: ') + 6
                name_end = text.find('\n', name_start)
                self.add_dialog.city_name_line_edit.setText(text[name_start: name_end])

            elif index == MainWindow.HOTEL_PAGE:
                hotel_name_start = text.find('Name: ')
                if hotel_name_start >= 0:
                    hotel_name_start += 6
                    hotel_name_end = text.find('\n', hotel_name_start)
                    self.add_dialog.hotel_name_line_edit.setText(text[hotel_name_start: hotel_name_end])
                city_name_start = text.find('City: ')
                if city_name_start >= 0:
                    city_name_start += 6
                    city_name_end = text.find('\n', city_name_start)
                    self.add_dialog.city_name_line_edit_2.setText(text[city_name_start: city_name_end])

            elif index == MainWindow.APARTMENT_PAGE:
                hotel_name_start = text.find('Hotel: ')
                if hotel_name_start >= 0:
                    hotel_name_start += 7
                    hotel_name_end = text.find('\n', hotel_name_start)
                    self.add_dialog.hotel_name_line_edit_2.setText(text[hotel_name_start: hotel_name_end])
                apart_number_start = text.find('Number: ')
                if apart_number_start >= 0:
                    apart_number_start += 8
                    apart_number_end = text.find('\n', apart_number_start)
                    apart_number = int(text[apart_number_start: apart_number_end])
                    self.add_dialog.apart_number_spin_box.setValue(apart_number)

            self.add_dialog.exec()
            self.clear_add_dialog()

        else:
            self.update_delete_dialog.update_delete_stacked_widget.setCurrentIndex(index)
            item_text = item.text()
            managing_text = str(self.update_delete_dialog.current_item_label.text())

            if index == MainWindow.CITY_PAGE:
                city_name = item_text
                self.update_delete_dialog.current_item_label.setText(managing_text + city_name)
                self.update_delete_dialog.city_name_line_edit.setText(city_name)

            elif index == MainWindow.HOTEL_PAGE:
                hotel_name_start = 0
                hotel_name_end = item_text.find('\n')
                hotel_name = item_text[hotel_name_start: hotel_name_end]
                city_name_start = hotel_name_end + 1
                city_name_end = item_text.find('\n', city_name_start)
                city_name = item_text[city_name_start: city_name_end]
                contact_number_start =  item_text.find('Contact: ', city_name_end + 1) + 9
                contact_number_end = item_text.find('\n', contact_number_start)
                contact_number = item_text[contact_number_start: contact_number_end]
                manager_name_start =  item_text.find('Manager: ', contact_number_end + 1)
                if manager_name_start >= 0:
                     manager_name_start += 9
                     manager_name_end = item_text.find('\n', manager_name_start)
                     manager_name = item_text[manager_name_start: manager_name_end]
                else:
                    manager_name = None
                text_desc_start = manager_name_end + 1 if manager_name is not None else contact_number_end + 1
                text_desc_end = item_text.find('\n', text_desc_start)
                text_desc = item_text[text_desc_start: text_desc_end]
                rating_start =  item_text.find('Rating: ', text_desc_end + 1)
                if rating_start >= 0:
                     rating_start += 8
                     rating_end = item_text.find('\n', rating_start)
                     rating = int(item_text[rating_start: rating_end])
                else:
                    rating = None
                ticks_start = rating_end + 1 if rating is not None else text_desc_end + 1
                restaurant = 1 if item_text.find('Hotel restaurant', ticks_start) >= 0 else 0
                free_meals = 1 if item_text.find('Free meals', ticks_start) >= 0 else 0
                pool = 1 if item_text.find('Private pool', ticks_start) >= 0 else 0
                free_internet = 1 if item_text.find('Free internet', ticks_start) >= 0 else 0

                self.update_delete_dialog.current_item_label.setText(managing_text + hotel_name)
                self.update_delete_dialog.hotel_name_line_edit.setText(hotel_name)
                self.update_delete_dialog.city_name_line_edit_2.setText(city_name)
                self.update_delete_dialog.contact_number_line_edit.setText(contact_number)
                if manager_name is not None:
                    self.update_delete_dialog.manager_name_line_edit.setText(manager_name)
                self.update_delete_dialog.text_desc_text_edit.setText(text_desc)
                self.update_delete_dialog.rating_combo_box.setCurrentIndex(rating if rating is not None else 0)
                self.update_delete_dialog.restaurant_check_box.setChecked(restaurant)
                self.update_delete_dialog.free_meals_check_box.setChecked(free_meals)
                self.update_delete_dialog.pool_check_box.setChecked(pool)
                self.update_delete_dialog.free_internet_check_box.setChecked(free_internet)

            elif index == MainWindow.APARTMENT_PAGE:
                hotel_name_start = 0
                first_new_line = item_text.find('\n')
                hotel_name_end = item_text.rfind(',', 0, first_new_line)
                hotel_name = item_text[hotel_name_start: hotel_name_end]
                apartment_number_start = item_text.rfind('.', 0, first_new_line) + 1
                apartment_number_end = first_new_line
                apartment_number = int(item_text[apartment_number_start: apartment_number_end])
                room_count_start = first_new_line + 1
                room_count_end = item_text.find(' ', room_count_start)
                room_count = int(item_text[room_count_start: room_count_end])
                second_new_line = item_text.find('\n', first_new_line + 1)
                capacity_end = item_text.rfind(',', 0, second_new_line)
                capacity_start = item_text.rfind(' ', 0, capacity_end) + 1
                capacity = int(item_text[capacity_start: capacity_end])
                price_per_night_euro_start = capacity_end + 2
                price_per_night_euro_end = item_text.find(' ', price_per_night_euro_start)
                price_per_night_euro = float(item_text[price_per_night_euro_start: price_per_night_euro_end])
                ac = 1 if item_text.find('AC', second_new_line) >= 0 else 0
                minibar = 1 if item_text.find('Minibar', second_new_line) >= 0 else 0
                tv = 1 if item_text.find('TV', second_new_line) >= 0 else 0
                double_bed = 1 if item_text.find('Double bed', second_new_line) >= 0 else 0

                self.update_delete_dialog.current_item_label.setText(managing_text + hotel_name + f', Apart. No.{apartment_number}')
                self.update_delete_dialog.hotel_name_line_edit_2.setText(hotel_name)
                self.update_delete_dialog.apart_number_spin_box.setValue(apartment_number)
                self.update_delete_dialog.room_count_spin_box.setValue(room_count)
                self.update_delete_dialog.apart_capacity_spin_box.setValue(capacity)
                self.update_delete_dialog.price_per_night_spin_box.setValue(price_per_night_euro)
                self.update_delete_dialog.ac_check_box.setChecked(ac)
                self.update_delete_dialog.minibar_check_box.setChecked(minibar)
                self.update_delete_dialog.tv_check_box.setChecked(tv)
                self.update_delete_dialog.double_bed_check_box.setChecked(double_bed)

            elif index == MainWindow.BOOKING_PAGE:
                hotel_name_start = 0
                first_new_line = item_text.find('\n')
                second_comma = item_text.rfind(',', 0, first_new_line)
                hotel_name_end = item_text.rfind(',', 0, second_comma)
                hotel_name = item_text[hotel_name_start: hotel_name_end]
                apartment_number_start = item_text.rfind('.', 0, second_comma) + 1
                apartment_number_end = second_comma
                apartment_number = int(item_text[apartment_number_start: apartment_number_end])
                passport_number_start = item_text.rfind(':', 0, first_new_line) + 2
                passport_number_end = first_new_line
                passport_number = item_text[passport_number_start: passport_number_end]
                book_date_start = item_text.find(':', first_new_line) + 2
                book_date_end = item_text.find(',', book_date_start)
                book_date = item_text[book_date_start: book_date_end]
                check_in_start = item_text.find(':', book_date_end) + 2
                check_in_end = item_text.find(',', check_in_start)
                check_in = item_text[check_in_start:check_in_end]
                check_out_start = item_text.find(':', check_in_end) + 2
                check_out_end = item_text.find('\n', check_out_start)
                check_out = item_text[check_out_start:check_out_end]
                adults_count_start = check_out_end + 1
                adults_count_end = item_text.find(' ', adults_count_start)
                adults_count = int(item_text[adults_count_start: adults_count_end])
                children_count_start = item_text.find(',', adults_count_end) + 2
                children_count_end = item_text.find(' ', children_count_start)
                children_count = int(item_text[children_count_start: children_count_end])

                self.update_delete_dialog.current_item_label.setText(managing_text + hotel_name + f', Apart. No.{apartment_number}, Check-in: {check_in}')
                self.update_delete_dialog.passport_number_line_edit_3.setText(passport_number)
                self.update_delete_dialog.hotel_name_line_edit_5.setText(hotel_name)
                self.update_delete_dialog.apart_number_spin_box_3.setValue(apartment_number)
                check_in_date_time = datetime.datetime.strptime(check_in, '%Y-%m-%d')
                self.update_delete_dialog.check_in_date_edit.setMinimumDate(check_in_date_time)
                self.update_delete_dialog.check_in_date_edit.setMaximumDate(check_in_date_time + datetime.timedelta(days=366))
                self.update_delete_dialog.check_out_date_edit.setMinimumDate(check_in_date_time + datetime.timedelta(days=1))
                self.update_delete_dialog.check_out_date_edit.setMaximumDate(check_in_date_time + datetime.timedelta(days=367))
                self.update_delete_dialog.check_out_date_edit.setDate(datetime.datetime.strptime(check_out, '%Y-%m-%d'))
                self.update_delete_dialog.adults_count_spin_box.setValue(adults_count)
                self.update_delete_dialog.children_count_spin_box.setValue(children_count)

            elif index == MainWindow.GUEST_PAGE:
                first_name_start = item_text.find(':') + 2
                first_name_end = item_text.find('\n', first_name_start)
                first_name = item_text[first_name_start: first_name_end]
                last_name_start = item_text.find(':', first_name_end) + 2
                last_name_end = item_text.find('\n', last_name_start)
                last_name = item_text[last_name_start: last_name_end]
                passport_number_start = item_text.find(':', last_name_end) + 2
                passport_number_end = item_text.find('\n', passport_number_start)
                passport_number = item_text[passport_number_start: passport_number_end]
                email_start = item_text.find(':', passport_number_end) + 2
                email_end = item_text.find('\n', email_start)
                if email_end < 0:
                    email_end = len(item_text)
                email = item_text[email_start: email_end]
                if email_end != len(item_text):
                     phone_number_start =  item_text.find(':', email_end + 1)
                     phone_number_start += 2
                     phone_number_end = len(item_text)
                     phone_number = item_text[phone_number_start: phone_number_end]
                else:
                    phone_number = None

                self.update_delete_dialog.current_item_label.setText(managing_text + passport_number)
                self.update_delete_dialog.first_name_line_edit.setText(first_name)
                self.update_delete_dialog.last_name_line_edit.setText(last_name)
                self.update_delete_dialog.passport_number_line_edit.setText(passport_number)
                self.update_delete_dialog.email_line_edit.setText(email)
                if phone_number is not None:
                    self.update_delete_dialog.phone_number_line_edit.setText(phone_number)

            self.update_delete_dialog.delete_button.setEnabled(True)
            self.update_delete_dialog.exec()
            self.clear_update_delete_dialog()

        self.search_list.clear()

    def add_entry(self):
        index = self.add_dialog.add_stacked_widget.currentIndex()
        if index == MainWindow.CITY_PAGE:
            city_name = self.add_dialog.city_name_line_edit.text()
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO CITY (city_name)
                                VALUES ('{city_name}')""")
        elif index == MainWindow.HOTEL_PAGE:
            hotel_name = self.add_dialog.hotel_name_line_edit.text()
            city_name = self.add_dialog.city_name_line_edit_2.text()
            contact_number = self.add_dialog.contact_number_line_edit.text()
            manager_name = self.add_dialog.manager_name_line_edit.text()
            manager_name_line = f", '{manager_name}'" if manager_name != '' else ''
            text_desc = self.add_dialog.text_desc_text_edit.toPlainText()
            try:
                rating = int(self.add_dialog.rating_combo_box.currentText())
            except ValueError:
                rating = None
            restaurant = int(self.add_dialog.restaurant_check_box.isChecked())
            free_meals = int(self.add_dialog.free_meals_check_box.isChecked())
            pool = int(self.add_dialog.pool_check_box.isChecked())
            free_internet = int(self.add_dialog.free_internet_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO HOTEL (hotel_name, city_id, contact_number{f', manager_name' if manager_name != '' else ''}) " +\
                                f"VALUES ('{hotel_name}', " +\
                                f"(SELECT city_id FROM CITY WHERE city_name = '{city_name}'), " +\
                                f"'{contact_number}'" +\
                                manager_name_line +\
                                ")")
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc{f', rating' if rating is not None else ''}, restaurant, free_meals, pool, free_internet) " +\
                                f"VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, " +\
                                f"'{text_desc}', " +\
                                f"{f'{rating}, ' if rating is not None else ''}" +\
                                f"{restaurant}, " +\
                                f"{free_meals}, " +\
                                f"{pool}, " +\
                                f"{free_internet}" +\
                                ")")
        elif index == MainWindow.APARTMENT_PAGE:
            hotel_name = self.add_dialog.hotel_name_line_edit_2.text()
            apartment_number = self.add_dialog.apart_number_spin_box.value()
            room_count = self.add_dialog.room_count_spin_box.value()
            capacity = self.add_dialog.apart_capacity_spin_box.value()
            price_per_night_euro = self.add_dialog.price_per_night_spin_box.value()
            ac = int(self.add_dialog.ac_check_box.isChecked())
            minibar = int(self.add_dialog.minibar_check_box.isChecked())
            tv = int(self.add_dialog.tv_check_box.isChecked())
            double_bed = int(self.add_dialog.double_bed_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro) " +\
                                f"VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}'), " +\
                                f"{apartment_number}, " +\
                                f"{room_count}, " +\
                                f"{capacity}, " +\
                                f"{price_per_night_euro}" +\
                                ")")
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO APARTMENT_DESCRIPTION (apart_id, air_conditioner, minibar, tv, double_bed) " +\
                                f"VALUES ((SELECT apart_id FROM APARTMENT " +\
                                f"        WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}') " +\
                                f"        AND apart_number = {apartment_number}), " +\
                                f"{ac}, " +\
                                f"{minibar}, " +\
                                f"{tv}, " +\
                                f"{double_bed}" +\
                                ")")

        with self.db_connection.cursor() as cursor:
            cursor.execute('COMMIT')

        self.add_dialog.accept()

    def update_entry(self):
        index = self.update_delete_dialog.update_delete_stacked_widget.currentIndex()
        managing_text = str(self.update_delete_dialog.current_item_label.text())
        if index == MainWindow.CITY_PAGE:
            old_city_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: ]
            city_name = self.update_delete_dialog.city_name_line_edit.text()

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE CITY
                                    SET city_name = '{city_name}'
                                    WHERE city_name = '{old_city_name}'
                """)

        elif index == MainWindow.HOTEL_PAGE:
            old_hotel_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: ]
            hotel_name = self.update_delete_dialog.hotel_name_line_edit.text()
            city_name = self.update_delete_dialog.city_name_line_edit_2.text()
            contact_number = self.update_delete_dialog.contact_number_line_edit.text()
            manager_name = self.update_delete_dialog.manager_name_line_edit.text()
            text_desc = self.update_delete_dialog.text_desc_text_edit.toPlainText()
            try:
                rating = int(self.update_delete_dialog.rating_combo_box.currentText())
            except ValueError:
                rating = None
            restaurant = int(self.update_delete_dialog.restaurant_check_box.isChecked())
            free_meals = int(self.update_delete_dialog.free_meals_check_box.isChecked())
            pool = int(self.update_delete_dialog.pool_check_box.isChecked())
            free_internet = int(self.update_delete_dialog.free_internet_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE HOTEL_DESCRIPTION
                                    SET text_desc = '{text_desc}',
                                        rating = {rating if rating is not None else 'null'},
                                        restaurant = {restaurant},
                                        free_meals = {free_meals},
                                        pool = {pool},
                                        free_internet = {free_internet}
                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                """)

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE HOTEL
                                    SET hotel_name = '{hotel_name}',
                                        city_id = (SELECT city_id FROM CITY WHERE city_name = '{city_name}'),
                                        contact_number = '{contact_number}',
                                        manager_name = {f"'{manager_name}'" if manager_name != '' else 'null'}
                                    WHERE hotel_name = '{old_hotel_name}'
                """)

        elif index == MainWindow.APARTMENT_PAGE:
            last_comma = managing_text.rfind(',')
            old_hotel_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: last_comma]
            last_dot = managing_text.rfind('.')
            old_apartment_number = int(managing_text[last_dot + 1: ])
            hotel_name = self.update_delete_dialog.hotel_name_line_edit_2.text()
            apart_number = self.update_delete_dialog.apart_number_spin_box.value()
            room_count = self.update_delete_dialog.room_count_spin_box.value()
            capacity = self.update_delete_dialog.apart_capacity_spin_box.value()
            price_per_night_euro = self.update_delete_dialog.price_per_night_spin_box.value()
            ac = int(self.update_delete_dialog.ac_check_box.isChecked())
            minibar = int(self.update_delete_dialog.minibar_check_box.isChecked())
            tv = int(self.update_delete_dialog.tv_check_box.isChecked())
            double_bed = int(self.update_delete_dialog.double_bed_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE APARTMENT_DESCRIPTION
                                    SET air_conditioner = {ac},
                                        minibar = {minibar},
                                        tv = {tv},
                                        double_bed = {double_bed}
                                    WHERE apart_id = (SELECT apart_id FROM APARTMENT
                                                      WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                                      AND apart_number = {old_apartment_number})
                """)

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE APARTMENT
                                    SET hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}'),
                                        apart_number = {apart_number},
                                        room_count = {room_count},
                                        apart_capacity = {capacity},
                                        price_per_night_euro = {price_per_night_euro}
                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                        AND apart_number = {old_apartment_number}
                """)

        elif index == MainWindow.BOOKING_PAGE:
            old_hotel_name_start = managing_text.find(':') + 2
            old_hotel_name_end = managing_text.find(',')
            old_hotel_name = managing_text[old_hotel_name_start: old_hotel_name_end]
            last_comma = managing_text.rfind(',')
            old_apart_number_start = managing_text.rfind('.') + 1
            old_apart_number = int(managing_text[old_apart_number_start: last_comma])
            old_check_in_start = managing_text.rfind(':') + 2
            old_check_in = managing_text[old_check_in_start: ]

            passport_number = self.update_delete_dialog.passport_number_line_edit_3.text()
            hotel_name = self.update_delete_dialog.hotel_name_line_edit_5.text()
            apart_number = self.update_delete_dialog.apart_number_spin_box_3.value()
            check_in = str(self.update_delete_dialog.check_in_date_edit.date().toPyDate())
            check_out = str(self.update_delete_dialog.check_out_date_edit.date().toPyDate())
            adults_count = self.update_delete_dialog.adults_count_spin_box.value()
            children_count = self.update_delete_dialog.children_count_spin_box.value()

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE BOOKING
                                    SET guest_id = (SELECT guest_id FROM GUEST WHERE passport_number = '{passport_number}'),
                                        apart_id = (SELECT apart_id FROM APARTMENT
                                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                          AND apart_number = {apart_number}),
                                        check_in = TO_DATE('{check_in}', 'YYYY-MM-DD'),
                                        check_out = TO_DATE('{check_out}', 'YYYY-MM-DD'),
                                        adults_count = {adults_count},
                                        children_count = {children_count}
                                    WHERE apart_id = (SELECT apart_id FROM APARTMENT
                                                      WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                                      AND apart_number = {old_apart_number})
                                          AND check_in LIKE TO_DATE('{old_check_in}', 'YYYY-MM-DD')
                                          AND (SELECT apart_capacity FROM APARTMENT
                                                            WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                            AND apart_number = {apart_number})
                                              >= {adults_count + children_count}
                                          AND ((SELECT COUNT(*)
                                                 FROM BOOKING b,
                                                      (SELECT * FROM APARTMENT
                                                       WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                             AND apart_number = {apart_number})
                                                      a
                                                 WHERE b.apart_id = a.apart_id
                                                     AND b.check_out > TO_DATE('{check_in}', 'YYYY-MM-DD')
                                                     AND b.check_in < TO_DATE('{check_out}', 'YYYY-MM-DD')) = 0
                                              OR {int(hotel_name == old_hotel_name and apart_number == old_apart_number)} > 0)
                """)

        elif index == MainWindow.GUEST_PAGE:
            old_passport_number_start = managing_text.find(':') + 2
            old_passport_number = managing_text[old_passport_number_start: ]

            first_name = self.update_delete_dialog.first_name_line_edit.text()
            last_name = self.update_delete_dialog.last_name_line_edit.text()
            passport_number = self.update_delete_dialog.passport_number_line_edit.text()
            email = self.update_delete_dialog.email_line_edit.text()
            phone_number = self.update_delete_dialog.phone_number_line_edit.text()

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE GUEST
                                    SET first_name = '{first_name}',
                                        last_name = '{last_name}',
                                        passport_number = '{passport_number}',
                                        email = '{email}',
                                        phone_number = {f"'{phone_number}'" if phone_number != '' else 'null'}
                                    WHERE passport_number = '{old_passport_number}'
                """)

        with self.db_connection.cursor() as cursor:
            cursor.execute('COMMIT')

        self.update_delete_dialog.accept()

    def delete_entry(self):
        index = self.update_delete_dialog.update_delete_stacked_widget.currentIndex()
        managing_text = str(self.update_delete_dialog.current_item_label.text())
        if index == MainWindow.CITY_PAGE:
            city_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: ]

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""DELETE FROM CITY
                                    WHERE city_name = '{city_name}'
                """)

        elif index == MainWindow.HOTEL_PAGE:
            old_hotel_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: ]
            hotel_name = self.update_delete_dialog.hotel_name_line_edit.text()
            city_name = self.update_delete_dialog.city_name_line_edit_2.text()
            contact_number = self.update_delete_dialog.contact_number_line_edit.text()
            manager_name = self.update_delete_dialog.manager_name_line_edit.text()
            text_desc = self.update_delete_dialog.text_desc_text_edit.toPlainText()
            try:
                rating = int(self.update_delete_dialog.rating_combo_box.currentText())
            except ValueError:
                rating = None
            restaurant = int(self.update_delete_dialog.restaurant_check_box.isChecked())
            free_meals = int(self.update_delete_dialog.free_meals_check_box.isChecked())
            pool = int(self.update_delete_dialog.pool_check_box.isChecked())
            free_internet = int(self.update_delete_dialog.free_internet_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE HOTEL_DESCRIPTION
                                    SET text_desc = '{text_desc}',
                                        rating = {rating if rating is not None else 'null'},
                                        restaurant = {restaurant},
                                        free_meals = {free_meals},
                                        pool = {pool},
                                        free_internet = {free_internet}
                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                """)

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE HOTEL
                                    SET hotel_name = '{hotel_name}',
                                        city_id = (SELECT city_id FROM CITY WHERE city_name = '{city_name}'),
                                        contact_number = '{contact_number}',
                                        manager_name = {f"'{manager_name}'" if manager_name != '' else 'null'}
                                    WHERE hotel_name = '{old_hotel_name}'
                """)

        elif index == MainWindow.APARTMENT_PAGE:
            last_comma = managing_text.rfind(',')
            old_hotel_name = managing_text[MainWindow.CURRENT_ITEM_BASE_LABEL_LEN: last_comma]
            last_dot = managing_text.rfind('.')
            old_apartment_number = int(managing_text[last_dot + 1: ])
            hotel_name = self.update_delete_dialog.hotel_name_line_edit_2.text()
            apart_number = self.update_delete_dialog.apart_number_spin_box.value()
            room_count = self.update_delete_dialog.room_count_spin_box.value()
            capacity = self.update_delete_dialog.apart_capacity_spin_box.value()
            price_per_night_euro = self.update_delete_dialog.price_per_night_spin_box.value()
            ac = int(self.update_delete_dialog.ac_check_box.isChecked())
            minibar = int(self.update_delete_dialog.minibar_check_box.isChecked())
            tv = int(self.update_delete_dialog.tv_check_box.isChecked())
            double_bed = int(self.update_delete_dialog.double_bed_check_box.isChecked())

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE APARTMENT_DESCRIPTION
                                    SET air_conditioner = {ac},
                                        minibar = {minibar},
                                        tv = {tv},
                                        double_bed = {double_bed}
                                    WHERE apart_id = (SELECT apart_id FROM APARTMENT
                                                      WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                                      AND apart_number = {old_apartment_number})
                """)

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE APARTMENT
                                    SET hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}'),
                                        apart_number = {apart_number},
                                        room_count = {room_count},
                                        apart_capacity = {capacity},
                                        price_per_night_euro = {price_per_night_euro}
                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                        AND apart_number = {old_apartment_number}
                """)

        elif index == MainWindow.BOOKING_PAGE:
            old_hotel_name_start = managing_text.find(':') + 2
            old_hotel_name_end = managing_text.find(',')
            old_hotel_name = managing_text[old_hotel_name_start: old_hotel_name_end]
            last_comma = managing_text.rfind(',')
            old_apart_number_start = managing_text.rfind('.') + 1
            old_apart_number = int(managing_text[old_apart_number_start: last_comma])
            old_check_in_start = managing_text.rfind(':') + 2
            old_check_in = managing_text[old_check_in_start: ]

            passport_number = self.update_delete_dialog.passport_number_line_edit_3.text()
            hotel_name = self.update_delete_dialog.hotel_name_line_edit_5.text()
            apart_number = self.update_delete_dialog.apart_number_spin_box_3.value()
            check_in = str(self.update_delete_dialog.check_in_date_edit.date().toPyDate())
            check_out = str(self.update_delete_dialog.check_out_date_edit.date().toPyDate())
            adults_count = self.update_delete_dialog.adults_count_spin_box.value()
            children_count = self.update_delete_dialog.children_count_spin_box.value()

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE BOOKING
                                    SET guest_id = (SELECT guest_id FROM GUEST WHERE passport_number = '{passport_number}'),
                                        apart_id = (SELECT apart_id FROM APARTMENT
                                                    WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                          AND apart_number = {apart_number}),
                                        check_in = TO_DATE('{check_in}', 'YYYY-MM-DD'),
                                        check_out = TO_DATE('{check_out}', 'YYYY-MM-DD'),
                                        adults_count = {adults_count},
                                        children_count = {children_count}
                                    WHERE apart_id = (SELECT apart_id FROM APARTMENT
                                                      WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{old_hotel_name}')
                                                      AND apart_number = {old_apart_number})
                                          AND check_in LIKE TO_DATE('{old_check_in}', 'YYYY-MM-DD')
                                          AND (SELECT apart_capacity FROM APARTMENT
                                                            WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                            AND apart_number = {apart_number})
                                              >= {adults_count + children_count}
                                          AND ((SELECT COUNT(*)
                                                 FROM BOOKING b,
                                                      (SELECT * FROM APARTMENT
                                                       WHERE hotel_id = (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{hotel_name}')
                                                             AND apart_number = {apart_number})
                                                      a
                                                 WHERE b.apart_id = a.apart_id
                                                     AND b.check_out > TO_DATE('{check_in}', 'YYYY-MM-DD')
                                                     AND b.check_in < TO_DATE('{check_out}', 'YYYY-MM-DD')) = 0
                                              OR {int(hotel_name == old_hotel_name and apart_number == old_apart_number)} > 0)
                """)

        elif index == MainWindow.GUEST_PAGE:
            old_passport_number_start = managing_text.find(':') + 2
            old_passport_number = managing_text[old_passport_number_start: ]

            first_name = self.update_delete_dialog.first_name_line_edit.text()
            last_name = self.update_delete_dialog.last_name_line_edit.text()
            passport_number = self.update_delete_dialog.passport_number_line_edit.text()
            email = self.update_delete_dialog.email_line_edit.text()
            phone_number = self.update_delete_dialog.phone_number_line_edit.text()

            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""UPDATE GUEST
                                    SET first_name = '{first_name}',
                                        last_name = '{last_name}',
                                        passport_number = '{passport_number}',
                                        email = '{email}',
                                        phone_number = {f"'{phone_number}'" if phone_number != '' else 'null'}
                                    WHERE passport_number = '{old_passport_number}'
                """)

        with self.db_connection.cursor() as cursor:
            cursor.execute('COMMIT')

        self.update_delete_dialog.accept()

    def clean_up(self):
        self.db_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        app.exec_()
    finally:
        window.clean_up()
