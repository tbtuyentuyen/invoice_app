""" Common Module """


from enum import Enum

class RegexPatterns(Enum): # pylint:disable=R0903
    """ Pattern class for regex """
    NAME = r"^[a-zA-Z0-9àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ,\s]*$"
    QUANTITY = r"^[0-9\s]*$"
    PRICE = r"^[0-9\s]*$"
    TYPE = r"^[a-zA-Z0-9àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ,\s]*$"

class ErrorMessage(Enum): # pylint:disable=R0903
    """ Error Message for raise exception """
    NAME_INPUT = "Tên không được chứa ký tự đặc biệt"
    QUANTITY_INPUT = "Vui lòng nhập số lượng hợp lệ (chỉ dùng số)."
    PRICE_INPUT = "Vui lòng nhập giá hợp lệ (chỉ dùng số)"
    TYPE_INPUT = "Loại không được chứa số hoặc ký tự đặc biệt."
    NONE_INPUT = "Vui lòng nhập thông tin vào trường bên trên."

class TableAttribute(Enum): # pylint:disable=R0903
    """ Table Attribute class """
    NAME = 'Tên mặt hàng'
    QUANTITY = 'Số lượng'
    TYPE = 'Loại'
    PRICE = 'Giá'

    @classmethod
    def list(cls):
        """ return variable list """
        return list(map(lambda c: c.value, cls))

class InputMode(Enum):
    """ Input Mode class """
    ADD = "Add"
    EDIT = "Edit"
