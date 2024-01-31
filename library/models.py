from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

#changed user model and made email as unique field instead of username
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    membership_date = models.DateField(default = timezone.now, null = True, blank = True)
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.BooleanField(default=False, blank = True)
    is_superuser = models.BooleanField(default=False, blank = True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} is membered since {self.membership_date}"

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 200)
    isbn = models.CharField(max_length=200)
    publishedDate = models.DateField()
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    
class BookDetail(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.OneToOneField(Book, on_delete = models.CASCADE)
    number_of_page = models.PositiveIntegerField()
    publisher = models.CharField(max_length= 255)
    language = models.CharField(max_length= 150)
    
    def __str__(self):
        return f"detail of {self.book.title}"
    


class BookBorrowed(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    returned_date = models.DateField(null=True, blank = True)
    
    
    def __str__(self):
        return f"{self.user_id.full_name} borrowed book {self.book_id.title}"
    
    