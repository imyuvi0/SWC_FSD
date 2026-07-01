from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Game, Publisher
from .serializers import GameSerializer, PublisherSerializer
from .permissions import IsOwnerOrReadOnly


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        publisher, _ = Publisher.objects.get_or_create(
            user=self.request.user,
            defaults={
                'name': self.request.user.username,
                'webhook_url': 'https://example.com/default-webhook',
                'webhook_secret': 'default-webhook-secret-key-123'
            }
        )
        serializer.save(publisher=publisher)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
