from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




# Create your models here.






# class EBooksModel(models.Model):
 
#     title = models.CharField(max_length = 80)
#     summary = models.TextField(max_length=2000)
#     pages = models.CharField(max_length=80)
#     pdf = models.FileField(upload_to='pdfs/')
#     author = models.CharField(max_length=80)
#     category = models.CharField(max_length=80)
#     author_id = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.title}"  #That code defines how an object should be displayed as a plain string, giving it a human-readable name.
#     Before __str__: You see something like <Article object (1)>, <Product object (2)>.

# After __str__: You see the actual title, like "My First Blog Post" or "Wireless Mouse".
    

# # from here i implemented real inventry system

# # -------------------
# # Book Model
# # -------------------
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    pages = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"
    


# -------------------
# User Profile (Optional extension)
# -------------------
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with Django's User model  
# #     user1 = User(username="alice")
# # profile1 = Profile(user=user1, membership_id="M123")

#     # membership_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

#     def __str__(self):
#         return self.user.username



# -------------------
# Transaction Model
# -------------------
class Transaction(models.Model):
    #This is a Python list of tuples used for the status field
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) #who borrowed the book.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)# Which book was borrowed.
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField() # Set days when borrowing
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')
    # fine = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"