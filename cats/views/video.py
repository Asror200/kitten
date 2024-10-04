from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from cats.models import Video
from cats import serializers, permissions
from django.shortcuts import get_object_or_404


class VideoAddAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Video.objects.all()
    serializer_class = serializers.VideoSerializer


class VideoUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    queryset = Video.objects.all()
    serializer_class = serializers.VideoSerializer
    lookup_field = 'pk'

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        return obj

    def put(self, request, pk, *args, **kwargs):
        video = self.get_object(pk)
        if video:
            serializer = serializers.VideoSerializer(video, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        video = self.get_object(pk)
        if video:
            serializer = serializers.VideoSerializer(video, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        video = self.get_object()
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
