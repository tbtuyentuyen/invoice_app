""" Event Module """


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent

    def on_add_button_clicked(self):
        """ Event press add button"""
        data = self.parent.input_layout.get_data()
        status = self.parent.input_layout.validate_all_data(data)
        if status is True:
            self.parent.table_layout.add_row_to_table(data)
            self.parent.input_layout.clear_all_data_input_field()
