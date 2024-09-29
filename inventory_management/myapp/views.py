from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer  # Serializer for input validation


# views.py (for fetching items)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item  # Assuming you have an Item model



class UserRegistrationView(APIView):
    def post(self, request):
        # Extract data from request body
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Extract user information
                username = serializer.validated_data['username']
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                # Create user object and save to MySQL database
                user = User.objects.create_user(username=username, email=email, password=password)
                
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response({"error": "Username or Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Check if the password matches
            if user.check_password(password):
                # Generate JWT token for authenticated user
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email"}, status=status.HTTP_404_NOT_FOUND)





class ItemListView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        # Fetch items from the database
        items = Item.objects.all().values()  # Query items
        return Response(items)



# @api_view(['GET'])
# def protected_view(request):
#     return Response({"message": "You are authenticated"}, status=200)


# def registration(request):
#     template = loader.get_template('registration.html')
#     return HttpResponse(template.render())


# @api_view(['GET'])
# def home_page(request):
#     template = loader.get_template('home_page.html')
#     return HttpResponse(template.render())

# @api_view(['GET'])
# def get_items(request):
#     return HttpResponse("get method")

# def post_items(request):
#     return HttpResponse("post method")    

# def put_items(request):
#     return HttpResponse("put method")

# def delete_items(request):
#     return HttpResponse("delete method")        

# # def members(request):
# #     return HttpResponse("Hello world!")



# # def members(request):
# #     return HttpResponse("Hello world!")    
