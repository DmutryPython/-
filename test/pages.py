from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv

class Lumber_input(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page, technology_page):
        super().__init__()
        layout = QVBoxLayout()

        self.commercial_page = commercial_page
        self.production_page = production_page
        self.technology_page = technology_page

        # Поле для ввода вида древесины
        label_text = QLabel("Введите вид древесины:")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("вид")

        # Кнопка сохранения в CSV
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_lumber_to_csv)

        self.line_edit_int = QLineEdit()
        int_validator = QIntValidator()
        self.line_edit_int.setValidator(int_validator)
        self.line_edit_int.setPlaceholderText("цена")

        # Кнопка возврата назад
        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Добавляем виджеты в компоновку
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.line_edit_int)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        # Устанавливаем компоновку для страницы
        self.setLayout(layout)

    def save_lumber_to_csv(self):
        # Получаем текст из поля и проверяем, не пустой ли он
        lumber_type = self.lumber_input.text()
        price = self.line_edit_int.text()
        if lumber_type:
            # Сохраняем данные в CSV-файл
            with open("resources/lumber_types.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([lumber_type, price])

            # Очищаем поле ввода
            self.lumber_input.clear()
            self.line_edit_int.clear()

            # Показываем сообщение об успешном сохранении
            QMessageBox.information(self, "Успех", "Вид древесины успешно сохранен!")

            self.commercial_page.update_lumber_list()
            self.production_page.update_lumber_list()
            self.technology_page.update_lumber_list()
        else:
            # Показываем предупреждение, если поле пустое
            QMessageBox.warning(self, "Ошибка", "Введите вид древесины для сохранения.")


class client(QWidget):
    def __init__(self, navigate_back, commercial_page):
        super().__init__()
        layout = QVBoxLayout()

        self.commercial_page = commercial_page

        # Поля для ввода
        label_text = QLabel("Имя клиента")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("Имя клиента")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_client_to_csv)

        self.line_edit_int = QLineEdit()
        self.line_edit_int.setPlaceholderText("Информация")

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

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
            with open("resources/name.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([client_name, info])

            self.lumber_input.clear()
            self.line_edit_int.clear()
            QMessageBox.information(self, "Успех", "Клиент добавлен")

            # Обновляем таблицу клиентов
            self.commercial_page.update_name_list()
        else:
            QMessageBox.warning(self, "Ошибка", "Введите имя для сохранения")


class order(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page):
        super().__init__()
        layout = QVBoxLayout()

        self.commercial_page = commercial_page
        self.production_page = production_page


        self.combo_box = QComboBox(self)
        self.status_list = ['Черновик', 'Согласован клиентом', 'Принят в производство', 'Выполнен']
        self.combo_box.addItems(self.status_list)


        self.date_order = QDateEdit(self)
        self.date_order.setDate(QDate.currentDate())

        self.deadline = QDateEdit(self)
        self.deadline.setDate(QDate.currentDate())

        self.info_client = QLineEdit()
        self.info_client.setPlaceholderText("Информация о клиенте")

        self.lumber = QLineEdit()
        self.lumber.setPlaceholderText("пиломатериал")

        self.quantity_lumber = QLineEdit()
        self.quantity_lumber.setValidator(QIntValidator())
        self.quantity_lumber.setPlaceholderText("кол-во пиломатериала")

        self.note = QLineEdit()
        self.note.setPlaceholderText("пометка")



        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_order_to_csv)



        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout.addWidget(QLabel("дата заказа"))
        layout.addWidget(self.date_order)
        layout.addWidget(QLabel("срок заказа"))
        layout.addWidget(self.deadline)
        layout.addWidget(self.info_client)
        layout.addWidget(self.lumber)
        layout.addWidget(self.quantity_lumber)
        layout.addWidget(self.note)
        layout.addWidget(self.combo_box)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)


    def save_order_to_csv(self):
        status = self.combo_box.currentText()
        if status != 'Черновик':
            if (self.date_order.dateTime() and self.deadline.dateTime() and self.info_client.text() and
                    self.quantity_lumber.text() and self.lumber.text()):

                if self.date_order.dateTime() < self.deadline.dateTime():
                    with open("resources/client.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([self.date_order.text(), self.deadline.text(), self.info_client.text(),
                                         self.lumber.text(), self.quantity_lumber.text(),
                                         self.note.text(), status])

                    self.info_client.clear()
                    self.lumber.clear()
                    self.quantity_lumber.clear()
                    self.note.clear()
                    QMessageBox.information(self, "Успех", "Заказ добавлен")

                    # Обновляем таблицу клиентов
                    self.commercial_page.update_client_list()
                    self.production_page.update_client_list()
                else:
                    QMessageBox.warning(self, "Ошибка", "Дата введенна некоректно")
            else:
                QMessageBox.warning(self, "Ошибка", "Введены не все обязательные данные ")
        else:
            if self.date_order.dateTime() < self.deadline.dateTime():
                with open("resources/client.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([self.date_order.text(), self.deadline.text(), self.info_client.text(),
                                     self.lumber.text(), self.quantity_lumber.text(), self.note.text(), status])

                self.info_client.clear()
                self.lumber.clear()
                self.quantity_lumber.clear()
                self.note.clear()
                QMessageBox.information(self, "Успех", "Заказ добавлен")

                self.commercial_page.update_client_list()
                self.production_page.update_client_list()
            else:
                QMessageBox.warning(self, "Ошибка", "Дата введенна некоректно")




