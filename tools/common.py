""" Common Module """


from enum import Enum, auto

class RegexPatterns(Enum): # pylint:disable=R0903
    """ Pattern class for regex """
    VIETNAMESE = r"a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"

    ONLY_LETTERS = rf"^[{VIETNAMESE}\s]*$"
    ONLY_DIGITS = r"^[0-9\s]*$"
    LETTERS_AND_DIGITS = rf"^[{VIETNAMESE}0-9\s]*$"
    LETTERS_DIGITS_SPECIAL = rf"^[{VIETNAMESE}0-9,\.\-_\/\s]*$"
    PHONE_NUMBER = r"^0\d{9}$"

class ErrorMessage(Enum):
    """ Generic error messages for validation """
    ONLY_NUMBER = "Trường này chỉ được chứa số."
    ONLY_LETTER = "Trường này chỉ được chứa chữ."
    ONLY_LETTER_AND_NUMBER = "Trường này chỉ được chứa chữ và số."
    INVALID_SPECIAL_CHAR = "Không được chứa ký tự đặc biệt không hợp lệ."
    EMPTY_INPUT = "Vui lòng nhập thông tin vào trường bên trên."
    INVALID_PHONE = "Số điện thoại không hợp lệ"

class TableAttribute(Enum): # pylint:disable=R0903
    """ Table Attribute class """
    NAME = 'Tên'
    QUANTITY = 'Số lượng'
    TYPE = 'Loại'
    PRICE = 'Giá'
    SUM = 'Thành tiền'

    @classmethod
    def list(cls):
        """ return variable list """
        return list(map(lambda c: c.value, cls))

class InputMode(Enum):
    """ Input Mode class """
    ADD = "Add"
    EDIT = "Edit"

class MongoDBStatus(Enum):
    """ MongoDB Status class """
    UNKNOWN = "Chưa xác định"
    CONNECTING = "Đang kết nối.."
    CONNECTED = "Đã kết nối"
    DISCONNECTED = "Đã ngắt kết nối"

class CustomerAttribute(Enum):
    """ Customer Attribute class """
    NAME = "Tên khách hàng"
    COMPANY = "Công ty"
    ADDRESS = "Địa chỉ"
    PHONE_NUMBER = "Số điện thoại"
    TAX_NUMBER = "Mã số thuế"
    PAYMENT_OPTIONS = "Hình thức thanh toán"

class MessageBoxType(Enum):
    """ Message Box Type class """
    INFO = auto()
    QUESTION = auto()
    WARNING = auto()
    ERROR = auto()
