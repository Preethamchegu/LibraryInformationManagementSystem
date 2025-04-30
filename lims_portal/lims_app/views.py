from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render,redirect
# Create your views here.
from .models import *
def home(request):
    return render(request, 'home.html', context={'current_tab':'home'})
def readers(request):
    return render(request, 'readers.html', context={'current_tab':'readers'})
def shopping(request):
    return HttpResponse("welcome to shopping")

def readers_tab(request):
    if request.method == "GET":
        students=Reader.objects.all()
        return render(request,"readers.html",context={"current_tab":"readers","readers":students})
    else:
        query=request.POST['query']
        students=Reader.objects.raw("select * from lims_app_reader where reader_name like '%"+query+"%'")
        return render(request, 'readers.html', context={'current_tab': 'readers', 'readers':students,"query":query})

def save_reader(request):
   reader_item=Reader(reference_id=request.POST['reference_id'],
                      reader_name=request.POST['reader_name'],
                      reader_department=request.POST['reader_department'],
                      reader_contact=request.POST['reader_contact'],
                      active=True)
   reader_item.save()
   return redirect('/readers')
#new
# views.py

def books(request):
    if request.method == "POST":
        book_name = request.POST['book_name']
        author = request.POST['author']
        category = request.POST['category']
        book_id = request.POST['book_id']
        Book.objects.create(book_name=book_name, author=author, category=category, book_id=book_id)
        return redirect('books')

    all_books = Book.objects.all()
    return render(request, 'books.html', {'books': all_books, 'current_tab': 'books'})


def issue_book(request):
    if request.method == "POST":
        reader_id = request.POST['reader_id']
        book_id = request.POST['book_id']
        reader = Reader.objects.get(id=reader_id)
        book = Book.objects.get(id=book_id)
        if book.available:
            IssuedBook.objects.create(reader=reader, book=book)
            book.available = False
            book.save()
        return redirect('issue_book')

    readers = Reader.objects.filter(active=True)
    books = Book.objects.filter(available=True)
    return render(request, 'issue_book.html', {'readers': readers, 'books': books, 'current_tab': 'issue_book'})

from django.utils import timezone
from django.utils.timezone import localtime

def return_book(request):
    if request.method == "POST":
        issued_book_id = request.POST['issued_book_id']
        issued = IssuedBook.objects.get(id=issued_book_id)
        issued.return_date = localtime(timezone.now())
        issued.save()

        # Mark book as available again
        book = issued.book
        book.available = True
        book.save()

        return redirect('return_book')

    issued_books = IssuedBook.objects.all().order_by('-issue_date')
    return render(request, 'returns.html', {'issued_books': issued_books, 'current_tab':'return_book'})
