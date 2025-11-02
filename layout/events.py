""" Event Module """


from common import VerifyType


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent

    def on_add_button_clicked(self):
        """ Event press add button"""
        data = self.parent.input_layout.validate_all_data()
        result = self.parent.table_layout.add_row_to_table(data)
        if result is True:
            self.parent.input_layout.clear_all_data_input_field()

    def on_name_input_change(self):
        """ Event input data to name input """
        self.parent.input_layout.validate_input(VerifyType.NAME)

    def on_quantity_input_change(self):
        """ Event input data to quantity input """
        self.parent.input_layout.validate_input(VerifyType.QUANTITY)

    def on_price_input_change(self):
        """ Event input data to price input """
        self.parent.input_layout.validate_input(VerifyType.PRICE)

    def on_type_input_change(self):
        """ Event input data to type input """
        self.parent.input_layout.validate_input(VerifyType.TYPE)
