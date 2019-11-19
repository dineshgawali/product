from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import SignUpSerializer
from django.views.generic import View
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from product_app.models import Product, UserRating
from product_app.serializer import ProductSerializer, RatingSerializer
from rest_framework.views import APIView
# Create your views here.

def new_post(request):
    return HttpResponse("Running")


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    #permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if not username and not password:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username):
            return Response(
                data={
                    "message": "user with same username already exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_user = User.objects.create_user(
            username=username, password=password
        )
        data = dict()
        data['data'] = request.data
        data['message'] = "User sign up successfullly"
        return Response(data=data, status=status.HTTP_201_CREATED)

    # def get(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    @csrf_exempt
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # login(request, user)
                data = dict()
                data['username'] = user.username	
                data['first_name'] = user.first_name	
                data['last_name'] = user.last_name
                return Response(data=data, )

            else:
                return Response(
                data={
                    "message": "User not activate"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                data={
                    "message": "username  and password not matches"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRatingView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
    queryset = UserRating.objects.all()
    serializer_class = RatingSerializer
    def get(self, request, format=None):
        rating = UserRating.objects.all()
        serializer = RatingSerializer(rating, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)