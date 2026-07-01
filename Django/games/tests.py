from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Publisher, Game, GameKey, Order, OrderItem


class GameKeyPlatformTests(APITestCase):

    def setUp(self):
        # Create users
        self.user_pub_a = User.objects.create_user(username='publisher_a', password='password123')
        self.user_pub_b = User.objects.create_user(username='publisher_b', password='password123')
        self.user_buyer = User.objects.create_user(username='buyer', password='password123')

        # Create tokens
        self.token_pub_a = Token.objects.create(user=self.user_pub_a)
        self.token_pub_b = Token.objects.create(user=self.user_pub_b)
        self.token_buyer = Token.objects.create(user=self.user_buyer)

        # Create publishers
        self.pub_a = Publisher.objects.create(
            name='Publisher A',
            webhook_url='https://example.com/webhook-a',
            webhook_secret='secret-a',
            user=self.user_pub_a
        )
        self.pub_b = Publisher.objects.create(
            name='Publisher B',
            webhook_url='https://example.com/webhook-b',
            webhook_secret='secret-b',
            user=self.user_pub_b
        )

        # Create game
        self.game = Game.objects.create(
            title='Epic Game 1',
            publisher=self.pub_a,
            price=19.99
        )

        # Create game keys
        self.key_1 = GameKey.objects.create(
            key_string='ABCD-1234-EFGH-5678',
            game=self.game,
            status='active',
            expires_at=timezone.now() + timezone.timedelta(days=30)
        )
        self.key_2 = GameKey.objects.create(
            key_string='WXYZ-9876-UVTS-5432',
            game=self.game,
            status='active',
            expires_at=timezone.now() + timezone.timedelta(days=30)
        )

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'new_user', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_anonymous_user_read_only(self):
        url = reverse('game-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        data = {'title': 'New Game', 'publisher': self.pub_a.id, 'price': 9.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_create_game(self):
        url = reverse('game-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_pub_a.key)
        data = {'title': 'New Game', 'publisher': self.pub_a.id, 'price': 29.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_is_owner_permission(self):
        url = reverse('game-detail', kwargs={'pk': self.game.id})

        # Publisher B attempts to edit Publisher A's game -> 403 Forbidden
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_pub_b.key)
        data = {'title': 'Hacked Title', 'publisher': self.pub_a.id, 'price': 1.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Publisher A modifies their own game -> 200 OK
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_pub_a.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game.refresh_from_db()
        self.assertEqual(self.game.title, 'Hacked Title')

    def test_purchase_key_success(self):
        url = reverse('purchase_key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_buyer.key)
        data = {'game_id': self.game.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['game_title'], self.game.title)

        # Verify key has been allocated and assigned in db
        assigned_key = GameKey.objects.get(owner=self.user_buyer)
        self.assertEqual(assigned_key.status, 'active')

    def test_purchase_key_no_stock(self):
        # Mark both keys as already owned
        self.key_1.owner = self.user_pub_b
        self.key_1.save()
        self.key_2.owner = self.user_pub_b
        self.key_2.save()

        url = reverse('purchase_key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_buyer.key)
        data = {'game_id': self.game.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No available keys for this game.')
