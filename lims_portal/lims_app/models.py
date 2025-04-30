from django.db import models

# Create your models here.
class Reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=10)
    reader_department = models.CharField(max_length=100)
    active= models.BooleanField(default=True)


    #new
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

    def __str__(self):
        return f"{self.reader.reader_name} - {self.book.book_name}"

return_date = models.DateTimeField(null=True, blank=True)  # Update this line
