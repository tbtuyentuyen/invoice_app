""" Common Module """


class RegexPatterns: # pylint:disable=R0903
    """ Pattern class for regex """
    NAME = r"^[a-zA-Z0-9\s]*$"
    QUANTITY = r"^[0-9\s]*$"
    PRICE = r"^[0-9\s]*$"
    TYPE = r"^[a-zA-Z\s]*$"

class ErrorMessage: # pylint:disable=R0903
    """ Error Message for raise exception """
    NAME_INPUT = "Tên không được chứa ký tự đặc biệt"
    QUANTITY_INPUT = "Vui lòng nhập số lượng hợp lệ (chỉ dùng số)."
    PRICE_INPUT = "Vui lòng nhập giá hợp lệ (chỉ dùng số)"
    TYPE_INPUT = "Loại không được chứa số hoặc ký tự đặc biệt."
    NONE_INPUT = "Vui lòng nhập thông tin vào trường bên trên."

class VerifyType: # pylint:disable=R0903
    """ Verify Type class """
    NAME = 'Name'
    QUANTITY = 'Quantity'
    PRICE = 'Price'
    TYPE = 'Type'
