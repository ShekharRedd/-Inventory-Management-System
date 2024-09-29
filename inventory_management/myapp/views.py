from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db import IntegrityError
from .models import User, Item
from .serializers import UserSerializer, ItemSerializer
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
import logging

CACHE_TTL = 300  # 5 minutes

# Get the custom logger
logger = logging.getLogger('myapp')



class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                username = serializer.validated_data['username']
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                user = User.objects.create_user(username=username, email=email, password=password)
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Username or Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    logger.info(f'User {request.user} is attempting to create an item')

    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        if Item.objects.filter(name=serializer.validated_data['name']).exists():
            return Response({"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info(f'Item {serializer.data["name"]} created successfully by user {request.user}')

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    logger.error(f'Invalid data provided by user {request.user}: {serializer.errors}')
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, item_id):
    logger.info(f'User {request.user} is trying to read item with ID {item_id}')

    # Check if the item is cached in Redis
    cache_key = f'item_{item_id}'
    item = cache.get(cache_key)

    # If item is not cached, fetch it from the database
    if not item:
        logger.debug(f'Item with ID {item_id} not found in cache, fetching from database')

        try:
            item = Item.objects.get(id=item_id)
            # Store the item in Redis cache
            cache.set(cache_key, item, timeout=CACHE_TTL)\
            logger.info(f'Item {item_id} fetched from database and cached')
            
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
    
    # Convert item to a serializable format for the response
    item_data = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'quantity': item.quantity,
        'price': item.price
    }
    logger.info(f'Item {item_id} returned successfully to user {request.user}')
    
    return Response(item_data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    logger.info(f'User {request.user} is trying to update item with ID {item_id}')

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.error(f'Item with ID {item_id} not found for update')

        return Response({"error": "Item not found"}, status=404)
    
    # Update item attributes
    item.name = request.data.get('name')
    item.description = request.data.get('description')
    item.quantity = request.data.get('quantity')
    item.price = request.data.get('price')
    item.save()
    logger.info(f'Item {item_id} updated successfully and cache invalidated')

    # Invalidate cache after update
    cache_key = f'item_{item_id}'
    cache.delete(cache_key)

    return Response({"message": "Item updated successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    logger.info(f'User {request.user} is trying to delete item with ID {item_id}')

    try:
        item = Item.objects.get(id=item_id)
        item.delete()

        # Invalidate cache after deletion
        cache_key = f'item_{item_id}'
        cache.delete(cache_key)
        logger.info(f'Item {item_id} deleted successfully and cache invalidated')

        return Response({"message": "Item deleted successfully"})
    except Item.DoesNotExist:
        logger.error(f'Item with ID {item_id} not found for deletion')

        return Response({"error": "Item not found"}, status=404)
