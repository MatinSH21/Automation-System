from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_due_date(value):
    if value <= timezone.now().date():
        raise ValidationError("Enter a valid due date")
