from .functions import PandasModel, table_input, ConditionalColorDelegate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView

class TechnologyPage(QWidget):
    def __init__(self, navigate_to_lumber_input, productionTask_page, navigate_back):
        super().__init__()

        self.tab = table_input()
        result_lumber = self.tab.result_lumber

        label_description = QLabel("Служба технолога")

        # Кнопка навигации
        button_second_page = QPushButton("Добавить древесину")
        button_second_page.clicked.connect(navigate_to_lumber_input)

        button_productionTask = QPushButton("Добавить задачу")
        button_productionTask.clicked.connect(productionTask_page)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблица
        self.table_lumber = QTableView()
        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        # Добавляем виджеты в компоновку
        layout = QVBoxLayout()
        layout.addWidget(label_description)
        layout.addWidget(button_second_page)
        layout.addWidget(button_productionTask)
        layout.addWidget(back_button)
        layout.addWidget(self.table_lumber)  # Добавляем таблицу на страницу

        self.setLayout(layout)

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        """Обновляет данные в таблицах."""
        self.tab = table_input()
        result_lumber = self.tab.result_lumber

        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)