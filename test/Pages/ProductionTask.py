from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator # Здесь импортируется QIntValidator
from sqlalchemy import *
from sqlalchemy.orm import *
import logging
from .functions import table_input, update_tables
from .sql.database_model import ProductionTasks, Orders, WoodProducts



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

        self.order_id = QComboBox(self)
        self.orders = list(map(str, self.session.execute(select(column('OrderID')).
                                             select_from(table('orders'))).scalars().all()))
        self.order_id.addItems(self.orders)
        self.quantity = 0
        self.wood_product_type = ''
        self.work_shop = ''

        self.quantity_label = QLabel("Количество: ")
        self.wood_product_type_label = QLabel("Тип дерева: ")
        self.workshop = QLabel("Цех: ")

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
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.wood_product_type_label)
        layout.addWidget(self.workshop)
        layout.addWidget(QLabel("Дополнительная информация:"))
        layout.addWidget(self.additional_info)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.order_id.currentTextChanged.connect(self.box_update)
        self.box_update(self.order_id.currentText())

    def box_update(self, text):
        try:
            order_id = int(text)
            order = self.session.get(Orders, order_id)
            shopName = order.WoodProductName
            print(shopName)
            workshop = self.session.get(WoodProducts, shopName)
            print(workshop.ProductionShopName)

            if order:
                self.quantity = order.WoodProductQuantity
                self.wood_product_type = order.WoodProductName
                quantity_text = f"Количество: {self.quantity}"
                wood_type_text = f"Тип дерева: {self.wood_product_type}"
            else:
                quantity_text = "Количество: "
                wood_type_text = "Тип дерева: "
            if workshop:
                self.work_shop = workshop.ProductionShopName
                work_shop_text = f"Цех:  {self.work_shop}"
            else:
                work_shop_text = "Цех: "
            self.quantity_label.setText(quantity_text)
            self.wood_product_type_label.setText(wood_type_text)
            self.workshop.setText(work_shop_text)
            self.layout().update()
            self.update()

        except ValueError:
            self.quantity_label.setText("Количество: ")
            self.wood_product_type_label.setText("Тип дерева: ")
            self.workshop.setText("Цех: ")



    def update_orderid(self):
        update_tables(self, 'orders', 'OrderID', self.order_id)


    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_orderid()
        # self.update_wood_product_types()
        super().showEvent(event)

    def add_task(self):
            try:
                date_registration = self.date_registration.date().toPyDate()
                date_start = self.date_start.date().toPyDate()
                wood_product_type = self.wood_product_type
                quantity = int(self.quantity)
                workshop = self.work_shop
                additional_info = self.additional_info.text()
                order_id = self.order_id.currentText()

                # Здесь вам нужно будет добавить логику для получения ID из названий (wood_product_type, workshop)
                # и создать объект ProductionTasks с соответствующими полями.  Замените на ваши реальные поля и таблицы:


                new_task = ProductionTasks(TaskRegistrationDate=date_registration,
                                           ProductionStartDate=date_start,
                                           WoodProductName=wood_product_type,
                                           WoodProductsQuantity=quantity,
                                           Shop=workshop,
                                           AdditionalTaskInformation=additional_info,
                                           OrderID=order_id
                                           )

                self.session.add(new_task)
                self.session.commit()
                QMessageBox.information(self, "Success", "Task added successfully!")

            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
                logging.exception(f"An error occurred: {e}")

