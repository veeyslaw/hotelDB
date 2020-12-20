import sys
import datetime
import cx_Oracle
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QHBoxLayout
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

        self.connect_ui()
        self.error_dialog = QDialog(self)
        self.configure_dialogs()

        self.db_connection = cx_Oracle.connect('tema', 'vlad', 'localhost/xe')

    def connect_ui(self):
        self.book_button.clicked.connect(self.go_to_book_page)
        self.admin_button.clicked.connect(self.go_to_admin_page)
        self.search_button.clicked.connect(self.search_bookings)
        self.back_button_2.clicked.connect(self.go_to_book_page)
        self.back_button.clicked.connect(self.go_to_offers_page)
        self.confirm_button.clicked.connect(self.confirm_booking)
        self.another_booking_button.clicked.connect(self.go_to_book_page)
        self.quit_button.clicked.connect(self.close)
        self.quit_admin_button.clicked.connect(self.close)
        self.search_button_2.clicked.connect(self.search_admin)
        self.search_combo_box.currentIndexChanged.connect(self.on_search_combo_box_change)
        self.check_in_date_edit.dateChanged.connect(self.on_check_in_date_change)

    def configure_dialogs(self):
        self.error_dialog.resize(300, 300)
        self.error_dialog.setWindowTitle('Error')
        button_box = QDialogButtonBox(self.error_dialog)
        horizontal_layout = QHBoxLayout(self.error_dialog)
        button_box.setStandardButtons(QDialogButtonBox.Ok)
        button_box.setObjectName("button_box")
        horizontal_layout.addWidget(button_box)
        button_box.accepted.connect(self.error_dialog.accept)
        # self.error_dialog.exec()

    def prepare_city_options(self):
        self.city_combo_box.clear()
        self.city_combo_box.addItem('Any city')
        with self.db_connection.cursor() as cursor:
            cursor.execute('SELECT * FROM CITY')
            for row in cursor:
                self.city_combo_box.addItem(row[1])

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

    def go_to_book_page(self):
        self.prepare_city_options()
        self.prepare_date_edits()
        self.reset_options()
        self.main_stacked_widget.setCurrentIndex(MainWindow.BOOK_PAGE)

    def go_to_admin_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.ADMIN_PAGE)

    def search_bookings(self):
        if self.city_combo_box.currentIndex() == 0:
            city = None
        else:
            city = str(self.city_combo_box.currentText())
        check_in = str(self.check_in_date_edit.date().toPyDate())
        check_out = str(self.check_out_date_edit.date().toPyDate())
        try:
            room_count = int(self.rooms_combo_box.currentText())
        except ValueError:
            room_count = None
        adults_count = self.adults_spin_box.value()
        children_count = self.children_spin_box.value()
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
                                AND b.check_out > TO_DATE('{check_in}', 'YYYY/MM/DD')
                                AND b.check_in <= TO_DATE('{check_out}', 'YYYY/MM/DD')) = 0)
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
                    AND apart_capacity >= {adults_count + children_count}
                    {f"AND city_name = '{city}'" if city is not None else ''}
                    {f'AND rating >= {rating}' if rating is not None else ''}
                    {f'AND room_count >= {room_count}' if room_count is not None else ''}
                """

        print(check_in)
        print(check_out)
        print(query)

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor:
                print(row)
        # TODO query db
        # TODO go to only if good query
        offers = None
        self.go_to_offers_page(offers)

    def go_to_offers_page(self, offers):
        self.offers_list.clear()
        # TODO add offers to list
        # TODO update period
        self.main_stacked_widget.setCurrentIndex(MainWindow.OFFERS_PAGE)
##############################################################################################################################
    def book(self):
        # TODO transaction offer
        self.first_name_line_edit.clear()
        self.last_name_line_edit.clear()
        self.passport_line_edit.clear()
        self.email_line_edit.clear()
        self.phone_number_line_edit.clear()
        self.main_stacked_widget.setCurrentIndex(MainWindow.CHECK_OUT_PAGE)

    def confirm_booking(self):
        # TODO complete db transaction
        self.main_stacked_widget.setCurrentIndex(MainWindow.SUCCESSFUL_PAGE)

    def on_search_combo_box_change(self, index):
        self.search_stacked_widget.setCurrentIndex(index)

    def search_city(self):
        city_name = str(self.city_name_line_edit.text())
        # TODO query bd for them
        items = None
        return items

    def search_hotel(self):
        hotel_name = str(self.hotel_name_line_edit.text())
        city_name = str(self.city_name_line_edit_2.text())
        # TODO query bd for them
        items = None
        return items

    def search_apartment(self):
        hotel_name = str(self.hotel_name_line_edit_2.text())
        apartment_number = self.apartment_number_spin_box.value()
        # TODO query bd for them
        items = None
        return items

    def search_booking(self):
        hotel_name = str(self.hotel_name_line_edit_3.text())
        apartment_number = self.apartment_number_spin_box_2.value()
        passport_number = str(self.passport_line_edit_2.text())
        check_in = self.check_in_date_edit_2.date()
        # TODO query bd for them
        items = None
        return items

    def search_guest(self):
        first_name = str(self.first_name_line_edit_2.text())
        last_name = str(self.last_name_line_edit_2.text())
        passport_number = str(self.passport_line_edit_3.text())
        email = str(self.email_line_edit_2.text())
        # TODO query bd for them
        items = None
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
        # TODO set check in date to sysdate
        self.first_name_line_edit_2.clear()
        self.last_name_line_edit_2.clear()
        self.passport_line_edit_3.clear()
        self.email_line_edit_2.clear()

    def search_admin(self):
        index = self.search_combo_box.currentIndex()
        if index == MainWindow.CITY_PAGE:
            items = self.search_city()
        elif index == MainWindow.HOTEL_PAGE:
            items = self.search_hotel()
        elif index == MainWindow.APARTMENT_PAGE:
            items = self.search_apartment()
        elif index == MainWindow.BOOKING_PAGE:
            items = self.search_booking()
        elif index == MainWindow.GUEST_PAGE:
            items = self.search_guest()
        self.search_list.clear()
        # TODO add items to list
        self.clear_search_pages()

    def clean_up(self):
        # TODO remove print before final
        print('### CLOSING CONNECTION ###')
        self.db_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        app.exec_()
    finally:
        window.clean_up()
