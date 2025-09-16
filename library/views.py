from django.shortcuts import redirect, render
from library.models import EBooksModel
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from .models import Book

from django.shortcuts import render
from .models import Transaction





from django.utils import timezone

from django.contrib.auth.models import User
from datetime import timedelta

# Create your views here.









def Registers(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first--name']
        lastName = request.POST['last--name']

        # Check if a user with the same username already exists
        if User.objects.filter(username=email).exists():
            messages.info(request,'User already exists')
            return render(request, 'register.html')   # i have to handle this error in frontend
        else:
            # Create a new user
            register = User.objects.create_user(username=email,password=password,first_name=firstName,last_name=lastName)
            # No need to call save() after create_user(), as it's already saved
            return redirect('login')
    else:
        return render(request, 'library/register.html')
    


from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Django default User uses username, not email.
        # If you’re using email for login, replace username with email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("books")  # or use LOGIN_REDIRECT_URL
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "library/login.html")

def home(request):
   return render(request, 'library/home.html')



def logout(request):
    auth.logout(request)
    return redirect('home')







# ---------------------------------------- Other Views (Reports, Transactions, Books) ------------------------------- #

# ------------------------books-----------------------



# Add Book
@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        category = request.POST['category']
        pages = request.POST['pages']
        total_copies = int(request.POST['total_copies'])
        book = Book.objects.create(
            title=title,
            author=author,
            category=category,
            pages=pages,
            total_copies=total_copies,
            available_copies=total_copies
        )
        messages.success(request, f'Book "{title}" added successfully.')
        return redirect('book_list')
    else:
        return render(request, 'library/add_book.html')




# List / Search Books

def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    category = request.GET.get('category')
    if category:
        books = books.filter(category__iexact=category)
    author = request.GET.get('author')
    if author:
        books = books.filter(author__icontains=author)
    available = request.GET.get('available')
    if available == '1':
        books = books.filter(available_copies__gt=0)
    return render(request, 'library/book_list.html', {'books': books})










# ------------------------reports-----------------------


# Popular Books



# # User Borrowing History
# def user_history(request, user_id):
#     transactions = Transaction.objects.filter(user_id=user_id)
#     return render(request, 'library/user_history.html', {'transactions': transactions})






# ------------------------transactions-----------------------



# Borrow Book
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        user = request.user
        if book.available_copies > 0:
            due_days = int(request.POST.get('due_days', 7))  # default 7 days
            due_date = timezone.now().date() + timedelta(days=due_days)
            Transaction.objects.create(
                user=user,
                book=book,
                borrowed_date=timezone.now().date(),
                due_date=due_date,
                status='borrowed'
            )
            book.available_copies -= 1
            book.save()
            messages.success(request, f'Book "{book.title}" borrowed successfully.')
        else:
            messages.error(request, f'Book "{book.title}" is not available.')
        return redirect('book_list')
    else:
        return render(request, 'library/borrow_book.html', {'book': book})


# Return Book
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        transaction.status = 'returned'
        transaction.returned_date = timezone.now().date()
        # Optional: fine calculation
        if transaction.returned_date > transaction.due_date:
            days_late = (transaction.returned_date - transaction.due_date).days
            transaction.fine = days_late * 5  # e.g., ₹5 per day
        transaction.save()
        book = transaction.book
        book.available_copies += 1
        book.save()
        messages.success(request, f'Book "{book.title}" returned successfully.')
        return redirect('my_borrowed_books')
    else:
        return render(request, 'library/return_book.html', {'transaction': transaction})


# List User Borrowed Books
def my_borrowed_books(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user, status='borrowed')
    return render(request, 'library/my_borrowed_books.html', {'transactions': transactions})


