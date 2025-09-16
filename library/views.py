from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Book, Transaction


def Registers(request):
    """
    Handle user registration.
    - POST: Create a new user if email is unique.
    - GET: Render registration form.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first--name']
        lastName = request.POST['last--name']

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.info(request, 'User already exists')
            return render(request, 'register.html')  # Frontend should display this error
        else:
            # Create new user
            User.objects.create_user(
                username=email,
                password=password,
                first_name=firstName,
                last_name=lastName
            )
            return redirect('login')
    else:
        return render(request, 'library/register.html')


def Login(request):
    """
    Handle user login.
    - POST: Authenticate credentials and log in.
    - GET: Render login form.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            print('User logged in successfully')
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'library/login.html')
    else:
        return render(request, 'library/login.html')


def logout(request):
    """
    Log out the current user and redirect to home page.
    """
    auth.logout(request)
    return redirect('home')


def home(request):
    """
    Render the home page.
    """
    return render(request, 'library/home.html')


# ===========================
# Book Views
# ===========================

@login_required
def add_book(request):
    """
    Add a new book to the library.
    - POST: Save book data to the database.
    - GET: Render add book form.
    """
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        category = request.POST['category']
        pages = request.POST['pages']
        total_copies = int(request.POST['total_copies'])
        added_by_id = request.user.id   # ID of the user adding the book

        # Create and save book to DB
        Book.objects.create(
            title=title,
            author=author,
            category=category,
            pages=pages,
            total_copies=total_copies,
            available_copies=total_copies,
            added_by_id=added_by_id
        )

        messages.success(request, f'Book "{title}" added successfully.')
        return redirect('book_list')
    else:
        return render(request, 'library/add_book.html')


def book_list(request):
    """
    Display all books in the library.
    Optional search/filter functionality commented out.
    """
    books = Book.objects.all()
    # Example filters (currently commented):
    # query = request.GET.get('q', '')
    # category = request.GET.get('category')
    # author = request.GET.get('author')
    # available = request.GET.get('available')
    return render(request, 'library/book_list.html', {'books': books})


# ===========================
# Transaction / Borrowing Views
# ===========================

@login_required
def borrow_book(request, book_id):
    """
    Borrow a book:
    - GET: Display borrow confirmation form.
    - POST: Create a transaction if the book is available.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        user = request.user

        if book.available_copies > 0:
            due_days = int(request.POST.get('due_days', 7))  # Default 7 days
            due_date = timezone.now().date() + timedelta(days=due_days)

            # Create Transaction record
            Transaction.objects.create(
                user=user,
                book=book,
                borrowed_date=timezone.now().date(),
                due_date=due_date,
                status='borrowed'
            )

            # Update available copies
            book.available_copies -= 1
            book.save()

            messages.success(request, f'Book "{book.title}" borrowed successfully.')
        else:
            messages.error(request, f'Book "{book.title}" is not available.')

        return redirect('book_list')
    else:
        # Render borrow confirmation page
        return render(request, 'library/borrow_book.html', {'book': book})


@login_required
def return_book(request, transaction_id):
    """
    Return a borrowed book:
    - POST: Mark transaction as returned, update returned_date, increase book copies.
    - GET: Render return confirmation page.
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        transaction.status = 'returned'
        transaction.returned_date = timezone.now().date()

        # Optional: calculate fines for late returns
        # if transaction.returned_date > transaction.due_date:
        #     days_late = (transaction.returned_date - transaction.due_date).days
        #     transaction.fine = days_late * 5  # ₹5 per day

        transaction.save()

        # Update book availability
        book = transaction.book
        book.available_copies += 1
        book.save()

        messages.success(request, f'Book "{book.title}" returned successfully.')
        return redirect('my_borrowed_books')
    else:
        return render(request, 'library/return_book.html', {'transaction': transaction})


@login_required
def my_borrowed_books(request):
    """
    List all books currently borrowed by the logged-in user.
    """
    user = request.user
    transactions = Transaction.objects.filter(user=user, status='borrowed')
    return render(request, 'library/my_borrowed_books.html', {'transactions': transactions})




@login_required
def profile(request):
    user = request.user  # current logged-in user
    print(user.username)  # e.g., 'himanshu'
    print(user.email)     # e.g., 'abc@gmail.com'
    print(user.id)        # user’s primary key
    my_added_books = Book.objects.filter(added_by_id=user.id)
    your_borrowed_books = Transaction.objects.filter(book__added_by_id=user.id, status='borrowed')
    return render(request, 'library/profile.html', {'user': user , 'my_books': my_added_books , 'borrowed_books': your_borrowed_books})




