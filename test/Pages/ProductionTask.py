from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator # Здесь импортируется QIntValidator
from sqlalchemy import *
from sqlalchemy.orm import *
import logging
from .functions import table_input
from .sql.database_model import ProductionTasks



class ProductionTask(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        layout = QVBoxLayout()
        tab = table_input()
        self.session = tab.session

        self.setWindowTitle("Добавить задание на производство")

        self.date_registration = QDateEdit(self)
        self.date_registration.setDate(QDate.currentDate())
        self.date_start = QDateEdit(self)
        self.date_start.setDate(QDate.currentDate())

        self.wood_product_type = QComboBox(self)
        self.update_wood_product_types()

        self.quantity = QLineEdit(self)
        self.quantity.setValidator(QIntValidator())
        self.quantity.setPlaceholderText("Количество")

        self.workshop = QComboBox(self)
        self.update_workshops()

        self.additional_info = QLineEdit(self)
        self.additional_info.setPlaceholderText("Дополнительная информация")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.add_task)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout.addWidget(QLabel("Дата регистрации:"))
        layout.addWidget(self.date_registration)
        layout.addWidget(QLabel("Дата начала:"))
        layout.addWidget(self.date_start)
        layout.addWidget(QLabel("Вид лесопродукции:"))
        layout.addWidget(self.wood_product_type)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.quantity)
        layout.addWidget(QLabel("Цех:"))
        layout.addWidget(self.workshop)
        layout.addWidget(QLabel("Дополнительная информация:"))
        layout.addWidget(self.additional_info)
        layout.addWidget(save_button)
        self.setLayout(layout)
        layout.addWidget(back_button)

    def update_wood_product_types(self):
        if self.wood_product_type:
            self.layout().removeWidget(self.wood_product_type)
            self.wood_product_type.deleteLater()
        self.wood_product_type = QComboBox(self)
        try:
            wood_product_types = list(self.session.execute(select(column('WoodProductName')).select_from(table('wood_products'))).scalars())
            if wood_product_types:  # Проверяем, не пустой ли список
                self.wood_product_type.addItems(wood_product_types)
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")  # Выводим сообщение об ошибке в консоль

    def update_workshops(self):
        if self.workshop:
            self.layout().removeWidget(self.workshop)
            self.workshop.deleteLater()
        self.workshop = QComboBox(self)
        try:
            workshops = list(self.session.execute(select(column('WorkshopName')).select_from(table('workshops'))).scalars())
            if workshops: # Проверяем, не пустой ли список
                self.workshop.addItems(workshops)
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}") # Выводим сообщение об ошибке в консоль

    def add_task(self):
        try:
            date_registration = self.date_registration.date().toPyDate()
            date_start = self.date_start.date().toPyDate()
            wood_product_type = self.wood_product_type.currentText()
            quantity = self.quantity.text()
            workshop = self.workshop.currentText()
            additional_info = self.additional_info.text()

            # Здесь вам нужно будет добавить логику для получения ID из названий (wood_product_type, workshop)
            # и создать объект ProductionTasks с соответствующими полями.  Замените на ваши реальные поля и таблицы:
            new_task = ProductionTasks(OrderRegistrationDate=date_registration,
                                       OrderStartDate=date_start,
                                       WoodProductID=wood_product_type,  # Нужно получить ID
                                       WoodProductQuantity=quantity,
                                       WorkshopID=workshop,  # Нужно получить ID
                                       AdditionalOrderInformation=additional_info,
                                       OrderID=self.order_id)

            self.session.add(new_task)
            self.session.commit()
            QMessageBox.information(self, "Success", "Task added successfully!")

        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            logging.exception(f"An error occurred: {e}")

