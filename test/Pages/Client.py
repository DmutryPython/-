from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from .sql.database_model import Base, Orders, clienttab
from .functions import table_input




class Client(QWidget):
    def __init__(self, navigate_back, commercial_page):
        super().__init__()

        tab = table_input()
        self.session = tab.session

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
