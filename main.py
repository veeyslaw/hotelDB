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
        # loadUi("Front/update_delete_dialog_form.ui", self.update_delete_dialog)

    def reset_book_cache(self):
        self.check_in = '2000-01-01'
        self.check_out = '2000-01-01'
        self.adults_count = -1
        self.children_count = -1
        self.hotel_name = ''
        self.apartment_number = -1

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
                    a.apart_number, room_count, price_per_night_euro,
                    air_conditioner, minibar, tv, double_bed
                FROM
                    CITY c,
                    HOTEL h,
                    HOTEL_DESCRIPTION hd,
                    (SELECT hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro
                     FROM APARTMENT inner_a
                     WHERE (SELECT COUNT(*)
                            FROM BOOKING b
                            WHERE b.hotel_id = inner_a.hotel_id
                                AND b.apart_number = inner_a.apart_number
                                AND b.check_out > TO_DATE('{self.check_in}', 'YYYY-MM-DD')
                                AND b.check_in < TO_DATE('{self.check_out}', 'YYYY-MM-DD')) = 0)
                    a,
                    APARTMENT_DESCRIPTION ad
                WHERE
                    c.city_id = h.city_id
                    AND h.hotel_id = hd.hotel_id
                    AND a.hotel_id = h.hotel_id
                    AND ad.hotel_id = a.hotel_id
                    AND ad.apart_number = a.apart_number
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

        self.offers_list.itemClicked.connect(self.book)
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
            cursor.execute(f"SELECT first_name, last_name, email, phone_number FROM GUEST WHERE LOWER(passport_number) = LOWER('{passport_number}')")
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
            cursor.execute(f"""INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
                            VALUES ((SELECT guest_id FROM GUEST WHERE LOWER(passport_number) = LOWER('{passport_number}')),
                                    (SELECT hotel_id FROM HOTEL WHERE hotel_name = '{self.hotel_name}'),
                                    {self.apartment_number},
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
            items = [f'{row[1]}\n{row[0]}\nContact: {row[2]}{f"{chr(10)}Manager: {row[3]}" if row[3] is not None else ""}\n' +\
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
            cursor.execute("SELECT hotel_name, a.apart_number, room_count, apart_capacity, price_per_night_euro, " +\
                                    "air_conditioner, minibar, tv, double_bed " +\
                            "FROM HOTEL h, APARTMENT a, APARTMENT_DESCRIPTION ad " +\
                            f"WHERE LOWER(hotel_name) LIKE LOWER('%{hotel_name}%') " +\
                            f"{f'AND a.apart_number = {apartment_number} ' if apartment_number > 0 else ''}" +\
                            "AND h.hotel_id = a.hotel_id " +\
                            "AND ad.hotel_id = a.hotel_id " +\
                            "AND ad.apart_number = a.apart_number")
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
                            "FROM BOOKING b, GUEST g, HOTEL h " +\
                            f"WHERE LOWER(hotel_name) LIKE LOWER('%{hotel_name}%') " +\
                            f"{f'AND apart_number = {apartment_number} ' if apartment_number > 0 else ''}" +\
                            f"AND LOWER(passport_number) LIKE LOWER('%{passport_number}%') " +\
                            check_in_line +\
                            "AND h.hotel_id = b.hotel_id " +\
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
            items = [f'{row[0]} {row[1]}\nPassport: {row[2]}\nEmail: {row[3]}' +\
                    f'{f"{chr(10)}Phone number: {row[4]}" if row[4] is not None else ""}'
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
