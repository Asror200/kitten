from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Views
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('profile/<int:pk>/', views.UserProfileAPIView.as_view(), name='user-profile'),

    # Authentication
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

]
