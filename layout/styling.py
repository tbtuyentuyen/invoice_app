""" Styling Module """


class Style():
    """ Style class """
    def __get_style(self, name):
        if name == 'QPushButton': # pylint: disable=R1705
            return """
                QPushButton#common_button {
                    background-color: #0F828C; /* Green */
                    color: white;
                    border-radius: 5px;
                    padding: 15px 15px;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }
                QPushButton#common_button:hover {
                    background-color: #78B9B5;
                }
                QPushButton#common_button:pressed {
                    background-color: #065084;
                }
                QPushButton#expand_toggle {
                    border: none;
                    padding: 6px;
                }
                QPushButton#expand_toggle:checked {
                    border: none;
                }
            """
        elif name == 'QLabel':
            return """
                QLabel#normal_label {
                    color: black;
                    font-size: 17px;
                    font-weight: 500;
                    font-family: 'Segoe UI';
                }
                QLabel#title_label {
                    color: black;
                    font-size: 20px;
                    font-weight: 600;
                    font-family: 'Segoe UI';
                }
                QLabel#visible_error_label {
                    color: #dc3545;
                    font-size: 13px;
                }
                
                QLabel#invisible_error_label {
                    color: transparent;
                    font-size: 13px;
                }
            """
        elif name == 'QCustomTableWidget':
            return """
                QTableWidget {
                    background-color: #EAEFEF;
                    border: 1px solid #320A6B;
                    color: #333446;
                    selection-background-color: #4181C0;
                    selection-color: #FFF;
                    font-size: 16px;
                }

                QTableWidget::item {
                    padding: 5px;
                }

                QTableWidget::item:selected {
                    background-color: #EAEFEF;
                    color: #333446;
                }

                QHeaderView::section {
                    background-color: #4F959D;
                    color: white;
                    border-style: none;
                    font-family: 'Segoe UI';
                    font-weight: 500;
                    font-size: 18px;
                    padding: 5px;
                }
            """
        elif name in ['QLineEdit', 'QMoneyLineEdit']:
            return """
                QLineEdit {
                    background-color: #EAEFEF;
                    color: #320A6B;
                    font-family: 'Segoe UI';
                    font-size: 16px;
                    border: 1px solid #5c6370;
                    padding: 7px;
                }
                QLineEdit::selection {
                    background-color: #61afef;
                    color: #ffffff;
                }
                
                QLineEdit#customer_input {
                    border: none;
                    border-bottom: 1px solid #aaa;
                }
                
                QLineEdit#total_input {
                    font-weight: bold;
                    font-size: 20px;
                }
                QLineEdit#error_input {
                    border: 1px solid #dc3545;
                }
            """
        elif name == "QFrame":
            return """
                QFrame#top_frame {
                    border: 1px solid #666;
                    border-radius: 10px;
                }
            """
        else:
            raise TypeError(f"[ERROR] Invalid class name {name}!")

    def set_style(self, obj):
        """ Set style sheet """
        obj_name = obj.__class__.__name__
        style = self.__get_style(obj_name)
        obj.setStyleSheet(style)
