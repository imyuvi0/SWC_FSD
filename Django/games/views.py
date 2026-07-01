from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Game, GameKey, Order, OrderItem
from .serializers import OrderSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # create_user hashes the password using PBKDF2 automatically
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_key(request):
    game_id = request.data.get('game_id')
    if not game_id:
        return Response({'error': 'game_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({'error': 'Game does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        # Retrieve and lock an available GameKey to prevent concurrent double-allocations
        game_key = GameKey.objects.select_for_update().filter(
            game=game,
            owner__isnull=True,
            status='active'
        ).first()

        if not game_key:
            return Response({'error': 'No available keys for this game.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order (automatically assigns a UUID primary key)
        order = Order.objects.create(
            user=request.user,
            total_amount=game.price
        )

        # Create OrderItem linked to order, game, and the locked key
        OrderItem.objects.create(
            order=order,
            game=game,
            game_key=game_key,
            price=game.price
        )

        # Assign the key to the customer
        game_key.owner = request.user
        game_key.save()

        # Serialize order details (containing UUID and nested items)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
