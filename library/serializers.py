from rest_framework import serializers
from .models import Book, BookDetail, User, BookBorrowed

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, allow_null=True)
    is_staff = serializers.BooleanField(required=False, allow_null=True)
    is_superuser = serializers.BooleanField(required=False, allow_null=True)
    class Meta:
        model = User
        exclude = ()
        read_only_fields = ("id",)

#serializer for login
class UserLoginSerializer(serializers.ModelSerializer):   
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ["email", "password"]

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ()
        read_only_fields = ("id",)
         
class BookDetailSerializer(serializers.ModelSerializer):  
    class Meta:
        model = BookDetail
        exclude = ()
        read_only_fields = ("id",)
        
class BookBorrowedSerializer(serializers.ModelSerializer):
    returned_date = serializers.DateField(required= False, allow_null=True)
    
    class Meta:
        model = BookBorrowed
        exclude = ()
        read_only_fields = ("id",)
        
        