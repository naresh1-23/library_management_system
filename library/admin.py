from django.contrib import admin
from .models import Book, BookDetail, User, BookBorrowed

admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(User)
admin.site.register(BookBorrowed)


