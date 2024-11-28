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
from .sql.database_model import WoodProducts
import os
import sqlalchemy as sa


db_path = os.path.join("Pages", "sql", "wood_production.db")
absolute_path = os.path.abspath(db_path)
from .functions import table_input


class Lumber(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page, technology_page):
        super().__init__()

        tab = table_input()
        self.session = tab.session

        self.commercial_page = commercial_page
        self.production_page = production_page
        self.technology_page = technology_page

        label_text = QLabel("Введите вид древесины:")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("вид")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_lumber)

        self.time_prod = QLineEdit()
        self.time_prod.setValidator(QIntValidator())
        self.time_prod.setPlaceholderText("время производства")

        self.workshop = QLineEdit()
        self.workshop.setPlaceholderText("workshop")

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.time_prod)
        layout.addWidget(self.workshop)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_lumber(self):
        try:
            lumber_type = self.lumber_input.text()
            time_prod = self.time_prod.text()
            workshop = self.workshop.text()
            if lumber_type:
                new_order = WoodProducts(
                    WoodProductName=lumber_type,
                    ProductionTime=time_prod,
                    ProductionShopName=workshop
                )

                self.session.add(new_order)
                self.session.commit()
                QMessageBox.information(self, "Success", "Order added successfully!")


            else:
                QMessageBox.warning(self, "Ошибка", "Введите вид древесины для сохранения.")
        except sa.exc.IntegrityError as e:
            QMessageBox.warning(self, "Ошибка", "Ошибка: Значение уже существует.")