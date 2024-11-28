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
        self.wood_product_types = self.session.execute(select(column('WoodProductName')).
                                                select_from(table('wood_products'))).scalars().all()
        self.wood_product_type.addItems(self.wood_product_types)

        self.quantity = QLineEdit(self)
        self.quantity.setValidator(QIntValidator())
        self.quantity.setPlaceholderText("Количество")

        self.workshop = QComboBox(self)
        self.shopname = self.session.execute(select(column('ShopName')).
                                                       select_from(table('production_shops'))).scalars().all()
        self.workshop.addItems(self.shopname)

        self.order_id = QComboBox(self)
        self.orders = self.session.execute(select(column('OrderID')).
                                             select_from(table('orders'))).scalars().all()
        self.order_id.addItems(self.orders)

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
        layout.addWidget(QLabel("Номер заказа:"))
        layout.addWidget(self.order_id)
        layout.addWidget(QLabel("Вид лесопродукции:"))
        layout.addWidget(self.wood_product_type)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.quantity)
        layout.addWidget(QLabel("Цех:"))
        layout.addWidget(self.workshop)
        layout.addWidget(QLabel("Дополнительная информация:"))
        layout.addWidget(self.additional_info)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def update_orderid(self):
        index = self.layout().indexOf(self.order_id)
        self.layout().removeWidget(self.order_id)
        self.order_id.deleteLater()
        self.order_id = QComboBox(self)
        try:
            orders = self.session.execute(select(column('OrderID')).select_from(table('orders'))).scalars()
            self.layout().insertWidget(index, self.order_id)
            self.order_id.addItems(orders)
            self.layout().update()
            self.update()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def update_wood_product_types(self):
        index = self.layout().indexOf(self.wood_product_type)
        self.layout().removeWidget(self.wood_product_type)
        self.wood_product_type.deleteLater()
        self.wood_product_type = QComboBox(self)
        try:
            wood_product_types = self.session.execute(select(column('WoodProductName')).select_from(table('wood_products'))).scalars()
            self.layout().insertWidget(index, self.wood_product_type)
            self.wood_product_type.addItems(wood_product_types)
            self.layout().update()
            self.update()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")  # Выводим сообщение об ошибке в консоль

    def update_workshops(self):
        index = self.layout().indexOf(self.workshop)
        self.layout().removeWidget(self.workshop)
        self.workshop.deleteLater()
        self.workshop = QComboBox(self)
        workshops = self.session.execute(select(column('ShopName')).select_from(table('production_shops'))).scalars()
        self.workshop.addItems(workshops)
        self.layout().insertWidget(index, self.workshop)
        self.layout().update()
        self.update()


    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_orderid()
        self.update_workshops()
        self.update_wood_product_types()
        super().showEvent(event)
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

