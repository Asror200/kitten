from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from cats.models import Cat
from cats import serializers, permissions
from django.http import Http404


class CatListCreateUpdateView(generics.GenericAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Cat.objects.all()
    """ In this class, you can perform various actions, including showing all cats,
        creating new ones, updating existing ones, and deleting them. However, remember:
        if you want to update or delete a cat, you must be the owner of that cat."""

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return serializers.CatCreateUpdateSerializer
        return serializers.CatSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            cat = self.get_object(pk)
            serializer = serializers.CatDetailSerializer(cat, context={'request': request})
            return Response(serializer.data)

        cats = self.get_queryset()
        serializer = self.get_serializer_class()(cats, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CatCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Cat.objects.get(pk=pk)
        except Cat.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        cat = self.get_object(pk)
        serializer = self.get_serializer_class()(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        cat = self.get_object(pk)
        serializer = self.get_serializer_class()(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        cat = self.get_object(pk)
        if cat:
            cat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
