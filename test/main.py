from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from Pages.Client import Client
from Pages.Lumber import Lumber
from Pages.Order import Order
from Pages.PreparationTasks import PreparationTasks
from Pages.ProductionTask import ProductionTask
from Pages.Commercial import CommercialPage
from Pages.home import MainPage
from Pages.Production import ProductionPage
from Pages.Technology import TechnologyPage
import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox


def my_excepthook(exc_type, exc_value, exc_traceback):
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception:\n{tb_str}")  # Print to console
    QMessageBox.critical(None, "Critical Error",
                         f"An unexpected error occurred. Please contact support.")  # Show to user
    sys.exit(1)  # Exit the application


sys.excepthook = my_excepthook


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
        self.technology_page = TechnologyPage(self.show_lumber_input_page, self.show_page, self.show_PreparationTasks_page, self.show_main_page)
        self.lumber_input_page = Lumber(self.show_last_page, self.commercial_page, self.production_page,
                                              self.technology_page)
        self.client_page = Client(self.show_last_page, self.commercial_page)
        self.productionTask_page = ProductionTask(self.show_last_page)
        self.order_page = Order(self.show_last_page)
        self.PreparationTasks_page = PreparationTasks(self.show_last_page)

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.commercial_page)
        self.stacked_widget.addWidget(self.production_page)
        self.stacked_widget.addWidget(self.technology_page)
        self.stacked_widget.addWidget(self.lumber_input_page)
        self.stacked_widget.addWidget(self.client_page)
        self.stacked_widget.addWidget(self.order_page)
        self.stacked_widget.addWidget(self.productionTask_page)
        self.stacked_widget.addWidget(self.PreparationTasks_page)

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

    def show_page(self):
        self.last_page = self.stacked_widget.currentWidget()
        self.stacked_widget.setCurrentWidget(self.productionTask_page)

    def show_PreparationTasks_page(self):
        self.last_page = self.stacked_widget.currentWidget()
        self.stacked_widget.setCurrentWidget(self.PreparationTasks_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
