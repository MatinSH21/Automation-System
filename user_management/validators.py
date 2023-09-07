from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):

    pattern = r"^09(1[0-9]|3[1-9]|2[1-9])[0-9]{7}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number.")
