from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_phone_number(value):

    pattern = r"^09(1[0-9]|3[1-9]|2[1-9])[0-9]{7}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number.")


def validate_birth_date(value):
    if value <= timezone.now().date():
        raise ValidationError("Enter a valid birth date")
