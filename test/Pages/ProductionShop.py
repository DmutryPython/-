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
from .sql.database_model import ProductionShops
import os
import sqlalchemy as sa


db_path = os.path.join("Pages", "sql", "wood_production.db")
absolute_path = os.path.abspath(db_path)
from .functions import table_input


class ProductionShop(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        tab = table_input()
        self.session = tab.session

        self.shop_input = QLineEdit()
        self.shop_input.setPlaceholderText("наименование цеха")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_shop)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(self.shop_input)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_shop(self):
        try:
            shop = self.shop_input.text()
            if shop:
                new_order = ProductionShops(
                    ShopName=shop
                )

                self.session.add(new_order)
                self.session.commit()
                QMessageBox.information(self, "Success", "Order added successfully!")
            else:
                QMessageBox.warning(self, "Ошибка", "Введите наименование цеха")
        except sa.exc.IntegrityError as e:
            QMessageBox.warning(self, "Ошибка", "Ошибка: Значение уже существует.")