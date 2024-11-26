from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from pages import client, Lumber_input, order
from Pages.Commercial import CommercialPage
from Pages.home import MainPage
from Pages.Production import ProductionPage
from Pages.Technology import TechnologyPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_page = None
        # Устанавливаем заголовок окна
        self.setWindowTitle("Лесозавод")

        # Создаем центральный виджет с QStackedWidget для хранения страниц
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Создаем страницы и добавляем их в QStackedWidget
        self.main_page = MainPage(self.show_commercial_page, self.show_production_page, self.show_technology_page)

        self.commercial_page = CommercialPage(self.show_lumber_input_page, self.show_client_page, self.show_order_page,
                                              self.show_main_page)
        self.production_page = ProductionPage(self.show_lumber_input_page, self.show_order_page, self.show_main_page)
        self.technology_page = TechnologyPage(self.show_lumber_input_page, self.show_main_page)
        self.lumber_input_page = Lumber_input(self.show_last_page, self.commercial_page, self.production_page,
                                              self.technology_page)
        self.client_page = client(self.show_last_page, self.commercial_page)
        self.order_page = order(self.show_last_page, self.commercial_page, self.production_page)

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.commercial_page)
        self.stacked_widget.addWidget(self.production_page)
        self.stacked_widget.addWidget(self.technology_page)
        self.stacked_widget.addWidget(self.lumber_input_page)
        self.stacked_widget.addWidget(self.client_page)
        self.stacked_widget.addWidget(self.order_page)


    # Методы для навигации
    def show_last_page(self):
        if self.last_page:
            self.stacked_widget.setCurrentWidget(self.last_page)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_commercial_page(self):
        self.stacked_widget.setCurrentWidget(self.commercial_page)

    def show_production_page(self):
        self.stacked_widget.setCurrentWidget(self.production_page)

    def show_technology_page(self):
        self.stacked_widget.setCurrentWidget(self.technology_page)

    def show_lumber_input_page(self):
        self.last_page = self.stacked_widget.currentWidget()
        self.stacked_widget.setCurrentWidget(self.lumber_input_page)

    def show_client_page(self):
        self.last_page = self.stacked_widget.currentWidget()
        self.stacked_widget.setCurrentWidget(self.client_page)

    def show_order_page(self):
        self.last_page = self.stacked_widget.currentWidget()
        self.stacked_widget.setCurrentWidget(self.order_page)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



