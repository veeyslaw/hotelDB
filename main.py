import sys
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

    def connect_buttons(self):
        self.book_buttont.clicked.connect(self.go_to_book_page)
        self.admin_button.clicked.connect(self.go_to_admin_page)
        

    def go_to_book_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.WELCOME_PAGE)

    def go_to_admin_page(self):
        self.main_stacked_widget.setCurrentIndex(MainWindow.ADMIN_PAGE)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
