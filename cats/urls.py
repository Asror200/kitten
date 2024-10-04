from django.urls import path
from cats.views import breed, cat, video, image

urlpatterns = [
    path('breeds/', breed.BreedListView.as_view(), name='breeds'),
    path('breed/<int:pk>/', breed.BreedDetailView.as_view(), name='breed-detail'),

    path('cats/', cat.CatListCreateUpdateView.as_view(), name='cats-list-create'),
    path('cat/<int:pk>/', cat.CatListCreateUpdateView.as_view(), name='cat-update'),
    path('video-create/', video.VideoAddAPIView.as_view(),
         name='video-create'),

    path('video-update-delete/<int:pk>/', video.VideoUpdateDeleteAPIView.as_view(),
         name='video-update-delete'),

    path('image-create/', image.ImageAddAPIView.as_view(),
         name='image-create'),

    path('image-update-delete/<int:pk>/', image.ImageUpdateDeleteAPIView.as_view(),
         name='image-update-delete'),

]
