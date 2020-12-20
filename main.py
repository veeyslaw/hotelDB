import sys
import cx_Oracle
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        self.connect_buttons()
        self.db_connection = cx_Oracle.connect('tema', 'vlad', 'localhost/xe')

    def connect_buttons(self):
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

    def set_city_options(self):
        self.city_combo_box.clear()
        with self.db_connection.cursor() as cursor:
            cursor.execute('SELECT * FROM CITY')
            for row in cursor:
                self.city_combo_box.addItem(row[1])

    def set_check_dates(self):
        with self.db_connection.cursor() as cursor:
            sysdate = cursor.execute('SELECT SYSDATE FROM DUAL').fetchone()[0].date()
        self.check_in_date_edit.setDate(sysdate)
        self.check_out_date_edit.setDate(sysdate)

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

    def go_to_book_page(self):
        self.set_city_options()
        self.set_check_dates()
        self.reset_options()
        self.main_stacked_widget.setCurrentIndex(MainWindow.BOOK_PAGE)

    def go_to_admin_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.ADMIN_PAGE)

    def search_bookings(self):
        city = str(self.city_combo_box.currentText())
        check_in = self.check_in_date_edit.date()
        check_out = self.check_out_date_edit.date()
        # TODO get current date?
        try:
            room_count = int(self.rooms_combo_box.currentText())
        except ValueError:
            room_count = 0
        adults_count = self.adults_spin_box.value()
        children_count = self.children_spin_box.value()
        try:
            rating = int(self.rating_combo_box.currentText())
        except ValueError:
            rating = 0
        restaurant = self.restaurant_check_box.isChecked()
        free_meals = self.free_meals_check_box.isChecked()
        minibar = self.minibar_check_box.isChecked()
        pool = self.pool_check_box.isChecked()
        free_internet = self.free_internet_check_box.isChecked()
        tv = self.tv_check_box.isChecked()
        ac = self.ac_check_box.isChecked()
        double_bed = self.double_bed_check_box.isChecked()
        # TODO querry db
        # TODO go to only if good querry
        offers = None
        self.go_to_offers_page(offers)

    def go_to_offers_page(self, offers):
        self.offers_list.clear()
        # TODO add offers to list
        self.main_stacked_widget.setCurrentIndex(MainWindow.OFFERS_PAGE)

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
        # TODO querry bd for them
        items = None
        return items

    def search_hotel(self):
        hotel_name = str(self.hotel_name_line_edit.text())
        city_name = str(self.city_name_line_edit_2.text())
        # TODO querry bd for them
        items = None
        return items

    def search_apartment(self):
        hotel_name = str(self.hotel_name_line_edit_2.text())
        apartment_number = self.apartment_number_spin_box.value()
        # TODO querry bd for them
        items = None
        return items

    def search_booking(self):
        hotel_name = str(self.hotel_name_line_edit_3.text())
        apartment_number = self.apartment_number_spin_box_2.value()
        passport_number = str(self.passport_line_edit_2.text())
        check_in = self.check_in_date_edit_2.date()
        # TODO querry bd for them
        items = None
        return items

    def search_guest(self):
        first_name = str(self.first_name_line_edit_2.text())
        last_name = str(self.last_name_line_edit_2.text())
        passport_number = str(self.passport_line_edit_3.text())
        email = str(self.email_line_edit_2.text())
        # TODO querry bd for them
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
