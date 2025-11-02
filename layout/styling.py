""" Styling Module """


class Style():
    """ Style class """
    def __get_style(self, name):
        if name == 'QPushButton': # pylint: disable=R1705
            return """
                QPushButton {
                    background-color: #0F828C; /* Green */
                    color: white;
                    border-radius: 5px;
                    padding: 15px 15px;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: "Consolas";
                }
                QPushButton:hover {
                    background-color: #78B9B5;
                }
                QPushButton:pressed {
                    background-color: #065084;
                }
            """
        elif name == 'QLabel':
            return """
                QLabel {
                    color: black;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: "Consolas", "Monaco", monospace;
                }
            """
        elif name == 'QTableWidget':
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
                    background-color: #E6E6E6;
                    color: #333446;
                }

                QHeaderView::section {
                    background-color: #4F959D;
                    color: white;
                    border-style: none;
                    font-family: "Consolas", "Monaco", monospace;
                    font-size: 18px;
                    padding: 5px;
                }

            """
        elif name == 'QPlainTextEdit':
            return """
                QPlainTextEdit {
                    background-color: #EAEFEF;
                    color: #320A6B;
                    font-family: "Consolas", "Monaco", monospace;
                    font-size: 16px;
                    border: 1px solid #5c6370;
                    padding: 7px;
                }
                QPlainTextEdit::selection {
                    background-color: #61afef; /* Selection background */
                    color: #ffffff; /* Selection text color */
                }
            """
        else:
            raise TypeError(f"[ERROR] Invalid class name {name}!")


    def set_style(self, obj):
        """ Set style sheet """
        obj_name = obj.__class__.__name__
        style = self.__get_style(obj_name)
        obj.setStyleSheet(style)

    def set_style_error_label_visible(self, obj): # TODO: gom ham
        """ Set style error label when visible """
        obj.setStyleSheet("""
            color: #dc3545;
            font-size: 13px;
        """)

    def set_style_error_label_invisible(self, obj): # TODO: gom ham
        """ Set style error label when invisible """
        obj.setStyleSheet("""
            color: transparent;
            font-size: 13px;
        """)

    def set_plain_text_edit_error(self, obj):
        """ Set plain text edit to red """
        obj.setStyleSheet("""
            QPlainTextEdit {
                border: 1px solid #dc3545;
            }
        """)
