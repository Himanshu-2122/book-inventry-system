from django.contrib import admin
from .models import Book, Transaction

# Registering models to appear in admin
admin.site.register(Book)
admin.site.register(Transaction)



# Register models so they can be managed via the Django admin dashboard.

# Customize the admin interface:

# Which fields are displayed in the list view.

# Filters and search functionality.

# Form layouts for adding or editing entries.