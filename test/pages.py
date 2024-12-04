from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Pages.sql.database_model import Base, Orders, clienttab
import logging
from Pages.sql.database_model import WoodProducts
import os
import sqlalchemy as sa

import sys

import os
db_path = os.path.join(".", "wood_production.db") #Relative to the executable
absolute_path = os.path.abspath(db_path)


class Lumber_input(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page, technology_page):
        super().__init__()

        self.setWindowTitle("Add New Lumber")
        engine = create_engine(f"sqlite:///{absolute_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.commercial_page = commercial_page
        self.production_page = production_page
        self.technology_page = technology_page

        label_text = QLabel("Введите вид древесины:")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("вид")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_lumber_to_csv)

        self.time_prod = QLineEdit()
        self.time_prod.setValidator(QIntValidator())
        self.time_prod.setPlaceholderText("время производства")

        self.workshop = QLineEdit()
        self.workshop.setValidator(QIntValidator())
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

    def save_lumber_to_csv(self):
        lumber_type = self.lumber_input.text()
        time_prod = self.time_prod.text()
        workshop = self.workshop.text()
        if lumber_type:
            new_order = WoodProducts(
                WoodProductName=lumber_type,
                ProductionTime=time_prod,
                ProductionShopID=workshop
            )

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")


        else:
            QMessageBox.warning(self, "Ошибка", "Введите вид древесины для сохранения.")


class client(QWidget):
    def __init__(self, navigate_back, commercial_page):
        super().__init__()

        self.setWindowTitle("Add New client")
        engine = create_engine(f"sqlite:///{absolute_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.commercial_page = commercial_page

        label_text = QLabel("Имя клиента")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("Имя клиента")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_client_to_csv)

        self.line_edit_int = QLineEdit()
        self.line_edit_int.setPlaceholderText("Информация")

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.line_edit_int)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_client_to_csv(self):
        client_name = self.lumber_input.text()
        info = self.line_edit_int.text()
        if client_name:
            new_order = clienttab(
                ClientName=client_name,
                ClientInfo=info,
            )

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите имя для сохранения")










