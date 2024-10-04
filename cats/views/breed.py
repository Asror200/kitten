from cats import serializers, permissions
from rest_framework import generics, viewsets
from cats.models import Breed
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BreedListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Breed.objects.all()
    serializer_class = serializers.BreedSerializer


class BreedDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
    queryset = Breed.objects.all()
    serializer_class = serializers.BreedDetailSerializer
    lookup_field = 'pk'