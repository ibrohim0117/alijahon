import re, requests


def validate_phone_number(phone_number):
    pattern = r'^\+998\d{9}$|^\d{9}$'
    match = re.match(pattern, phone_number)
    if match:
        return True
    else:
        return False

# print(validate_phone_number('+998995882742'))
