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

def edit_reader(request, reader_id):
    if request.method == "POST":
        reader = Reader.objects.get(id=reader_id)
        reader.reader_name = request.POST['reader_name']
        reader.reader_contact = request.POST['reader_contact']
        reader.reference_id = request.POST['reference_id']
        reader.reader_department = request.POST['reader_department']
        reader.save()
        return redirect('/readers')
    else:
        reader = Reader.objects.get(id=reader_id)
        return render(request, 'readers.html', context={
            'current_tab': 'readers',
            'edit_reader': reader,
            'readers': Reader.objects.all()
        })

def delete_reader(request, reader_id):
    reader = Reader.objects.get(id=reader_id)
    reader.delete()
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
        allowed_days = int(request.POST['allowed_days'])
        reader = Reader.objects.get(id=reader_id)
        book = Book.objects.get(id=book_id)
        if book.available:
            IssuedBook.objects.create(
                reader=reader,
                book=book,
                allowed_days=allowed_days
            )
            book.available = False
            book.save()
        return redirect('issue_book')

    readers = Reader.objects.filter(active=True)
    books = Book.objects.filter(available=True)
    return render(request, 'issue_book.html', {
        'readers': readers, 
        'books': books, 
        'current_tab': 'issue_book'
    })

from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import messages

def return_book(request):
    if request.method == "POST":
        issued_book_id = request.POST['issued_book_id']
        issued = IssuedBook.objects.get(id=issued_book_id)
        
        # Calculate final fine amount before returning
        fine_amount = issued.get_fine_amount()
        
        issued.return_date = localtime(timezone.now()).date()
        issued.save()

        # Mark book as available again
        book = issued.book
        book.available = True
        book.save()

        # Show success message with fine amount if any
        if fine_amount > 0:
            messages.warning(request, f'Book returned successfully. Fine amount: ₹{fine_amount}')
        else:
            messages.success(request, 'Book returned successfully')

        return redirect('return_book')

    # Get unreturned books and sort them by days remaining
    unreturned_books = IssuedBook.objects.filter(return_date=None)
    # Sort unreturned books by days remaining (ascending)
    unreturned_books = sorted(unreturned_books, key=lambda x: x.get_days_remaining())
    
    # Get returned books sorted by return date (most recent first)
    returned_books = IssuedBook.objects.filter(return_date__isnull=False).order_by('-return_date')
    
    return render(request, 'returns.html', {
        'unreturned_books': unreturned_books,
        'returned_books': returned_books,
        'current_tab': 'return_book'
    })
