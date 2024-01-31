from django.shortcuts import render
from rest_framework.views import APIView
from .models import Book, BookDetail, User, BookBorrowed
from .serializers import BookDetailSerializer, BookSerializer, UserSerializer, BookBorrowedSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


#This api view is used to list all the books and also used to add books
class BookView(APIView):    
    def get(self,request, format = None ):
        data = Book.objects.all()
        serialized_data = BookSerializer(data = data, many = True)
        serialized_data.is_valid()
        return Response({"status": 200,"data":serialized_data.data}, status = status.HTTP_200_OK)
    
    def post(self, request, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            data = {
                "title": request.data.get("title"),
                "isbn": request.data.get("isbn"),
                "publishedDate": request.data.get("publishedDate"),
                "genre": request.data.get("genre"),
            }
            #checking whether the book is already there or not
            checking_data= Book.objects.filter(title=request.data.get("title")).first()
            if checking_data:
                return Response({"status": 400,"message": "data already exist"}, status = status.HTTP_400_BAD_REQUEST)
            serializer = BookSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200,"data":serializer.data}, status = status.HTTP_201_CREATED)
            return Response({"status": 200,"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    

#This view is used to see the detail of the book. In this book have 1-1 relationship with the detail model
class BookDetailView(APIView):    
    def get(self,request, format = None ):
        data = BookDetail.objects.all()
        serialized_data = BookDetailSerializer(data = data, many = True)
        serialized_data.is_valid()
        return Response({"status": 200,"data":serialized_data.data}, status = status.HTTP_200_OK)
    
    def post(self, request, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            book = Book.objects.filter(id = request.data.get("book_id")).first()
            if not book:
                return Response({"status": 400,"message":"Selected book doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            serializer = BookDetailSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200,"data":serializer.data}, status = status.HTTP_201_CREATED)
            return Response({"status": 400,"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
#this is used to update, delete and get single book detail.
class BookDetailUpdateDeleteView(APIView):
    def get(self, request, pk, format = None):
        data = BookDetail.objects.filter(book_id = pk).first()
        book = Book.objects.filter(id = pk).first()
        if not data:
            return Response({"status":400,"message":"data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
        serialized_data = BookDetailSerializer(data)
        serialized_book = BookSerializer(book)
        return Response({"status": 200,"book":serialized_book.data,"data":serialized_data.data}, status = status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:   
            book_detail = BookDetail.objects.filter(book_id = pk).first()
            if not book_detail:
                return Response({"status":400,"message":"data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            serializer = BookDetailSerializer(book_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200,"data":serializer.data}, status = status.HTTP_202_ACCEPTED)
            return Response({"status": 400,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
    
    def delete(self, request, pk, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:    
            book_detail = BookDetail.objects.filter(book_id = pk).first()
            if not book_detail:
                return Response({"status": 400,"message":"data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            book_detail.delete()
            return Response({"status": 200,"message":"data deleted successfully"},status = status.HTTP_200_OK)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
class UserLists(APIView):
    def get(self, request, format = None):
        if request.user.is_superuser:   
            user = User.objects.all()
            serializer = UserSerializer(data = user, many = True)
            serializer.is_valid()
            return Response({"status": 200,"message": "List of users", "users": serializer.data}, status = status.HTTP_200_OK)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, format= None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser: 
            password = request.data.get("password")
            data = {
                "email": request.data.get("email"),
                "full_name": request.data.get("full_name"),
                "password": make_password(password),
                "membership_date": request.data.get("membership_date")
            }
            user = User.objects.filter(email = request.data.get("email")).first()
            if user:
                return Response({"status": 400, "message": "User already exist"}, status = status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200, "message": "User successfully created"}, status = status.HTTP_201_CREATED)
            return Response({"status": 400, "error": serializer.errors}, status = stats.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)

class UserUpdateDeleteView(APIView):
    def get(self, request, pk, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            data = User.objects.filter(id = pk).first()
            if not data:
                return Response({"status":400,"message":"User doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            serialized_data = UserSerializer(data)
            return Response({"status": 200,"data":serialized_data.data}, status = status.HTTP_200_OK)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            user_detail = User.objects.filter(id = pk).first()
            if not user_detail:
                return Response({"status":400,"message":"User doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            password = request.data.get("password")
            data = {
                "email": request.data.get("email"),
                "full_name": request.data.get("full_name"),
                "password": make_password(password),
                "membership_date": request.data.get("membership_date")
            }
            serializer = UserSerializer(user_detail, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200,"data":serializer.data}, status = status.HTTP_202_ACCEPTED)
            return Response({"status": 400,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            user_detail = User.objects.filter(id = pk).first()
            if not user_detail:
                return Response({"status": 400,"message":"User doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            user_detail.delete()
            return Response({"status": 200,"message":"User deleted successfully"},status = status.HTTP_200_OK)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
    
            
class BookBorrowLists(APIView):
    def get(self, request, format = None):
        borrowed = BookBorrowed.objects.all()
        serializer = BookBorrowedSerializer(data = borrowed, many = True)
        serializer.is_valid()
        return Response({"status": 200,"message": "List of borrowers", "data": serializer.data}, status = status.HTTP_200_OK)
    
    def post(self, request, format= None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            serializer = BookBorrowedSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200, "message": "Book borrowed successfully added"}, status = status.HTTP_201_CREATED)
            return Response({"status": 400, "error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
        
    

class BorrowUpdateDeleteView(APIView):
    def get(self, request, pk, format = None):
        data = BookBorrowed.objects.filter(user_id = pk).first()
        if not data:
            return Response({"status":400,"message":"Data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
        serialized_data = BookBorrowedSerializer(data)
        return Response({"status": 200,"data":serialized_data.data}, status = status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            borrower_detail = BookBorrowed.objects.filter(user_id = pk).first()
            if not borrower_detail:
                return Response({"status":400,"message":"Data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            serializer = BookBorrowedSerializer(borrower_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200,"data":serializer.data}, status = status.HTTP_202_ACCEPTED)
            return Response({"status": 400,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)
        
    
    def delete(self, request, pk, format = None):
        #checked whether given user is admin or not. Since, only admin can add delete and update
        if request.user.is_superuser:
            borrower_detail = BookBorrowed.objects.filter(user_id = pk).first()
            if not borrower_detail:
                return Response({"status": 400,"message":"Data doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            borrower_detail.delete()
            return Response({"status": 200,"message":"Data deleted successfully"},status = status.HTTP_200_OK)
        return Response({"status": 400, "message": "access denied"}, status = status.HTTP_401_UNAUTHORIZED)

#Since, I have used token authentication system using simple jwt.
#Below function return access token for authenticated users which can be used to check the users.
    
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token)
    }

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens(user)
                return Response({"status":200,'token': token, 'msg': 'logged in'}, status = status.HTTP_202_ACCEPTED)
            return Response({"status": 400, "error": "User doesn't exists"}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"status": 400, "error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    