def update_lumber_list(self):
    self.load_csv_lumber("resources/lumber_types.csv", self.table)


def update_name_list(self):
    self.load_csv_client("resources/name.csv", self.table_name)


def update_client_list(self):
    self.load_csv_order("resources/client.csv", self.table_order)