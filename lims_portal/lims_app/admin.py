from _csv import Writer

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(IssuedBook)