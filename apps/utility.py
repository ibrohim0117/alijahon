import re, requests

from django.db.models import Manager



def validate_phone_number(phone_number):
    pattern = r'^\+998\d{9}$|^\d{9}$'
    match = re.match(pattern, phone_number)
    if match:
        return True
    else:
        return False

# print(validate_phone_number('+998995882742'))

import math
a = int(input('a = '))
b = int(input('b = '))
c = int(input('c = '))
p = a + b + b
print('Uchburchak peremetiri ', p)
print('Uchburchak peremetiri ', math.sqrt(p/2 * (p/2-a) + (p/2-c) + (p/2-b)))



