from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime, date

# Create your models here.
class Reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be a 10-digit number',
            ),
        ]
    )
    reader_department = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

class Book(models.Model):
    book_id = models.CharField(max_length=100, unique=True)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.book_name

class IssuedBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    allowed_days = models.IntegerField(default=15)

    def __str__(self):
        return f"{self.reader.reader_name} - {self.book.book_name}"

    def get_days_remaining(self):
        if self.return_date:
            return 0
        today = date.today()
        days_passed = (today - self.issue_date).days
        remaining = self.allowed_days - days_passed
        return remaining

    def get_fine_amount(self):
        if not self.return_date:
            today = date.today()
            days_passed = (today - self.issue_date).days
            if days_passed > self.allowed_days:
                return (days_passed - self.allowed_days) * 1  # ₹1 per day
        return 0
