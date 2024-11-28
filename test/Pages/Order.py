from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .sql.database_model import Base, Orders, clienttab
import logging
import os
import sqlalchemy as sa
from .functions import table_input

class Order(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        tab = table_input()
        self.session = tab.session

        self.setWindowTitle("Add New Order")

        self.combo_box = QComboBox(self)
        self.status_list = ['Черновик', 'Согласован клиентом', 'Принят в производство', 'Выполнен']
        self.combo_box.addItems(self.status_list)

        self.date_order = QDateEdit(self)
        self.date_order.setDate(QDate.currentDate())

        self.deadline = QDateEdit(self)
        self.deadline.setDate(QDate.currentDate())

        self.client = QLineEdit()
        self.client.setPlaceholderText("Информация о клиенте")

        self.lumber = QComboBox(self)
        self.lumber_list = self.session.execute(sa.select(sa.column('WoodProductName')).
                                                select_from(sa.table('wood_products'))).scalars().all()
        self.lumber.addItems(self.lumber_list)

        self.quantity_lumber = QLineEdit()
        self.quantity_lumber.setValidator(QIntValidator())
        self.quantity_lumber.setPlaceholderText("кол-во пиломатериала")

        self.note = QLineEdit()
        self.note.setPlaceholderText("пометка")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.add_order)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("дата заказа"))
        layout.addWidget(self.date_order)
        layout.addWidget(QLabel("срок заказа"))
        layout.addWidget(self.deadline)
        layout.addWidget(self.client)
        layout.addWidget(self.lumber)
        layout.addWidget(self.quantity_lumber)
        layout.addWidget(self.note)
        layout.addWidget(self.combo_box)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def add_order(self):
        try:
            date_order = self.date_order.date().toPyDate()
            deadline = self.deadline.date().toPyDate()
            client = self.client.text()
            lumber = self.lumber.currentText()
            quantity_lumber = self.quantity_lumber.text()
            note = self.note.text()
            status = self.combo_box.currentText()

            if status != 'Черновик':
                if not all([date_order, deadline, client, quantity_lumber, lumber]):
                    QMessageBox.warning(self, "Ошибка", "Введены не все данные")
                    return

            if date_order >= deadline:
                QMessageBox.warning(self, "Ошибка", "Срок заказа должен быть позже даты заказа")
                return


            new_order = Orders(OrderRegistrationDate=date_order,
                               OrderCompletionDate=deadline,
                               ClientName=client,
                               WoodProductName=lumber,  # Use the ID from the database
                               WoodProductQuantity=quantity_lumber,
                               AdditionalOrderInformation=note,
                               OrderStatus=status)

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")


        except exc.SQLAlchemyError as e:
            self.session.rollback()  # Rollback transaction on error
            QMessageBox.critical(self, "Database Error", f"Database error: {e}")
            logging.exception(f"Database error: {e}")  # Log the error for debugging

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            logging.exception(f"An unexpected error occurred: {e}")

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        index = self.layout().indexOf(self.quantity_lumber)  # Находим индекс quantity_lumber
        self.tab = table_input()
        self.session = self.tab.session
        # Удаляем старый ComboBox
        self.layout().removeWidget(self.lumber)
        self.lumber.deleteLater()

        # Создаем новый ComboBox и добавляем его в layout
        self.lumber = QComboBox(self)
        lumber_list = self.session.execute(sa.select(sa.column('WoodProductName')).select_from(sa.table('wood_products'))).scalars().all()
        self.lumber.addItems(lumber_list)
        self.layout().insertWidget(index, self.lumber) # Добавляем в layout

        # Обновляем layout, чтобы изменения отобразились
        self.layout().update()
        self.update()

